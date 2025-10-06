import pygame
import numpy as np
import math

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

camera = np.array([0.0, 0.0, -1.0])
sphere_center = np.array([0.0, 0.0, 3.0])
sphere_radius = 1.0

fov = math.pi / 2
running = True
clock = pygame.time.Clock()
compression = 4

angleX = 0.0
angleY = 0.0
pygame.mouse.set_visible(False)
sky_color = np.array([135, 206, 235])

light_dir = np.array([1.0, 1.0, -1.0])
light_dir /= np.linalg.norm(light_dir)

def rotate_camera(v, ax, ay):
    sinY, cosY = math.sin(ax), math.cos(ax)
    sinX, cosX = math.sin(ay), math.cos(ay)
    # Поворот Y
    xz_x = v[..., 0] * cosY + v[..., 2] * sinY
    xz_z = -v[..., 0] * sinY + v[..., 2] * cosY
    xz_y = v[..., 1]
    # Поворот X
    yz_y = xz_y * cosX - xz_z * sinX
    yz_z = xz_y * sinX + xz_z * cosX
    return np.stack([xz_x, yz_y, yz_z], axis=-1)

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    dx = pygame.mouse.get_pos()[0] - WIDTH // 2
    dy = pygame.mouse.get_pos()[1] - HEIGHT // 2
    angleX += dx * 0.002
    angleY += dy * 0.002
    pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))

    keys = pygame.key.get_pressed()
    speed = 2.0 if keys[pygame.K_LCTRL] else 0.2
    forward = np.array([math.sin(angleX), 0, math.cos(angleX)])
    right = np.array([math.cos(angleX), 0, -math.sin(angleX)])
    up = np.array([0, 1, 0])

    if keys[pygame.K_w]: camera += forward * speed
    if keys[pygame.K_s]: camera -= forward * speed
    if keys[pygame.K_a]: camera -= right * speed
    if keys[pygame.K_d]: camera += right * speed
    if keys[pygame.K_SPACE]: camera += up * speed
    if keys[pygame.K_LSHIFT]: camera -= up * speed

    screen.fill(sky_color)

    xs = np.arange(0, WIDTH, compression)
    ys = np.arange(0, HEIGHT, compression)
    px, py = np.meshgrid(xs, ys)
    px = (2 * (px + 0.5) / WIDTH - 1) * math.tan(fov / 2) * WIDTH / HEIGHT
    py = -(2 * (py + 0.5) / HEIGHT - 1) * math.tan(fov / 2)
    ray_dirs = np.stack([px, py, np.ones_like(px)], axis=-1)
    ray_dirs = rotate_camera(ray_dirs, angleX, angleY)
    ray_dirs /= np.linalg.norm(ray_dirs, axis=-1)[..., None]

    oc = camera - sphere_center
    a = np.sum(ray_dirs**2, axis=-1)
    b = 2 * np.sum(oc * ray_dirs, axis=-1)
    c = np.sum(oc**2) - sphere_radius**2
    disc = b**2 - 4*a*c

    hit_mask = disc >= 0
    t = np.zeros_like(a)
    t[hit_mask] = (-b[hit_mask] - np.sqrt(disc[hit_mask])) / (2*a[hit_mask])
    t[t < 0] = 0
    hit_mask &= t > 0

    # Цвета
    color = np.zeros(ray_dirs.shape, dtype=np.float32)
    hit_points = camera + ray_dirs * t[..., None]
    normals = hit_points - sphere_center
    normals /= np.linalg.norm(normals, axis=-1)[..., None]
    brightness = np.clip(np.sum(normals * light_dir, axis=-1), 0.2, 1.0)
    cvals = ((sky_color + 240) / 510 * 255 * brightness[..., None]).astype(np.uint8)

    # Рисуем пиксели
    for i in range(ys.shape[0]):
        for j in range(xs.shape[0]):
            if hit_mask[i, j]:
                pygame.draw.rect(screen, cvals[i, j], (xs[j], ys[i], compression, compression))

    pygame.display.flip()
    clock.tick(30)

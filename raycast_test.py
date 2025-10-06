import pygame
import numpy as np
import math

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raycast Sphere + Plane NumPy")

camera = np.array([0.0, 0.0, -3.0], dtype=np.float32)
sphere_center = np.array([0.0, 0.0, 3.0], dtype=np.float32)
sphere_radius = 1.0

compression = 4

fov = np.pi / 2
running = True
clock = pygame.time.Clock()

angleX, angleY = 0.0, 0.0
pygame.mouse.set_visible(False)

sky_color = np.array([135, 206, 235], dtype=np.float32)
sphere_color = np.array([255, 255, 255], dtype=np.float32)
plane_color = np.array([200, 200, 200], dtype=np.float32)
light_dir = np.array([1.0, 1.0, -1.0], dtype=np.float32)
light_dir /= np.linalg.norm(light_dir)

plane_y = -1.5  # высота пола

# Предвычисляем координаты пикселей в сжатом виде
h_c = HEIGHT // compression
w_c = WIDTH // compression
xs_c = (2 * (np.arange(w_c) + 0.5) / w_c - 1) * np.tan(fov / 2) * WIDTH / HEIGHT
ys_c = -(2 * (np.arange(h_c) + 0.5) / h_c - 1) * np.tan(fov / 2)
px_c, py_c = np.meshgrid(xs_c, ys_c)
pz_c = np.ones_like(px_c)
ray_dirs_c = np.stack([px_c, py_c, pz_c], axis=-1)
ray_dirs_c /= np.linalg.norm(ray_dirs_c, axis=-1, keepdims=True)

def rotate_rays(rays, forward, right, up):
    rotated = rays[...,0][...,np.newaxis]*right + \
              rays[...,1][...,np.newaxis]*up + \
              rays[...,2][...,np.newaxis]*forward
    rotated /= np.linalg.norm(rotated, axis=-1, keepdims=True)
    return rotated



while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    dx, dy = np.array(pygame.mouse.get_pos()) - np.array([WIDTH // 2, HEIGHT // 2])
    angleX -= dx * 0.002
    angleY -= dy * 0.002
    pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))

    keys = pygame.key.get_pressed()
    speed = 2.0 if keys[pygame.K_LCTRL] else 0.1
    # горизонтальный угол
    cosX, sinX = math.cos(angleX), math.sin(angleX)
    # вертикальный угол
    cosY, sinY = math.cos(angleY), math.sin(angleY)

    forward = np.array([
        math.sin(angleX) * math.cos(angleY),  # x
        math.sin(angleY),  # y
        math.cos(angleX) * math.cos(angleY)  # z
    ], dtype=np.float32)

    right = np.cross(forward, np.array([0, 1, 0], dtype=np.float32))
    right /= np.linalg.norm(right)

    up = np.cross(right, forward)
    up /= np.linalg.norm(up)

    if keys[pygame.K_w]: camera += forward * speed
    if keys[pygame.K_s]: camera -= forward * speed
    if keys[pygame.K_a]: camera -= right * speed
    if keys[pygame.K_d]: camera += right * speed
    if keys[pygame.K_SPACE]: camera += up * speed
    if keys[pygame.K_LSHIFT]: camera -= up * speed

    screen_array = np.tile(sky_color, (h_c, w_c, 1))
    rays = rotate_rays(ray_dirs_c, forward, right, up)

    # --- Сфера ---
    oc = camera - sphere_center
    a = np.sum(rays * rays, axis=-1)
    b = 2 * np.sum(oc * rays, axis=-1)
    c = np.sum(oc * oc) - sphere_radius**2
    disc = b**2 - 4*a*c
    mask_sphere = disc >= 0
    t_sphere = np.zeros_like(disc)
    t_sphere[mask_sphere] = (-b[mask_sphere] - np.sqrt(disc[mask_sphere])) / (2*a[mask_sphere])
    mask_sphere &= t_sphere > 0
    t_sphere_final = np.where(mask_sphere, t_sphere, np.inf)

    # --- Плоскость ---
    # y = plane_y => t_plane = (plane_y - camera_y) / ray_y
    t_plane = (plane_y - camera[1]) / rays[..., 1]
    mask_plane = (t_plane > 0)
    t_plane_final = np.where(mask_plane, t_plane, np.inf)

    # --- Выбираем ближайший объект ---
    mask_sphere_final = t_sphere_final < t_plane_final
    mask_plane_final = ~mask_sphere_final & (t_plane_final != np.inf)

    # Рендер сферы
    if np.any(mask_sphere_final):
        hit = camera + rays * t_sphere_final[..., np.newaxis]
        normal = hit - sphere_center
        normal /= np.linalg.norm(normal, axis=-1, keepdims=True)
        brightness = np.clip(np.sum(normal * light_dir, axis=-1), 0.2, 1.0)
        for i in range(3):
            screen_array[..., i][mask_sphere_final] = sphere_color[i] * brightness[mask_sphere_final]

    # Рендер плоскости
    if np.any(mask_plane_final):
        hit_plane = camera + rays * t_plane_final[..., np.newaxis]
        # Плоскость горизонтальная, нормаль (0,1,0)
        normal = np.array([0, 1, 0], dtype=np.float32)
        brightness = np.clip(np.sum(normal * light_dir), 0.2, 1.0)
        for i in range(3):
            screen_array[..., i][mask_plane_final] = plane_color[i] * brightness

    # Масштабирование обратно
    screen_array_full = np.repeat(np.repeat(screen_array, compression, axis=0), compression, axis=1)
    pygame.surfarray.blit_array(screen, np.transpose(screen_array_full[:HEIGHT, :WIDTH], (1,0,2)).astype(np.uint8))

    pygame.display.flip()
    clock.tick(30)

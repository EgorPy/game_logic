import pygame
import math

pygame.init()
WIDTH, HEIGHT = 1280, 720  # pygame.display.get_window_size()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

camera = [0, 0, -1]
sphere_center = (0, 0, 3)
sphere_radius = 1

fov = math.pi / 2
running = True
clock = pygame.time.Clock()

compression = 8

angleX = 0
angleY = 0
pygame.mouse.set_visible(False)

sky_color = (135, 206, 235)


def normalize(v):
    length = math.sqrt(sum(x * x for x in v))
    return (v[0] / length, v[1] / length, v[2] / length)


def normalize_val(v, length):
    return v / length


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def rotate(v, ax, ay):
    # Вращение вокруг оси Y (влево-вправо)
    sinY, cosY = math.sin(ax), math.cos(ax)
    xz_rot = (v[0] * cosY + v[2] * sinY, v[1], -v[0] * sinY + v[2] * cosY)
    # Вращение вокруг оси X (вверх-вниз)
    sinX, cosX = math.sin(ay), math.cos(ay)
    yz_rot = (xz_rot[0], xz_rot[1] * cosX - xz_rot[2] * sinX, xz_rot[1] * sinX + xz_rot[2] * cosX)
    return yz_rot


# 1. Предвычисляем свет
light_dir = normalize((1, 1, -1))

# 2. Предвычисляем матрицу поворота камеры
sinX, cosX = math.sin(angleY), math.cos(angleY)
sinY, cosY = math.sin(angleX), math.cos(angleX)


def rotate_camera(v):
    x, y, z = v
    # поворот Y
    xz_x = x * cosY + z * sinY
    xz_z = -x * sinY + z * cosY
    xz_y = y
    # поворот X
    yz_y = xz_y * cosX - xz_z * sinX
    yz_z = xz_y * sinX + xz_z * cosX
    return (xz_x, yz_y, yz_z)


while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    dx = pygame.mouse.get_pos()[0] - WIDTH // 2
    dy = pygame.mouse.get_pos()[1] - HEIGHT // 2
    angleX += dx * 0.002
    angleY += dy * 0.002
    pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))

    sinX, cosX = math.sin(angleY), math.cos(angleY)
    sinY, cosY = math.sin(angleX), math.cos(angleX)

    # print(angleX, angleY)

    keys = pygame.key.get_pressed()
    forward = normalize((math.sin(angleX), 0, math.cos(angleX)))
    right = normalize((math.cos(angleX), 0, -math.sin(angleX)))
    up = (0, 1, 0)

    if keys[pygame.K_LCTRL]:
        speed = 2
    else:
        speed = 0.2
    if keys[pygame.K_w]:
        camera[0] += forward[0] * speed
        camera[2] += forward[2] * speed
    if keys[pygame.K_s]:
        camera[0] -= forward[0] * speed
        camera[2] -= forward[2] * speed
    if keys[pygame.K_a]:
        camera[0] -= right[0] * speed
        camera[2] -= right[2] * speed
    if keys[pygame.K_d]:
        camera[0] += right[0] * speed
        camera[2] += right[2] * speed
    if keys[pygame.K_SPACE]:
        camera[1] += speed
    if keys[pygame.K_LSHIFT]:
        camera[1] -= speed

    screen.fill(sky_color)

    for y in range(0, HEIGHT, compression):
        for x in range(0, WIDTH, compression):
            px = (2 * (x + 0.5) / WIDTH - 1) * math.tan(fov / 2) * WIDTH / HEIGHT
            py = -(2 * (y + 0.5) / HEIGHT - 1) * math.tan(fov / 2)

            # ray_dir = normalize((px, py, 1))
            ray_dir = rotate_camera((px, py, 1))

            oc = sub(camera, sphere_center)
            a = dot(ray_dir, ray_dir)
            b = 2 * dot(oc, ray_dir)
            c = dot(oc, oc) - sphere_radius ** 2
            disc = b * b - 4 * a * c

            if disc >= 0:
                t = (-b - math.sqrt(disc)) / (2 * a)
                if t > 0:
                    hit = (camera[0] + ray_dir[0] * t,
                           camera[1] + ray_dir[1] * t,
                           camera[2] + ray_dir[2] * t)
                    normal = normalize(sub(hit, sphere_center))
                    light_dir = normalize((1, 1, -1))
                    brightness = max(0.2, dot(normal, light_dir))
                    cval1 = int(255 * normalize_val(sky_color[0] + 240, 510) * brightness)
                    cval2 = int(255 * normalize_val(sky_color[1] + 240, 510) * brightness)
                    cval3 = int(255 * normalize_val(sky_color[2] + 240, 510) * brightness)
                    pygame.draw.rect(screen, (cval1, cval2, cval3), (x, y, compression, compression))

    pygame.display.flip()
    clock.tick(30)


import pygame as pg
import math as m
from opensimplex import OpenSimplex

# variables listed with values

class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def normalize(self):
        magnitude = m.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        if magnitude != 0:
            self.x /= magnitude
            self.y /= magnitude
            self.z /= magnitude

class Light:
    def __init__(self, direction, intensity=1.0):
        self.direction = direction  
        self.intensity = intensity

light = Light(Vector(0, -1, -1), intensity=1.0)  # Example: light pointing downward (ye implemented nahi hai yet, depends on solar intensity)
light.direction.normalize()

def generate_normal_map(radius: int, center: Vector, width: int, height: int, simplex: OpenSimplex) -> pg.Surface:
    display = pg.Surface((width, height))
    for x in range(-radius, radius):
        for y in range(-radius, radius):
            if (x * x + y * y) <= radius * radius:
                # Normal calculation
                normal = Vector(
                    -(radius - x) / radius + 1,
                    (radius - y) / radius - 1
                )
                normal.z = m.sqrt(max(0, 1 - (normal.x * normal.x + normal.y * normal.y)))
                normal.normalize()
                
                terrain_value = 0.5 * simplex.noise3(normal.x, normal.y, normal.x)
                terrain_value += 0.25 * (simplex.noise3(normal.x * 4, normal.y * 4, normal.x * 4) + 1) / 2
                terrain_value += 0.125 * (simplex.noise3(normal.x * 8, normal.y * 8, normal.x * 8) + 1) / 2
                terrain_value += 0.125 * (simplex.noise3(normal.x * 16, normal.y * 16, normal.x * 16) + 1) / 2
                terrain_value += 0.0625 * (simplex.noise3(normal.x * 32, normal.y * 32, normal.x * 32) + 1) / 2
                terrain_value += 0.03125 * (simplex.noise3(normal.x * 64, normal.y * 64, normal.x * 64) + 1) / 2
                terrain_value += 0.015625 * (simplex.noise3(normal.x * 128, normal.y * 128, normal.x * 128) + 1) / 2

                # Determine terrain color
                if terrain_value < -0.25:
                    color = (139, 69, 19)  # Brown
                elif terrain_value < 0:
                    color = (205, 133, 63)  # Sandy Brown
                elif terrain_value < 0.25:
                    color = (135, 206, 250)  # Light Blue
                else:
                    color = (34, 139, 34)  # Steel Blue

                display.set_at((center.x + x, center.y + y), color)

                # Clouds
                cloud_value = simplex.noise3(normal.x * 2, normal.y * 2, normal.z)
                if cloud_value > 0.3:   # we will replace this with the cloud density formula/value
                    light_direction = Vector(-0.5, -0.5, -1)
                    light_direction.normalize()
                    light_power = max(0, normal.x * light_direction.x +
                                         normal.y * light_direction.y +
                                         normal.z * light_direction.z)
                    cloud_color = (255, 255, 255)
                    # cloud_final_color = tuple(int(c * light_power) for c in cloud_color)
                    # display.set_at((center.x + x, center.y + y), cloud_color)

                    alpha = 0.5  # Transparency level (0.0 = fully transparent, 1.0 = fully opaque)

                    try:
                        background_color = display.get_at((center.x + x, center.y + y))[:3]
                    except IndexError:
                        background_color = (0, 0, 0)

                    blended_color = (
                        int(alpha * cloud_color[0] + (1 - alpha) * background_color[0]),
                        int(alpha * cloud_color[1] + (1 - alpha) * background_color[1]),
                        int(alpha * cloud_color[2] + (1 - alpha) * background_color[2]),
                    )

                    display.set_at((center.x + x, center.y + y), blended_color)

    return display
# TO ADD:
# levers
# Population (city lights?)
# solar intensity
# sun 


def main():
    pg.init()
    width, height = 800, 600
    display = pg.display.set_mode((width, height))
    center = Vector(width // 2, height // 2)
    radius = 200

    simplex = OpenSimplex(seed=42)

    normal_map = generate_normal_map(radius, center, width, height, simplex)

    display.blit(normal_map, (0, 0))
    pg.display.flip()

    # Main event loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

    pg.quit()


if __name__ == "__main__":
    main()

import pygame
from typing import Tuple
import json

AXIS_COLOR = (160, 160, 160)
POINT_COLOR = (200, 200, 200)
GRAPH_COLOR = (255, 255, 255)
DEFAULT_FILENAME = "data.json"

virtual_origin_pos_shift = (200, -600)

def screen_to_virtual_coords(screen_pos: Tuple[float, float]) -> Tuple[float, float]:
    return (screen_pos[0] - virtual_origin_pos_shift[0], -screen_pos[1] - virtual_origin_pos_shift[1])

def virtual_to_screen_coords(virt_pos: Tuple[float, float]) -> Tuple[float, float]:
    return (virt_pos[0] + virtual_origin_pos_shift[0], -virt_pos[1] - virtual_origin_pos_shift[1])

def draw_axis(surface):
    pygame.draw.line(surface, AXIS_COLOR, virtual_to_screen_coords((-2000, 0)), virtual_to_screen_coords((2000, 0)), 3)
    pygame.draw.line(surface, AXIS_COLOR, virtual_to_screen_coords((0, -2000)), virtual_to_screen_coords((0, 2000)), 3)

# takes in virtual position
def draw_point_at_position(surface, position: Tuple[float, float]):
    pygame.draw.circle(surface, POINT_COLOR, virtual_to_screen_coords(position), 5)
    # pygame.draw.circle(surface, POINT_COLOR, virtual_to_screen_coords(position), 8)

def save_points_to_json(data: list, filename: str = DEFAULT_FILENAME):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def load_json_file(filename: str = DEFAULT_FILENAME) -> list[Tuple[float, float]]:
    with open(filename, 'r') as file:
        return json.load(file)
    
digit_to_superscript_mapping = {
    0: "⁰",
    1: "¹",
    2: "²",
    3: "³",
    4: "⁴",
    5: "⁵",
    6: "⁶",
    7: "⁷",
    8: "⁸",
    9: "⁹",
}
def number_to_subscript(num: int):
    result = ""
    for char in str(num):
        if char in digit_to_superscript_mapping:
            result += digit_to_superscript_mapping[char]

    return result

def draw_function(screen, fn):
    points = []
    for x in range(-1000, 1000, 10):
        points.append((x, fn(x)))

    for i in range(len(points) - 1):
        pygame.draw.line(screen, GRAPH_COLOR, virtual_to_screen_coords(points[i]), virtual_to_screen_coords(points[i + 1]), 2)
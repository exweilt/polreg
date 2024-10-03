import pygame
from typing import Tuple
import json
import copy

AXIS_COLOR = (160, 160, 160)
POINT_COLOR = (200, 200, 200)
GRAPH_COLOR = (255, 255, 255)
DEFAULT_FILENAME = "data.json"

# screen space position of virtual origin. y is inversed
virtual_origin_pos_shift = [200, -600]
scale = 1.0

def screen_to_virtual_coords(screen_pos: Tuple[float, float]) -> Tuple[float, float]:
    return (
        (screen_pos[0] * scale - virtual_origin_pos_shift[0]), 
        (-screen_pos[1] * scale - virtual_origin_pos_shift[1])
    )

def virtual_to_screen_coords(virt_pos: Tuple[float, float]) -> Tuple[float, float]:
    return (
        (virt_pos[0] + virtual_origin_pos_shift[0]) / scale, 
        (-virt_pos[1] - virtual_origin_pos_shift[1]) / scale
    )

def virtual_size():
    return (
        abs(screen_to_virtual_coords((800, 800))[0] - screen_to_virtual_coords((0, 0))[0]),
        abs(screen_to_virtual_coords((800, 800))[1] - screen_to_virtual_coords((0, 0))[1]),
    )

def zoom(cursor_pos: Tuple[float, float], zoom_factor: float):
    global scale, virtual_origin_pos_shift
    
    # Convert cursor position to virtual coordinates
    cursor_virtual = screen_to_virtual_coords(cursor_pos)

    past_pos = copy.deepcopy(virtual_origin_pos_shift)

    mouse_normalized = (cursor_pos[0] / 800.0, cursor_pos[1] / 800.0)

    virtual_origin_pos_shift[0] -= virtual_size()[0]*mouse_normalized[0]
    virtual_origin_pos_shift[1] += virtual_size()[1]*mouse_normalized[1]

    scale = scale * zoom_factor

    virtual_origin_pos_shift[0] += virtual_size()[0]*mouse_normalized[0]
    virtual_origin_pos_shift[1] -= virtual_size()[1]*mouse_normalized[1]


    # screen_width_in_virual_units_before_scale = \
    #     screen_to_virtual_coords((800, 800))[0] - screen_to_virtual_coords((0, 0))[0]
    
    # scale = scale * zoom_factor

    # screen_width_in_virual_units_after_scale = \
    #     screen_to_virtual_coords((800, 800))[0] - screen_to_virtual_coords((0, 0))[0]
    
    # delta_width = screen_width_in_virual_units_after_scale - screen_width_in_virual_units_before_scale
    # print(delta_width)
    # virtual_origin_pos_shift[0] += delta_width/2
    # virtual_origin_pos_shift[1] -= delta_width/2

    # utils.scale /= 1.01
    # rect_change = utils.screen_to_virtual_coords((800, 800))[0] - buf_width
    # print (rect_change)

    # Update scale
    
    # if cursor_virtual[0] >= 0:
    #     virtual_origin_pos_shift[0] += 1.0
    
    # # Calculate the new virtual origin shift to zoom in/out at the cursor position
    # virtual_origin_pos_shift[0] += (cursor_virtual[0] - virtual_origin_pos_shift[0]) * (1 - zoom_factor)
    # virtual_origin_pos_shift[1] += (cursor_virtual[1] - virtual_origin_pos_shift[1]) * (1 - zoom_factor)
    
    # # Update the scale
    # scale = new_scale

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

def normalize_dataset(points: list[Tuple[float, float]]):
    """ Normalizes dataset to [0, 1] range. """

    x_values = [x for x, y in points]
    y_values = [y for x, y in points]

    min_x = min(x_values)
    max_x = max(x_values)

    min_y = min(y_values)
    max_y = max(y_values)

    normalized_points = [
        (
            (x - min_x) / (max_x - min_x),
            (y - min_y) / (max_y - min_y)
        )
        for x, y in points
    ]
    return normalized_points
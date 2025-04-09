""" Useful math functions """

import math


def move_dir(angle, speed):
    """ Moves object in specific direction """

    return [math.cos(deg_to_rad(angle)) * speed, math.sin(deg_to_rad(angle)) * speed]


def lerp(start, end, t):
    """ Interpolate between two values for specific time """

    return start + t * (end - start)


def touched_up(y1: int, height1: int, y2: int) -> bool:  # height2
    """ Checks if one object is touching up of other object """

    # if y1 < (y2 - height2) < (y1 + height1):
    if y1 > y2 + height1:
        return True


def touched_down(y1: int, height1: int, y2: int, height2: int) -> bool:
    """ Checks if one object is touching down of other object """

    # if y2 < (y1 + height1) < (y2 + height2):
    if y1 + height1 < y2 + height2:
        return True


def touched_left(x1: int, width1: int, x2: int, width2: int) -> bool:
    """ Checks if one object is touching left of other object """

    if x2 < (x1 - width1) < (x2 + width2):
        return True


def touched_right(x1: int, width1: int, x2: int, width2: int) -> bool:
    """ Checks if one object is touching right of other object """

    if x2 < (x1 + width1) < (x2 + width2):
        return True


def line_circle_intersection(line_start, line_end, circle_center, circle_radius):
    """Finds intersection points between a line segment and a circle"""

    # Extract points
    x1, y1 = line_start
    x2, y2 = line_end
    cx, cy = circle_center
    r = circle_radius

    # Vector from start to end of the line
    dx = x2 - x1
    dy = y2 - y1

    # Vector from start of the line to the circle's center
    fx = x1 - cx
    fy = y1 - cy

    # Quadratic equation coefficients
    a = dx ** 2 + dy ** 2
    b = 2 * (fx * dx + fy * dy)
    c = fx ** 2 + fy ** 2 - r ** 2

    # Discriminant of the quadratic equation
    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        return None  # No intersection

    # Compute the parameter `t` for the intersection points
    discriminant_sqrt = math.sqrt(discriminant)
    t1 = (-b - discriminant_sqrt) / (2 * a)
    t2 = (-b + discriminant_sqrt) / (2 * a)

    # Store intersection points
    # intersection_points = []

    # Check if t1 lies within the segment [0, 1]
    if 0 <= t1 <= 1:
        return [x1 + t1 * dx, y1 + t1 * dy]

    # Check if t2 lies within the segment [0, 1]
    if 0 <= t2 <= 1:
        return [x1 + t2 * dx, y1 + t2 * dy]

    # Return the intersection points if any, otherwise None
    return None


def line_line_intersection(p1, p2, p3, p4):
    """ Detects collision between two lines """

    # Calculate intersection using determinant math
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        return False  # Lines are parallel or coincident

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

    return 0 <= t <= 1 and 0 <= u <= 1


def line_rect_intersection(line_start, line_end, rect_pos, rect_size):
    """ Detects collision between line and rectangle """

    rect_x, rect_y = rect_pos
    rect_w, rect_h = rect_size

    # Define the rectangle's edges as lines
    rect_lines = [
        ((rect_x, rect_y), (rect_x + rect_w, rect_y)),  # Top
        ((rect_x, rect_y), (rect_x, rect_y + rect_h)),  # Left
        ((rect_x + rect_w, rect_y), (rect_x + rect_w, rect_y + rect_h)),  # Right
        ((rect_x, rect_y + rect_h), (rect_x + rect_w, rect_y + rect_h)),  # Bottom
    ]

    # Check for intersection with each edge of the rectangle
    for edge_start, edge_end in rect_lines:
        if line_line_intersection(line_start, line_end, edge_start, edge_end):
            return True

    return False


def collision(pos1, size1, pos2, size2):
    """ 2D rectangles collision check """

    return (
            pos1[0] < pos2[0] + size2[0] and  # Left edge of the first rect is to the left of the right edge of the second rect
            pos1[0] + size1[0] > pos2[0] and  # Right edge of the first rect is to the right of the left edge of the second rect
            pos1[1] < pos2[1] + size2[1] and  # Top edge of the first rect is above the bottom edge of the second rect
            pos1[1] + size1[1] > pos2[1]  # Bottom edge of the first rect is below the top edge of the second rect
    )


def touched(x1: int, weight1: int, x2: int, weight2: int, y1: int, height1: int, y2: int, height2: int) -> bool:
    """ Checks if one object is touching other object """

    if (x1 <= x2 <= (x1 + weight1) and y1 <= y2 <= (y1 + height1)) or (
            x1 <= (x2 + weight2) and (x1 + weight1) >= x2 and y1 <= (y2 + height2) and (y1 + height1) >= y2):
        return True
    else:
        return False


def deg_to_rad(degree: float) -> float:
    """ Converts degrees to radians """

    return degree * math.pi / 180


def rad_to_deg(radian: float) -> float:
    """ Converts radians to degrees """

    return radian * 180 / math.pi


def rgb_to_hex(r=0, g=0, b=0) -> str:
    """ Converts rgb value to hex value """

    return "#" + str(hex(r))[2:].rjust(2, "0").upper() + str(hex(g))[2:].rjust(2, "0").upper() + str(hex(b))[2:].rjust(
        2, "0").upper()


def distance(pos1=None, pos2=None) -> float:
    """ Gets distance between two positions using Pythagorean theorem """

    if pos1 is None:
        pos1 = [0, 0]
    if pos2 is None:
        pos2 = [500, 500]

    x_distance = pos1[0] - pos2[0]
    y_distance = pos1[1] - pos2[1]
    distance = pow(x_distance ** 2 + y_distance ** 2, 0.5)
    return distance


def rotate_to_cord(pos1=None, pos2=None) -> float:
    """
    :param pos1: pos of the object that must be turned
    :param pos2: pos of the object to turn to
    :return: angle to turn to face to given position
    """

    if pos1 is None:
        pos1 = [0, 0]
    if pos2 is None:
        pos2 = [500, 500]

    x_distance = pos1[0] - pos2[0]
    y_distance = pos1[1] - pos2[1]
    try:
        angle = math.atan(x_distance / y_distance)
        angle = rad_to_deg(angle)
        if pos1[1] > pos2[1]:
            return angle + 180
        else:
            return angle
    except ZeroDivisionError:
        return 0


def add_brightness(color: list, value: int) -> list:
    """ Adds brightness to given color """

    r, g, b = color
    r += value
    g += value
    b += value
    if r > 255:
        err = r - 255
        g += err // 2
        b += err // 2
    if g > 255:
        err = g - 255
        r += err // 2
        b += err // 2
    if b > 255:
        err = b - 255
        g += err // 2
        r += err // 2
    r = 255 if r > 255 else r
    g = 255 if g > 255 else g
    b = 255 if b > 255 else b
    return [r, g, b]


def sub_brightness(color: list, value: int) -> list:
    """ Subtracts brightness to given color """

    r, g, b = color
    r -= value
    g -= value
    b -= value
    r = 0 if r < 0 else r
    g = 0 if g < 0 else g
    b = 0 if b < 0 else b
    return [r, g, b]


def check_value(c: int):
    """ Checks if value is from 0 to 255 """

    if c > 255:
        return 255
    if c < 0:
        return 0
    return c

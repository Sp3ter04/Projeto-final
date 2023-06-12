from math import sqrt
from graphics import *


def get_distance(p1, p2):
    delta_x = p1.getX() - p2.getX()
    delta_y = p1.getY() - p2.getY()
    distance = sqrt(delta_x**2 + delta_y**2)
    return delta_x, delta_y, distance

def circle_circle_interception(p1, radius1, p2, radius2, tolerance=0):
    if sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1])**2) <= radius1 + radius2 + tolerance:
        return True
    else:
        return False


def circle_square_interception(p1, width, p2, radius, tolerance=0):
    interception_points = []
    for point in [p1, (p1[0] + width, p1[1]), (p1[0], p1[1] + width),
                  (p1[0] + width, p1[1] + width)]:
        if get_distance(Point(point[0], point[1]), Point(p2[0], p2[1]))[2] <= radius + tolerance:
            interception_points.append(point)

    if len(interception_points) != 0:
        return True
    else:
        return False


def square_square_interception(p1, width_1, p2, width_2, tolerance=0):
    interception_points = []
    tolerance = tolerance / 2
    square_1_corners = [p1, (p1[0], p1[1] + width_1),
                        (p1[0] + width_1, p1[1] + width_1), (p1[0] + width_1, p1[1])]
    for point in square_1_corners:
        if p2[0] - tolerance <= point[0] <= p2[0] + width_2 + tolerance \
                and p2[1] - tolerance <= point[1] <= p2[1] + width_2 + tolerance:
            interception_points.append(point)

    if len(interception_points) != 0:
        return True
    else:
        return False
    
def display_error_message(message, win):
    outer_rectangle = Rectangle(Point(30, 88), Point(70, 100))
    outer_rectangle.setFill(color_rgb(184, 162, 125))
    inner_rectangle = Rectangle(Point(32, 90), Point(68, 98))
    inner_rectangle.setFill(color_rgb(217, 202, 165))
    error_message = Text(Point(50, 94), message)
    error_message.setFace("times roman")
    error_message.setStyle("bold")
    error_message.setSize(14)
    error_message.setTextColor(color_rgb(65, 66, 69))
    error_box = [outer_rectangle, inner_rectangle, error_message]
    for entity in error_box:
        entity.draw(win)
    time.sleep(0.8)
    for entity in error_box:
        entity.undraw()

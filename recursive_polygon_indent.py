# recursive_polygon_indent.py
# Question 3 – Recursive geometric pattern with turtle (inward “V” indentation)

import math
import turtle as T

# ---------- Core recursive rule ----------
def indent_edge(length: float, depth: int):
    """
    Replace one edge with four edges (length/3 each) where the middle third
    becomes two sides of an equilateral triangle pointing inward.

    For inward indentation while tracing the polygon counter-clockwise:
      turn sequence = left 60, right 120, left 60
    """
    if depth == 0:
        T.forward(length)
        return

    seg = length / 3.0
    indent_edge(seg, depth - 1)
    T.left(60)          # start the inward notch
    indent_edge(seg, depth - 1)
    T.right(120)        # tip of the notch
    indent_edge(seg, depth - 1)
    T.left(60)          # finish the notch
    indent_edge(seg, depth - 1)

# ---------- Draw the whole polygon ----------
def draw_pattern(sides: int, side_len: float, depth: int):
    # Speed up drawing
    T.tracer(False)
    T.hideturtle()
    T.speed(0)
    T.pensize(1)

    # Try to center the polygon on screen
    # (place the turtle at the leftmost vertex and face right)
    angle_ext = 360.0 / sides
    R = side_len / (2 * math.sin(math.pi / sides))  # circumradius (approx. for depth 0)
    T.penup()
    T.goto(-side_len/2.0, -R * 0.35)   # a comfy offset so deeper levels don't clip
    T.setheading(0)                    # face east
    T.pendown()

    # Trace the polygon CCW so “left 60, right 120, left 60” points inward
    for _ in range(sides):
        indent_edge(side_len, depth)
        T.left(angle_ext)

    T.tracer(True)

# ---------- User input ----------
def read_int(prompt, min_val=1):
    while True:
        try:
            v = int(input(prompt))
            if v >= min_val:
                return v
        except ValueError:
            pass
        print(f"Please enter an integer ≥ {min_val}.")

def read_float(prompt, min_val=1.0):
    while True:
        try:
            v = float(input(prompt))
            if v >= min_val:
                return v
        except ValueError:
            pass
        print(f"Please enter a number ≥ {min_val}.")

if __name__ == "__main__":
    print("Recursive Polygon Indentation (turtle)\n")
    n_sides = read_int("Enter the number of sides: ", 3)   # regular polygon needs ≥ 3
    side_len = read_float("Enter the side length (pixels): ", 10.0)
    depth    = read_int("Enter the recursion depth: ", 0)

    screen = T.Screen()
    screen.title(f"Recursive Polygon – sides={n_sides}, length={side_len}, depth={depth}")

    draw_pattern(n_sides, side_len, depth)

    print("\nDone. Close the window or click in it to exit.")
    T.exitonclick()

import math
import random
import tkinter as tk
from dataclasses import dataclass


@dataclass(frozen=True)
class Point3D:
    x: float
    y: float
    z: float

    def distance_to(self, other):
        return math.sqrt(squared_distance(self, other))

    def __sub__(self, other):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar):
        return Point3D(self.x * scalar, self.y * scalar, self.z * scalar)

    __rmul__ = __mul__

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Point3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def octant(self):
        if self.x == 0 or self.y == 0 or self.z == 0:
            return "On an axis plane"
        signs = "".join("+" if value > 0 else "-" for value in (self.x, self.y, self.z))
        octants = {
            "+++": "I", "-++": "II", "--+": "III", "+-+": "IV",
            "++-": "V", "-+-": "VI", "---": "VII", "+--": "VIII",
        }
        return f"Octant {octants[signs]} ({signs})"


class AABB:
    def __init__(self, minimum, maximum):
        if any(a > b for a, b in zip(
                (minimum.x, minimum.y, minimum.z),
                (maximum.x, maximum.y, maximum.z))):
            raise ValueError("Each AABB minimum coordinate must be <= its maximum.")
        self.minimum = minimum
        self.maximum = maximum

    def contains(self, point):
        return all(low <= value <= high for low, value, high in zip(
            (self.minimum.x, self.minimum.y, self.minimum.z),
            (point.x, point.y, point.z),
            (self.maximum.x, self.maximum.y, self.maximum.z)))

    def intersects_sphere(self, sphere):
        closest = Point3D(
            clamp(sphere.center.x, self.minimum.x, self.maximum.x),
            clamp(sphere.center.y, self.minimum.y, self.maximum.y),
            clamp(sphere.center.z, self.minimum.z, self.maximum.z),
        )
        return squared_distance(closest, sphere.center) <= sphere.radius ** 2

    def intersects(self, other):
        return (
            self.minimum.x <= other.maximum.x and self.maximum.x >= other.minimum.x
            and self.minimum.y <= other.maximum.y and self.maximum.y >= other.minimum.y
            and self.minimum.z <= other.maximum.z and self.maximum.z >= other.minimum.z
        )


class Sphere3D:
    def __init__(self, center, radius):
        if radius < 0:
            raise ValueError("Sphere radius must be non-negative.")
        self.center = center
        self.radius = radius

    def contains_point(self, point):
        return squared_distance(self.center, point) <= self.radius * self.radius

    def intersects(self, other):
        radius_sum = self.radius + other.radius
        return squared_distance(self.center, other.center) <= radius_sum * radius_sum


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def squared_distance(a, b):
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2


def euclidean_distance(a, b):
    return math.sqrt(squared_distance(a, b))


def manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def chebyshev_distance(a, b):
    return max(abs(a.x - b.x), abs(a.y - b.y), abs(a.z - b.z))

def complete_square_sphere(linear_terms, constant):
    center = Point3D(*(-value / 2 for value in linear_terms))
    radius_squared = sum(value * value for value in (
        center.x, center.y, center.z)) - constant
    return center, math.sqrt(radius_squared), radius_squared


def project(point, origin, scale=48):
    return (origin[0] + (point.x - point.z * 0.45) * scale,
            origin[1] - (point.y - point.z * 0.35) * scale)


def make_random_objects(count=100):
    random.seed(3)
    objects = []
    for _ in range(count):
        center = Point3D(random.uniform(-10, 10),
                         random.uniform(-10, 10),
                         random.uniform(-10, 10))
        radius = random.uniform(0.4, 1.4)
        sphere = Sphere3D(center, radius)
        box = AABB(
            Point3D(center.x - radius, center.y - radius, center.z - radius),
            Point3D(center.x + radius, center.y + radius, center.z + radius),
        )
        objects.append((sphere, box))
    return objects


def main():
    box = AABB(Point3D(-2, -2, -2), Point3D(2, 2, 2))
    points = [
        Point3D(0, 0, 0), Point3D(3, 0.5, 0),
        Point3D(-1, 2, 1), Point3D(1, -1, 1.5),
    ]
    sphere_a = Sphere3D(Point3D(-1.5, 0, 0), 0.9)
    sphere_b = Sphere3D(Point3D(-0.1, 0, 0), 0.7)
    sphere_c = Sphere3D(Point3D(3.5, 0, 0), 0.8)
    distance_a, distance_b = Point3D(1, 2, 3), Point3D(4, 6, 8)
    random_objects = make_random_objects()
    sphere_pairs = 0
    aabb_pairs = 0
    for i in range(len(random_objects)):
        for j in range(i + 1, len(random_objects)):
            if random_objects[i][0].intersects(random_objects[j][0]):
                sphere_pairs += 1
            if random_objects[i][1].intersects(random_objects[j][1]):
                aabb_pairs += 1

    root = tk.Tk()
    root.title("Activity 3 - 3D Geometry and Spatial Bounding Volumes")
    window_height = min(840, root.winfo_screenheight() - 80)
    root.geometry(f"980x{window_height}")
    root.minsize(940, 700)
    tk.Label(root, text="Activity 3: 3D Geometry and Bounding Volumes",
             font=("Arial", 15, "bold")).pack(pady=8)

    canvas = tk.Canvas(root, width=930, height=280, bg="white")
    canvas.pack(padx=20, pady=5)
    origin = (460, 140)
    corners = [Point3D(x, y, z) for x, y, z in [
        (-2, -2, -2), (2, -2, -2), (2, 2, -2), (-2, 2, -2),
        (-2, -2, 2), (2, -2, 2), (2, 2, 2), (-2, 2, 2),
    ]]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6),
             (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    for start, end in edges:
        canvas.create_line(*project(corners[start], origin), *project(corners[end], origin),
                           fill="gray", width=2)
    for index, point in enumerate(points):
        px, py = project(point, origin)
        inside = box.contains(point)
        color = "green" if inside else "red"
        canvas.create_oval(px - 5, py - 5, px + 5, py + 5, fill=color)
        canvas.create_text(px + 9, py - 8, text=f"P{index + 1}", anchor="w",
                           fill=color, font=("Arial", 9))
    canvas.create_text(18, 18, anchor="nw", text="AABB: [-2, 2] x [-2, 2] x [-2, 2]",
                       fill="black", font=("Arial", 11, "bold"))
    canvas.create_text(18, 250, anchor="nw", text="Green: inside    Red: outside",
                       fill="black", font=("Arial", 9))

    p, q = Point3D(2, -1, 7), Point3D(1, -3, 5)
    sphere_center, sphere_radius, radius_squared = complete_square_sphere((4, -6, 2), 6)
    rows = ["Vector operations:"]
    rows.append(f"P - Q = {p - q}    P + Q = {p + q}")
    rows.append(f"P dot Q = {p.dot(q)}    P cross Q = {p.cross(q)}")
    rows.append(f"P octant: {p.octant()}    Distance P(2,-1,7) to Q(1,-3,5): "
                f"{p.distance_to(q):.1f}")
    rows.extend([
        "",
        f"(x + 2)^2 + (y - 3)^2 + (z + 1)^2 = {radius_squared:g}",
        f"Sphere center={sphere_center}, radius={sphere_radius:.3f}",
        f"Random 3D broad phase ({len(random_objects)} objects):",
        f"Sphere intersections: {sphere_pairs}    AABB overlaps: {aabb_pairs}",
        "",
        "Point                   Inside AABB",
    ])
    for index, point in enumerate(points):
        rows.append(f"P{index + 1} {str(point):25} {box.contains(point)}")
    rows.extend([
        "",
        f"Sphere A intersects B: {sphere_a.intersects(sphere_b)}"
        f"    Sphere A intersects C: {sphere_a.intersects(sphere_c)}",
        f"Sphere A intersects AABB: {box.intersects_sphere(sphere_a)}",
        "",
        f"Distance {distance_a} -> {distance_b}:",
        f"  Euclidean (L2)  = {euclidean_distance(distance_a, distance_b):.3f}",
        f"  Manhattan (L1)  = {manhattan_distance(distance_a, distance_b):.3f}",
        f"  Chebyshev (L∞)  = {chebyshev_distance(distance_a, distance_b):.3f}",
    ])
    tk.Label(root, text="\n".join(rows), justify="left", anchor="w",
             font=("Courier", 10)).pack(fill="x", padx=34, pady=4)
    print("Distance Example 3:", p.distance_to(q))
    print("Sphere Example 5:", sphere_center, sphere_radius)
    print(f"100-object broad phase: {sphere_pairs} sphere pairs; {aabb_pairs} AABB pairs")
    root.mainloop()


if __name__ == "__main__":
    main()

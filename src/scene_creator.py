from argparse import ArgumentParser
from pathlib import Path
from typing import Callable

import jsonpickle

from src.components.camera import Camera
from src.components.color import Color
from src.components.light import Light
from src.components.material import Material
from src.components.objects_in_space import Object, Plane, Sphere
from src.components.point import Point
from src.components.scene import Scene
from src.components.vector import Vector


def ask_continue(object_type: str) -> bool:
    """Asks the user if they want to continue."""
    while True:
        answer = input(f"Do you want to continue adding {object_type}? [y/n] ")
        if answer.lower() == "y":
            return True
        elif answer.lower() == "n":
            return False
        else:
            print("Invalid answer. Please try again.")


def get_color(object_type: str) -> Color:
    """Gets the color from the user."""
    while True:
        color = input(f"Enter the color of the {object_type} (r, g, b): ")
        try:
            r, g, b = color[1:-1].split(", ")
            return Color(int(r), int(g), int(b))
        except ValueError:
            print("Invalid color. Please try again.")


def get_material(materials: dict[str, Material]) -> Material:
    """Gets the material from the user."""
    while True:
        material = input("Enter the name of the material: ")
        try:
            return materials[material]
        except KeyError:
            print("Invalid material. Please try again.")


def get_sphere(material: Material) -> Object:
    """Gets a sphere from the user."""
    while True:
        radius = float(input("Enter the radius of the sphere: "))
        center = input("Enter the center of the sphere (x, y, z): ")
        try:
            x, y, z = center[1:-1].split(", ")
            return Sphere(
                material=material,
                radius=radius,
                center=Point(float(x), float(y), float(z)),
            )
        except ValueError:
            print("Invalid center. Please try again.")


def get_plane(material: Material) -> Object:
    while True:
        normal = input("Enter the normal of the plane (x, y, z): ")
        point = input("Enter the point of the plane (x, y, z): ")
        try:
            normal_x, normal_y, normal_z = normal[1:-1].split(", ")
            point_x, point_y, point_z = point[1:-1].split(", ")
            return Plane(
                material=material,
                point=Point(float(point_x), float(point_y), float(point_z)),
                normal=Vector(float(normal_x), float(normal_y), float(normal_z)),
            )
        except ValueError:
            print("Invalid normal or point. Please try again.")


OBJECT_CREATOR_FUNCTIONS = {
    "sphere": get_sphere,
    "plane": get_plane,
}


def get_object_creator_function(object_type: str) -> Callable[[Material], Object]:
    """Gets the object creator function."""
    while True:
        object_type = input("Enter the type of the object: ").lower()
        try:
            return OBJECT_CREATOR_FUNCTIONS[object_type]
        except KeyError:
            print("Invalid object type. Please try again.")


def create_scene_materials() -> dict[str, Material]:
    """Creates the materials of the scene."""
    first_run = True
    materials: dict[str, Material] = {}
    while first_run or ask_continue("materials"):
        first_run = False
        name = input("Enter the name of the material: ")

        color = get_color("material")
        ka = float(input("Enter the ambient coefficient: "))
        kd = float(input("Enter the diffusion coefficient: "))
        ks = float(input("Enter the specular coefficient: "))
        rugosity = float(input("Enter the rugosity coefficient: "))

        materials[name] = Material(
            color=color.normalized(),
            ambient_coefficient=ka,
            diffusion_coefficient=kd,
            specular_coefficient=ks,
            rugosity_coefficient=rugosity,
            reflection_coefficient=0,
            transmission_coefficient=0,
        )

    return materials


def create_scene_objects(materials: dict[str, Material]) -> list[Object]:
    """Creates the objects of the scene."""
    first_run = True
    objects: list[Object] = []
    while first_run or ask_continue("objects"):
        first_run = False
        name = input("Enter the name of the object: ")
        material = get_material(materials)
        object_creator_function = get_object_creator_function(name)
        objects.append(object_creator_function(material))

    return objects


def create_scene_lights() -> list[Light]:
    first_run = True
    lights: list[Light] = []
    while first_run or ask_continue("lights"):
        first_run = False
        position = input("Enter the position of the light (x, y, z): ")
        color = get_color("light")
        try:
            x, y, z = position[1:-1].split(", ")
            lights.append(
                Light(
                    position=Point(float(x), float(y), float(z)),
                    color=color,
                )
            )
        except ValueError:
            print("Invalid position. Please try again.")

    return lights


def create_camera() -> Camera:
    while True:
        position = input("Enter the position of the camera (x, y, z): ")
        look_at = input("Enter the look_at of the camera (x, y, z): ")
        v_up = input("Enter the v_up of the camera (x, y, z): ")
        distance_from_screen = input("Enter the distance from the screen: ")
        vertical_resolution = input("Enter the vertical resolution: ")
        horizontal_resolution = input("Enter the horizontal resolution: ")
        try:
            pos_x, pos_y, pos_z = position[1:-1].split(", ")
            look_at_x, look_at_y, look_at_z = look_at[1:-1].split(", ")
            v_up_x, v_up_y, v_up_z = v_up[1:-1].split(", ")
            return Camera(
                position=Point(float(pos_x), float(pos_y), float(pos_z)),
                look_at=Point(float(look_at_x), float(look_at_y), float(look_at_z)),
                v_up=Vector(float(v_up_x), float(v_up_y), float(v_up_z)),
                distance_from_screen=float(distance_from_screen),
                vertical_resolution=int(vertical_resolution),
                horizontal_resolution=int(horizontal_resolution),
            )
        except ValueError:
            print("Invalid input. Please try again.")


def main():
    ap = ArgumentParser()

    ap.add_argument("destination", help="The destination of the scene file", type=Path)

    args = ap.parse_args()

    materials = create_scene_materials()
    objects = create_scene_objects(materials)
    lights = create_scene_lights()
    camera = create_camera()

    ambient_color = get_color("ambient")
    background_color = get_color("background")

    scene = Scene(
        camera=camera,
        objects=objects,
        lights=lights,
        ambient_color=ambient_color,
        background_color=background_color,
    )

    with open(args.destination, "w") as f:
        f.write(jsonpickle.encode(scene))


if __name__ == "__main__":
    main()

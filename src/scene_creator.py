from argparse import ArgumentParser
from pathlib import Path

import jsonpickle

from src.components.scene import Scene
from src.ui.camera_ui import create_camera
from src.ui.color_ui import create_color
from src.ui.light_ui import create_lights
from src.ui.material_ui import create_materials
from src.ui.objects_ui import create_scene_objects
from src.ui.transformations_ui import apply_transformation


def main():
    ap = ArgumentParser()

    ap.add_argument("destination", help="The destination of the scene file", type=Path)
    ap.add_argument(
        "-e",
        "--edit",
        help="Edit an existing scene file",
        action="store_true",
    )

    args = ap.parse_args()

    if not args.edit:
        materials = create_materials()
        objects = create_scene_objects(materials)
        lights = create_lights()
        camera = create_camera()

        ambient_color = create_color("ambient")
        background_color = create_color("background")

        scene = Scene(
            camera=camera,
            objects=objects,
            lights=lights,
            ambient_color=ambient_color,
            background_color=background_color,
        )
    else:
        with open(args.destination, "r") as f:
            scene: Scene = jsonpickle.decode(f.read())

        objects = scene.objects
        for i, obj in enumerate(objects):
            print(f"{i}: {obj}")

        while True:
            try:
                obj_index = int(input("Enter the index of the object to edit: "))
                obj = objects[obj_index]
                break
            except ValueError:
                print("Invalid index. Please try again.")
            except IndexError:
                print("Index out of bounds. Please try again.")

        objects[obj_index] = apply_transformation(obj)

    with open(args.destination, "w") as f:
        f.write(jsonpickle.encode(scene))


if __name__ == "__main__":
    main()

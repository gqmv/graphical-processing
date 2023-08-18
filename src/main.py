from argparse import ArgumentParser
from pathlib import Path

import jsonpickle

from src.renderer import render_scene


def main():
    ap = ArgumentParser()

    ap.add_argument("scene", help="The scene file", type=Path)
    ap.add_argument("destination", help="The destination of the image file", type=Path)

    args = ap.parse_args()

    with open(args.scene, "r") as f:
        scene = jsonpickle.decode(f.read())

    img = render_scene(scene=scene, multithread=True)
    img.write_ppm(args.destination.absolute())


if __name__ == "__main__":
    main()

from argparse import ArgumentParser
from pathlib import Path

import jsonpickle
import pygame as pg

from src.components.scene import Scene
from src.rendering_engine import render_scene


def main():
    ap = ArgumentParser()

    ap.add_argument("scene", help="The scene file", type=Path)

    args = ap.parse_args()

    with open(args.scene, "r") as f:
        scene: Scene = jsonpickle.decode(f.read())

    pg.init()
    screen = pg.display.set_mode(
        (scene.camera.horizontal_resolution, scene.camera.vertical_resolution)
    )
    pg.display.set_caption("Ray Tracer")

    exit_render = False
    while not exit_render:
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    exit_render = True
                    pg.quit()

                case pg.KEYDOWN:
                    match event.key:
                        case pg.K_ESCAPE:
                            exit_render = True
                            pg.quit()

                        case pg.K_w:
                            scene.camera = scene.camera.move_relative(0, 0, 1)
                        case pg.K_s:
                            scene.camera = scene.camera.move_relative(0, 0, -1)
                        case pg.K_a:
                            scene.camera = scene.camera.move_relative(-1, 0, 0)
                        case pg.K_d:
                            scene.camera = scene.camera.move_relative(1, 0, 0)
                        case pg.K_UP:
                            scene.camera = scene.camera.move_relative(0, 1, 0)
                        case pg.K_DOWN:
                            scene.camera = scene.camera.move_relative(0, -1, 0)

        img = render_scene(scene=scene, multithread=True)
        px_array = pg.PixelArray(screen)

        for x in range(scene.camera.horizontal_resolution):
            for y in range(scene.camera.vertical_resolution):
                px_array[x, y] = img.get_pixel(x, y).as_rgb()

        pg.display.update()


if __name__ == "__main__":
    main()

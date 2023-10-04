from src.components.scene import Scene
from src.rendering_engine import render_scene

scene = Scene()

img = render_scene(scene=scene, multithread=True)
img.write_ppm("test.ppm")

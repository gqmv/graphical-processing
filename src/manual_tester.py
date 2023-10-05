from src.components.camera import Camera
from src.components.light import Light
from src.components.material import Material
from src.components.objects_in_space import BezierSurface
from src.components.point import Point
from src.components.scene import Scene
from src.components.vector import Vector
from src.rendering_engine import render_scene
from src.components.color import Color

# Criando uma câmera
camera_position = Point(0, 0, 0)
camera_look_at = Point(0, 0, 1)
camera_up_vector = Vector(0, 1, 0)
camera_distance = 500
vertical_res = 500
horizontal_res = 500

camera = Camera(camera_position, camera_look_at, camera_up_vector, camera_distance, vertical_res, horizontal_res)

# Criando um objeto (superfície de Bezier)
# Cor do ouro (aproximada em RGB)
gold_color = Color(254, 254, 254)  # Um tom dourado.

# Coeficientes de propriedades do material
diffusion_coeff = 0.7        # Ouro tem uma boa difusão de luz.
specular_coeff = 0.8         # O ouro é bem brilhante.
ambient_coeff = 0.1          # Um pouco de brilho na ausência de luz direta.
reflection_coeff = 0       # Ouro reflete bem, mas não é um espelho perfeito.
transmission_coeff = 0       # O ouro não é transparente.
rugosity_coeff = 25          # Um valor mais alto para uma rugosidade menor, fazendo o brilho especular mais concentrado.

# Criando a instância do material com os valores definidos
material = Material(
    color=gold_color,
    diffusion_coefficient=diffusion_coeff,
    specular_coefficient=specular_coeff,
    ambient_coefficient=ambient_coeff,
    reflection_coefficient=reflection_coeff,
    transmission_coefficient=transmission_coeff,
    rugosity_coefficient=rugosity_coeff
)

points = [
    [Point(-1, -1, 3), Point(-1, 0, 8), Point(-1, 1, 4)],
    [Point(0, -3, 3), Point(0, 4, 8), Point(0, 2, 4)],
    [Point(-3, -1, 3), Point(3, 0, 8), Point(1, 1, 4)]
]
K1 = 15
K2 = 15

bezier_surface = BezierSurface(material, points, K1, K2)

# Criando uma luz
light_position = Point(0, 2, 0)
light_color = Color(1, 1, 1)
light = Light(light_position, light_color)

# Cores ambiente e de fundo
ambient_color = Color(0.1, 0.1, 0.1)
background_color = Color(0.5, 0.5, 0.5)

# Criando a cena
scene = Scene(camera, [bezier_surface], [light], ambient_color, background_color)

img = render_scene(scene=scene, multithread=False)
img.write_ppm("test.ppm")
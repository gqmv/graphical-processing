from src.components.material import Material
from src.ui.color_ui import create_color
from src.ui.utils import ask_continue


def get_material(materials: dict[str, Material]) -> Material:
    """Gets a material from the dictionary of materials from user input."""
    while True:
        material = input("Enter the name of the material: ")
        try:
            return materials[material]
        except KeyError:
            print("Invalid material. Please try again.")


def create_materials() -> dict[str, Material]:
    """Creates a dictionary of materials from user input."""
    first_run = True
    materials: dict[str, Material] = {}
    while first_run or ask_continue("materials"):
        first_run = False
        name = input("Enter the name of the material: ")

        color = create_color("material")
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

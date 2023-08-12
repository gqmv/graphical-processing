from src.components.color import Color


class Material:
    """Material properties of an object. This is used to define how light interacts with the object."""

    def __init__(
        self,
        color: Color,
        diffusion_coefficient: float,
        specular_coefficient: float,
        ambient_coefficient: float,
        reflection_coefficient: float,
        transmission_coefficient: float,
        rugosity_coefficient: float,
    ):
        self.color = color
        self.diffusion_coefficient = diffusion_coefficient
        self.specular_coefficient = specular_coefficient
        self.ambient_coefficient = ambient_coefficient
        self.reflection_coefficient = reflection_coefficient
        self.transmission_coefficient = transmission_coefficient
        self.rugosity_coefficient = rugosity_coefficient

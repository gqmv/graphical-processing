from src.components.color import Color
from src.components.light import Light
from src.components.vector import Vector
from src.components.point import Point


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

    def get_ambient_component(self, scene_color: Color) -> Color:
        """Returns the ambient component of the material according to phong's model."""
        return self.ambient_coefficient * scene_color * self.color

    def get_diffuse_component(
        self, light: Light, normal_at_position: Vector, hit_position: Point
    ) -> Color:
        """Returns the diffuse component of the material according to phong's model."""
        if self.color == Color(0, 0, 1):
            pass
        to_light = (light.position - hit_position).normalized()
        return (
            (light.color * self.color)
            * self.diffusion_coefficient
            * max((normal_at_position.dot_product(to_light)), 0)
        )

    def get_specular_component(
        self,
        light: Light,
        normal_at_position: Vector,
        hit_position: Point,
        spectator_position: Point,
    ) -> Color:
        """Returns the specular component of the material according to phong's model."""
        if self.specular_coefficient == 1:
            pass
        to_light = (light.position - hit_position).normalized()
        reflection_vector = (
            2 * normal_at_position * (normal_at_position.dot_product(to_light))
            - to_light
        )
        to_spectator = (spectator_position - hit_position).normalized()
        return (
            (light.color * self.color)
            * self.specular_coefficient
            * (max(reflection_vector.dot_product(to_spectator), 0))
            ** self.rugosity_coefficient
        )

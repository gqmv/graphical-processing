from typing import Generic, TypeVar

T = TypeVar("T")


class GeneralizedFuntionRegistry(Generic[T]):
    """A registry used to store functions."""

    def __init__(self):
        self.registry: dict[str, T] = {}

    def register(self, name: str):
        def decorator(func: T):
            self.registry[name] = func
            return func

        return decorator

    def get(self, name: str) -> T:
        return self.registry[name]

    def __iter__(self):
        return iter(self.registry)


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


def get_triplet(text: str) -> tuple[float, float, float]:
    """Gets a triplet of floats from user input."""
    while True:
        triplet = input(text)
        try:
            x, y, z = triplet.split(", ")
            return float(x), float(y), float(z)
        except ValueError:
            print("Invalid triplet. Please try again.")

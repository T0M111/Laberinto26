"""Patrón Flyweight — ConcreteFlyweight Oro."""
from moneda import Moneda


class Oro(Moneda):
    """Moneda de oro. Estado intrínseco: value = 10."""

    @property
    def value(self) -> int:
        return 10

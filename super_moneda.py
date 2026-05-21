"""Patrón Flyweight — ConcreteFlyweight SuperMoneda."""
from moneda import Moneda


class SuperMoneda(Moneda):
    """Super moneda. Estado intrínseco: value = 50."""

    @property
    def value(self) -> int:
        return 50

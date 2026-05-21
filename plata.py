"""Patrón Flyweight — ConcreteFlyweight Plata."""
from moneda import Moneda


class Plata(Moneda):
    """Moneda de plata. Estado intrínseco: value = 5."""

    @property
    def value(self) -> int:
        return 5

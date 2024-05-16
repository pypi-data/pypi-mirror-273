"""Module with calculations."""

from typing import TypeVar

T = TypeVar("T", int, float)


def get_sum(a: T, b: T) -> T:
    """Sum."""
    return a + b


def get_product(a: T, b: T) -> T:
    """Product."""
    return a * b


def get_quotient(a: T, b: T) -> float:
    """Quotient.

    Return quotient of a and b.
    """
    return a / b


def get_diff(a: T, b: T) -> T:
    """Difference."""
    return a - b

"""Main module of the script."""

from .calc import get_product, get_quotient, get_sum


def main() -> None:
    print(f"Product: {get_product(2, 3)}")
    print(f"Quotient: {get_quotient(2, 3)}")
    print(f"Sum: {get_sum(2, 3)}")

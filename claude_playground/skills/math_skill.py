"""
Math Skill
Provides mathematical utility functions
"""

import math


def factorial(n: int) -> int:
    """Calculate factorial of n"""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    return math.factorial(n)


def fibonacci(n: int) -> list:
    """Generate Fibonacci sequence up to n terms"""
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
    return fib_sequence[:n]


def is_prime(num: int) -> bool:
    """Check if a number is prime"""
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


if __name__ == "__main__":
    print(f"Factorial of 5: {factorial(5)}")
    print(f"Fibonacci (10 terms): {fibonacci(10)}")
    print(f"Is 17 prime? {is_prime(17)}")
    print(f"Is 18 prime? {is_prime(18)}")

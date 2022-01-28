from typing import List
from rest_framework.serializers import ValidationError

MAX_POINTS_PER_TICKET = 55


def fib_sequence(limit: int) -> List[int]:
    a, b, sequence = 0, 1, [0, 1]
    while True:
        if a > limit:
            break
        a, b = b, a + b
        sequence.append(a)
    return sequence


def valid_points_count(points: int):
    if points not in fib_sequence(MAX_POINTS_PER_TICKET):
        raise ValidationError('Improper value: must be a positive integer out of Fibonacci Sequence not '
                              f'greater than {MAX_POINTS_PER_TICKET}')

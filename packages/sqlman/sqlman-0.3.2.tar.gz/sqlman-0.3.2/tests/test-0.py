# -*- coding: utf-8 -*-

from typing import TypeVar
from enum import Enum


class Mode(Enum):
    value0 = 0
    value1 = 1
    value2 = 2


m: Mode = Mode(2)
print(type(m.value))


def demo(a=()):
    """

    Args:
        a:

    Returns:

    """
    print(type(a))


demo()

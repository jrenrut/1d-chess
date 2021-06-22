from argparse import Namespace
from dataclasses import dataclass
from typing import Optional

from .color import Color
from .piece import Piece

NOPIECE = Namespace(string=".", is_piece=False)


@dataclass
class Square:
    index: int
    color: Color
    current: Optional[Piece] = NOPIECE

    def __post_init__(self):
        if self.color.value == 0:
            self.show = "************\n*          *\n*          *\n*          *\n*          *\n*          *\n*          *\n*          *\n*          *\n*          *\n*          *\n************"
        else:
            self.show = "************\n*..........*\n*..........*\n*..........*\n*..........*\n*..........*\n*..........*\n*..........*\n*..........*\n*..........*\n*..........*\n************"

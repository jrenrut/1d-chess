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

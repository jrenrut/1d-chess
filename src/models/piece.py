from dataclasses import dataclass
from enum import Enum

from .color import Color


class PieceType(Enum):
    PAWN = "p"
    KNIGHT = "n"
    BISHOP = "b"
    ROOK = "r"
    QUEEN = "q"
    KING = "k"


@dataclass
class Piece:
    id: int
    color: Color

    is_piece = True
    steps = []
    strides = []
    can_move = True  # pieces pinned to king cannot move

    def __post_init__(self):
        if self.color.value == 0:
            self.string = self.name.value.upper()
        else:
            self.string = self.name.value.lower()


@dataclass
class Pawn(Piece):
    name = PieceType.PAWN
    has_moved = False

    def __post_init__(self):
        super().__post_init__()
        if self.color:
            self.steps = [-1, -2]
        else:
            self.steps = [1, 2]


@dataclass
class Knight(Piece):
    name = PieceType.KNIGHT
    steps = [-3, -2, 2, 3]


@dataclass
class Bishop(Piece):
    name = PieceType.BISHOP
    strides = [-2, 2]


@dataclass
class Rook(Piece):
    name = PieceType.ROOK
    has_moved = False
    strides = [-1, 1]


@dataclass
class Queen(Piece):
    name = PieceType.QUEEN
    strides = [-2, -1, 1, 2]


@dataclass
class King(Piece):
    name = PieceType.KING
    steps = [-1, 1]
    has_moved = False
    in_check = False


def get_piece(name, id):

    if name.isupper():
        color = Color.WHITE
    else:
        color = Color.BLACK

    if name.lower() == "p":
        return Pawn(id, color)
    elif name.lower() == "n":
        return Knight(id, color)
    elif name.lower() == "b":
        return Bishop(id, color)
    elif name.lower() == "r":
        return Rook(id, color)
    elif name.lower() == "q":
        return Queen(id, color)
    else:
        assert name.lower() == "k", f"Unknown piece: {name}"
        return King(id, color)

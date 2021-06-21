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
    jumps = []
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
        if self.color.value == 0:
            self.steps = [[1, 2]]
            self.show = "            \n            \n            \n            \n    PPPPP   \n   PPPPPPP  \n    PPPPP   \n     PPP    \n     PPP    \n   PPPPPPP  \n            \n            "
        else:
            self.steps = [[-1, -2]]
            self.show = "            \n            \n            \n            \n   -ppppp-  \n  -ppppppp- \n   -ppppp-  \n    -ppp-   \n    -ppp-   \n  -ppppppp- \n            \n            "


@dataclass
class Knight(Piece):
    name = PieceType.KNIGHT
    jumps = [-3, -2, 2, 3]

    def __post_init__(self):
        super().__post_init__()
        if self.color.value == 0:
            self.show = "            \n            \n            \n      NNN   \n     NNNNN  \n   NNNNNNN  \n   N  NNNN  \n      NNN   \n     NNNN   \n   NNNNNNN  \n            \n            "
        else:
            self.show = "            \n            \n            \n     -nnn-  \n    -nnnnn- \n  -nnnnnnn- \n  -n  nnnn- \n     -nnn-  \n    -nnnn-  \n  -nnnnnnn- \n            \n            "


@dataclass
class Bishop(Piece):
    name = PieceType.BISHOP
    strides = [-2, 2]

    def __post_init__(self):
        super().__post_init__()
        if self.color.value == 0:
            self.show = "            \n            \n      B     \n     BBB    \n    BBBBB   \n   BBBBBBB  \n    BBBBB   \n     BBB    \n     BBB    \n   BBBBBBB  \n            \n            "
        else:
            self.show = "            \n            \n     -b-    \n    -bbb-   \n   -bbbbb-  \n  -bbbbbbb- \n   -bbbbb-  \n    -bbb-   \n    -bbb-   \n  -bbbbbbb- \n            \n            "


@dataclass
class Rook(Piece):
    name = PieceType.ROOK
    has_moved = False
    strides = [-1, 1]

    def __post_init__(self):
        super().__post_init__()
        if self.color.value == 0:
            self.show = "            \n            \n            \n   RR R RR  \n   RRRRRRR  \n   RRRRRRR  \n   RRRRRRR  \n     RRR    \n     RRR    \n   RRRRRRR  \n            \n            "
        else:
            self.show = "            \n            \n            \n  -rr r rr- \n  -rrrrrrr- \n  -rrrrrrr- \n  -rrrrrrr- \n    -rrr-   \n    -rrr-   \n  -rrrrrrr- \n            \n            "


@dataclass
class Queen(Piece):
    name = PieceType.QUEEN
    strides = [-2, -1, 1, 2]

    def __post_init__(self):
        super().__post_init__()
        if self.color.value == 0:
            self.show = "            \n            \n     Q Q    \n   Q QQQ Q  \n   QQQQQQQ  \n   QQQQQQQ  \n    QQQQQ   \n     QQQ    \n     QQQ    \n   QQQQQQQ  \n            \n            "
        else:
            self.show = "            \n            \n    -q q-   \n  -q qqq q- \n  -qqqqqqq- \n  -qqqqqqq- \n   -qqqqq-  \n    -qqq-   \n    -qqq-   \n  -qqqqqqq- \n            \n            "


@dataclass
class King(Piece):
    name = PieceType.KING
    has_moved = False
    in_check = False

    def __post_init__(self):
        super().__post_init__()
        if self.color.value == 0:
            self.steps = [[-1], [1, 2]]
            self.show = "            \n            \n     KKK    \n   KKKKKKK  \n     KKK    \n   KKKKKKK  \n    KKKKK   \n     KKK    \n     KKK    \n   KKKKKKK  \n            \n            "
        else:
            self.steps = [[-1, -2], [1]]
            self.show = "            \n            \n    -kkk-   \n  -kkkkkkk- \n    -kkk-   \n  -kkkkkkk- \n   -kkkkk-  \n    -kkk-   \n    -kkk-   \n  -kkkkkkk- \n            \n            "


def make_piece(name, id):

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

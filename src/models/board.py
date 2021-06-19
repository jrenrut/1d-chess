from argparse import Namespace
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from . import piece

NOPIECE = Namespace(string=".")


class SquareColor(Enum):
    WHITE = 0
    BLACK = 1


@dataclass
class Square:
    index: int
    color: SquareColor
    current: Optional[piece.Piece] = NOPIECE


class Board:
    def __init__(
        self,
        size=16,
        placement="kqrbnp",
        mirror_placement=True,
        read_colors=False,
    ):

        self.size = size
        self.board = [
            Square(i, SquareColor.WHITE) if i % 2 else Square(i, SquareColor.BLACK)
            for i in range(size)
        ]

        if mirror_placement:
            assert len(placement) <= self.size / 2, "Cannot fit pieces on board."
            n_start = len(placement)
            empty = "." * (self.size - (2 * n_start))
            placement = deepcopy(placement).upper() + empty + deepcopy(placement)[::-1]
        else:
            assert len(placement) == self.size, "Cannot fit pieces on board."

        self.update(placement)

    def update(self, placement):

        self.placement = deepcopy(placement)

        piece_id = 0
        for i, (piece_) in enumerate(placement):
            if piece_ != ".":
                self.board[i].current = piece.get_piece(piece_, piece_id)
                piece_id += 1

    def __getitem__(self, index):
        return self.board[index]

    @property
    def ctn(self):
        return "".join([square.current.string for square in self.board])


def parse_ctn(ctn):
    placement, active, castling, en_passent, halfmove, fullmove = ctn.split(" ")

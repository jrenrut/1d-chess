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
        self, size=16, positions=["k", "q", "r", "b", "n", "p"], mirror_positions=True
    ):

        self.board = [
            Square(i, SquareColor.WHITE) if i % 2 else Square(i, SquareColor.BLACK)
            for i in range(size)
        ]

        if mirror_positions:
            assert len(positions) <= size / 2, "Cannot fit pieces on board."
            n_start = len(positions)
            empty = [""] * (size - (2 * n_start))
            positions = deepcopy(positions) + empty + deepcopy(positions)[::-1]
            colors = (
                [piece.PieceColor.WHITE] * n_start
                + empty
                + [piece.PieceColor.BLACK] * n_start
            )
        else:
            assert len(positions) == size, "Cannot fit pieces on board."
            if "" in positions:
                n_start = positions.index("")
            else:  # no empty spaces
                n_start = size / 2
            colors = (
                [piece.PieceColor.WHITE] * n_start + empty + [piece.PieceColor.BLACK]
            )

        self.start_positions = deepcopy(positions)

        piece_id = 0
        for i, (position, color) in enumerate(zip(positions, colors)):
            if position:
                self.board[i].current = piece.get_piece(position, piece_id, color)
                piece_id += 1

    def __getitem__(self, index):
        return self.board[index]

    @property
    def ctn(self):
        return "".join([square.current.string for square in self.board])


def parse_ctn(ctn):
    positions, active, halfmove, fullmove = ctn.split(" ")

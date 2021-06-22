from copy import deepcopy

from .color import Color
from .piece import make_piece
from .square import Square


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
            Square(i, Color.WHITE) if i % 2 else Square(i, Color.BLACK)
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
                self.board[i].current = make_piece(piece_, piece_id)
                piece_id += 1

    def update_piece(self, index, new_piece):

        self.board[index].current = new_piece

    def __getitem__(self, index):
        return self.board[index]

    @property
    def ctn(self):
        return "".join([square.current.string for square in self.board])

    @property
    def show(self):
        lines = [""] * 12
        count = 1
        for square in self.board:
            if square.current.is_piece:
                square_show = "".join(
                    [
                        p if p != " " else s
                        for p, s in zip(square.current.show, square.show)
                    ]
                )
            else:
                square_show = square.show
            square_show = square_show.split("\n")
            for i in range(12):
                if count == self.size:
                    lines[i] += square_show[i] + "\n"
                else:
                    lines[i] += square_show[i]
            count += 1
        board_show = "".join(lines)
        print(board_show)


def parse_ctn(ctn):
    placement, active, castling, en_passent, halfmove, fullmove = ctn.split(" ")

from .board import Board


class Game:
    def __init__(
        self, size=16, positions=["k", "q", "r", "b", "n", "p"], mirror_positions=True
    ):

        self.board = Board(size, positions=positions, mirror_positions=mirror_positions)

        self.active = "w"
        # TODO assumes king will always be behind rook in initial placement. Okay?
        if "r" in positions and positions.index("r") - positions.index("k") >= 3:
            self.castling = "Kk"
        else:
            self.castling = "-"
        self.en_passant = "-"
        self.halfmove = 0
        self.fullmove = 1

    @property
    def ctn(self):

        return " ".join(
            [
                self.board.ctn,
                self.active,
                self.castling,
                self.en_passant,
                str(self.halfmove),
                str(self.fullmove),
            ]
        )

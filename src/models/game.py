from .board import Board


class Game:
    def __init__(self, size=16, placement="kqrbnp", mirror_placement=True):

        self.board = Board(size, placement=placement, mirror_placement=mirror_placement)

        self.placement = self.board.placement
        self.active = "w"
        #  assumes king will always be behind rook in initial placement. Okay?
        if "r" in placement and placement.index("r") - placement.index("k") >= 3:
            self.castling = "Kk"
        else:
            self.castling = "-"
        self.en_passant = "-"
        self.halfmove = 0
        self.fullmove = 1

    def update(self, ctn):
        (
            self.placement,
            self.active,
            self.castling,
            self.en_passant,
            self.halfmove,
            self.fullmove,
        ) = ctn.split(" ")
        self.board.update(self.placement)

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

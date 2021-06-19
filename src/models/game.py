from .board import Board
from .player import Player


class Game:
    def __init__(self, size=16, placement="kqrbnp", mirror_placement=True):

        self.size = size

        self.board = Board(size, placement=placement, mirror_placement=mirror_placement)
        self.squares = self.board.board

        white_pieces, black_pieces = [], []
        for square in self.squares:
            piece = square.current
            if not piece.is_piece:
                continue
            if piece.color.value == 0:
                white_pieces.append(piece)
            else:
                black_pieces.append(piece)
        self.white = Player(white_pieces)
        self.black = Player(black_pieces)

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

    def apply_move(self, start, end):

        assert start < self.size, f"Start position off board: {start}"
        assert end < self.size, f"End position off board: {end}"

        start_square = self.board[start]
        assert start_square.current.is_piece, "No piece on start square."

        # end_square = self.board[end]

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

from copy import deepcopy

from .board import Board
from .color import Color
from .player import Player


class Game:
    def __init__(self, size=16, placement="kqrbnp", mirror_placement=True):

        self.size = size

        self.board = Board(size, placement=placement, mirror_placement=mirror_placement)
        self.squares = self.board.board

        self.update_players(self.squares)

        self.placement = self.board.placement
        self.active = "w"
        self.active_color = Color.WHITE
        #  assumes king will always be behind rook in initial placement. Okay?
        if "r" in placement and placement.index("r") - placement.index("k") >= 3:
            self.castling = "Kk"
        else:
            self.castling = "-"
        self.en_passant = "-"
        self.halfmove = 0
        self.fullmove = 0

    def checkmate(self):

        return

    def update(self, ctn):
        (
            self.placement,
            self.active,
            self.castling,
            self.en_passant,
            self.halfmove,
            self.fullmove,
        ) = ctn.split(" ")
        if self.active == "w":
            self.active_color = Color.WHITE
        else:
            self.active_color = Color.BLACK
        self.board.update(self.placement)
        self.squares = self.board.board

    def update_players(self, squares):

        white_pieces, black_pieces = [], []
        for square in squares:
            if not square.current.is_piece:
                continue
            if square.current.color.value == 0:
                white_pieces.append(square)
            else:
                black_pieces.append(square)

        if self.active == "w":
            self.player = Player(white_pieces)
            self.opponent = Player(black_pieces)
        else:
            self.player = Player(black_pieces)
            self.opponent = Player(white_pieces)

    def update_moves(self):

        self.player_moves = {}
        self.opponent_moves = {}
        self.checks = []  # format: [opponent_square, [intermediate_squares]]
        for square in self.squares:
            piece = square.current
            if not piece.is_piece:
                continue
            if not piece.can_move:
                continue
            color = piece.color
            moves = []
            if piece.steps:
                # list of lists because king can move forward or backward
                for steps in piece.steps:
                    for step in steps:
                        try:
                            attack_square = self.squares[square.index + step]
                        except IndexError:
                            break
                        if attack_square.current.is_piece:
                            if attack_square.current.color == color:
                                break
                            else:
                                moves.append(attack_square.index)
                                if attack_square.current.name.value == "k":
                                    self.checks.append([square, []])
                                break
                        else:
                            moves.ppend(attack_square.index)
            elif piece.strides:
                stride_moves = []
                for stride in piece.strides:
                    i = 1
                    while True:
                        try:
                            attack_square = self.squares[square.index + stride * i]
                        except IndexError:
                            break
                        if attack_square.current.is_piece:
                            if attack_square.current.color == color:
                                break
                            else:
                                stride_moves.append(attack_square.index)
                                if attack_square.current.name.value == "k":
                                    self.checks.append([square, stride_moves])
                                break
                        else:
                            stride_moves.append(attack_square.index)
                        i += 1
                moves += stride_moves
            else:
                for jump in piece.jumps:
                    try:
                        attack_square = self.squares[square.index + jump]
                    except IndexError:
                        break
                    if attack_square.current.is_piece:
                        if attack_square.current.color == color:
                            continue
                        else:
                            moves.append(attack_square.index)
                            if attack_square.current.name.value == "k":
                                self.checks.append([square, []])
                            continue
                    else:
                        moves.ppend(attack_square.index)
            if color == self.active_color:
                self.player_moves[square] = moves
            else:
                self.opponent_moves[square] = moves

    def check_legal_moves(self, player):

        if self.checks:
            legal_moves = {}
            for player_square, attack_squares in self.player_moves.items():
                piece_moves = []
                for attack_square in attack_squares:
                    for checking_square, intermediate_squares in self.checks:
                        if attack_square == checking_square.index:
                            piece_moves.append(attack_square)
                        for intermediate_square in intermediate_squares:
                            if attack_square == intermediate_square:
                                piece_moves.append(attack_square)
                if piece_moves:
                    legal_moves[player_square] = piece_moves
            if not legal_moves:
                self.checkmate()
                return
            self.player_moves = legal_moves

    def apply_move(self, start, end):

        assert start < self.size, f"Start position off board: {start}"
        assert end < self.size, f"End position off board: {end}"

        start_square = self.board[start]
        assert start_square.current.is_piece, "No piece on start square."

        halfmove = True
        if self.board[end].current.is_piece:
            halfmove = False

        placement = [p for p in self.placement]
        placement[end] = deepcopy(placement[start])
        placement[start] = "."
        self.placement = "".join(placement)

        piece = start_square.current
        if not piece.has_moved:
            if piece.name.value == "p":
                piece.has_moved = True
                piece.steps = [piece.steps[0][0]]
                self.board.update_piece(start_square.index, piece)
                self.squares = self.board.board
                halfmove = False
                if abs(start - end) == 2:
                    self.en_passant = (start + end) / 2  # index between squares
            if piece.name.value == "r" or piece.name.value == "k":
                piece.has_moved = True
                self.board.update_piece(start_square.index, piece)
                self.squares = self.board.board
                if piece.color.value == 0:
                    letter = "K"
                else:
                    letter = "k"
                if letter in self.castling:
                    self.castling.replace(letter, "")

        if halfmove:
            self.halfmove += 1

        if self.active == "w":
            self.active = "b"
            self.fullmove += 1
        else:
            self.active = "w"

        return self.ctn

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

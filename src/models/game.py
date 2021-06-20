from copy import deepcopy

from .board import Board
from .color import Color
from .player import Player
from .square import NOPIECE


class Game:
    def __init__(self, size=16, placement="kqrbnp", mirror_placement=True):

        self.size = size

        self.board = Board(size, placement=placement, mirror_placement=mirror_placement)

        self.placement = self.board.placement
        self.active = "w"
        self.active_color = Color.WHITE
        self.castling = "-"
        if "r" in placement:
            r_indexes = [i for i, p in enumerate(placement) if p == "r"]
            for r_index in r_indexes:
                if abs(placement.index("k") - r_index) >= 3:
                    self.castling = "Kk"
        self.en_passant = "-"
        self.halfmove = "0"
        self.fullmove = "1"

        self.update_players()
        self.update_moves()
        self.ctn

    def checkmate(self):

        return

    def update(self):
        (
            self.placement,
            self.active,
            self.castling,
            self.en_passant,
            self.halfmove,
            self.fullmove,
        ) = self.ctn.split(" ")
        if self.active == "w":
            self.active_color = Color.WHITE
        else:
            self.active_color = Color.BLACK
        self.board.update(self.placement)
        self.update_players()
        self.update_moves()

    def update_players(self):

        white_pieces, black_pieces = [], []
        for square in self.board.board:
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
        self.castle_squares = []
        for square in self.board.board:
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
                        if ((square.index + step) < 0) or (
                            (square.index + step) >= self.size
                        ):
                            break
                        attack_square = self.board[square.index + step]
                        if attack_square.current.is_piece:
                            if attack_square.current.color == color:
                                break
                            else:
                                moves.append(attack_square.index)
                                if attack_square.current.name.value == "k":
                                    self.checks.append([square, []])
                                elif (
                                    piece.name.value == "p"
                                    and not piece.has_moved
                                    and piece.steps[0][-1] + square.index
                                    == int(self.en_passant)
                                ):
                                    continue
                                break
                        else:
                            moves.append(attack_square.index)
                            if (
                                piece.color == self.active_color
                                and abs(step) == 2
                                and piece.name.value == "k"
                            ):
                                self.castle_squares = [
                                    square.index,
                                    square.index + steps[0],
                                    square.index + steps[1],
                                ]
            elif piece.strides:
                stride_moves = []
                for stride in piece.strides:
                    i = 1
                    while True:
                        if ((square.index + stride * i) < 0) or (
                            (square.index + stride * i) >= self.size
                        ):
                            break
                        attack_square = self.board[square.index + stride * i]
                        if attack_square.current.is_piece:
                            if attack_square.current.color == color:
                                break
                            else:
                                stride_moves.append(attack_square.index)
                                if attack_square.current.name.value == "k":
                                    if attack_square.index > square.index:
                                        stride_check_moves = [
                                            sm
                                            for sm in stride_moves
                                            if sm > square.index
                                        ]
                                    else:
                                        stride_check_moves = [
                                            sm
                                            for sm in stride_moves
                                            if sm < square.index
                                        ]
                                    self.checks.append([square, stride_check_moves])
                                break
                        else:
                            stride_moves.append(attack_square.index)
                        i += 1
                moves += stride_moves
            else:
                for jump in piece.jumps:
                    if ((square.index + jump) < 0) or (
                        (square.index + jump) >= self.size
                    ):
                        break
                    attack_square = self.board[square.index + jump]
                    if attack_square.current.is_piece:
                        if attack_square.current.color == color:
                            continue
                        else:
                            moves.append(attack_square.index)
                            if attack_square.current.name.value == "k":
                                self.checks.append([square, []])
                            continue
                    else:
                        moves.append(attack_square.index)
            if color == self.active_color:
                self.player_moves[square.index] = moves
            else:
                self.opponent_moves[square.index] = moves

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
            self.castle_squares = []

        if self.castle_squares:
            castle = True
            for castle_square in self.castle_squares:
                for attacked_squares in self.opponent_moves.values():
                    if castle_square in attacked_squares:
                        castle = False
            if not castle:
                king_index = self.castle_squares[0]
                del self.player_moves[king_index][-1]

    def apply_move(self, start, end):

        assert start < self.size, f"Start position off board: {start}"
        assert end < self.size, f"End position off board: {end}"

        start_square = self.board[start]
        piece = start_square.current
        assert piece.is_piece, "No piece on start square."
        assert piece.color == self.active_color, "Wrong color piece."
        assert start in self.player_moves, "Illegal move."
        assert end in self.player_moves[start], "Illegal move."

        self.board.update_piece(start, NOPIECE)

        halfmove = True
        if self.board[end].current.is_piece:
            halfmove = False

        placement = [p for p in self.placement]
        placement[end] = deepcopy(placement[start])
        placement[start] = "."
        if piece.name.value == "p":
            if not piece.has_moved:
                piece.has_moved = True
                piece.steps = [[piece.steps[0][0]]]
                self.board.update_piece(end, piece)
                halfmove = False
                if abs(start - end) == 2:
                    skipped = int((start + end) / 2)  # index between squares
                    self.en_passant = str(skipped)
                    skipped_square = self.board[skipped]
                    if skipped_square.current.is_piece:
                        self.board.update_piece(skipped, NOPIECE)
                        placement[skipped] = "."

        if piece.name.value == "r":
            if not piece.has_moved:
                piece.has_moved = True
                self.board.update_piece(end, piece)
                if piece.color.value == 0:
                    letter = "K"
                else:
                    letter = "k"
                if letter in self.castling:
                    self.castling.replace(letter, "")
                    if not self.castling:
                        self.castling = "-"

        if piece.name.value == "k":
            if not piece.has_moved:
                piece.has_moved = True
                self.board.update_piece(end, piece)
                if piece.color.value == 0:
                    letter = "K"
                else:
                    letter = "k"
                if letter in self.castling:
                    self.castling.replace(letter, "")
                    if not self.castling:
                        self.castling = "-"
            if abs(start - end) == 2:
                skipped = int((start + end) / 2)  # index between squares
                sign = int((end - start) / 2)
                index = end + 1 * sign
                while True:
                    square = self.board[index]
                    if square.current.is_piece:
                        assert square.current.name.value == "r", "Cannot castle."
                        rook = deepcopy(self.board[index].current)
                        rook.has_moved = True
                        self.board.update_piece(skipped, rook)
                        self.board.update_piece(index, NOPIECE)
                        placement[skipped] = deepcopy(placement[index])
                        placement[index] = "."
                        break
                    index += 1 * sign

        self.placement = "".join(placement)

        if halfmove:
            self.halfmove = str(int(self.halfmove) + 1)

        if self.active == "w":
            self.active = "b"
        else:
            self.active = "w"
            self.fullmove = str(int(self.fullmove) + 1)

        self.update()
        return self.ctn

    @property
    def ctn(self):

        return " ".join(
            [
                self.placement,
                self.active,
                self.castling,
                self.en_passant,
                self.halfmove,
                self.fullmove,
            ]
        )

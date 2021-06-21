from copy import deepcopy

from .player import Player


class ZeroSum(Player):
    def move(self):

        game = deepcopy(self.game)

        start, end = -1, -1
        best_balance = -1e3
        for square, attack_squares in game.player_moves.items():
            for attack_square in attack_squares:
                copy = deepcopy(game)
                copy.apply_move(square, attack_square)
                n_defended = sum(len(v) for v in copy.player_moves.values())
                n_attacking = sum(len(v) for v in copy.opponent_moves.values())
                balance = n_attacking - n_defended
                if balance > best_balance:
                    start, end = square, attack_square

        return self.game.apply_move(start, end)

import numpy as np

from .player import Player


class Random(Player):
    def move(self):

        attack_squares = []
        for square, attack_squares_ in self.game.player_moves.items():
            for attack_square in attack_squares_:
                attack_squares.append([square, attack_square])

        index = np.random.randint(0, len(attack_squares))
        start, end = attack_squares[index]

        return self.game.apply_move(start, end)

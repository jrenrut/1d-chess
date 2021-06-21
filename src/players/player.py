class Player:
    def __init__(self, game):

        self.game = game

    def move(self, start, end):

        return self.game.apply_move(start, end)

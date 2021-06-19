from .color import Color


class Player:
    def __init__(self, pieces):

        self.pieces = pieces

        if pieces[0].color.value == 0:
            self.color = Color.WHITE
        else:
            self.color = Color.BLACK

        self.king = next(piece for piece in self.pieces if piece.name.value == "k")

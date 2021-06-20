from .color import Color


class Player:
    def __init__(self, squares):

        self.squares = squares

        if squares[0].current.color.value == 0:
            self.color = Color.WHITE
        else:
            self.color = Color.BLACK

        # assumes single king
        self.king = next(
            square for square in self.squares if square.current.name.value == "k"
        )

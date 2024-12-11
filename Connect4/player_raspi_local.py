from sense_hat import SenseHat
from game import Connect4


class Player_Raspi_Local:
    """
    A local player for Raspberry Pi using Sense HAT for input and output.
    """

    def __init__(self, game: Connect4, id, sense: SenseHat):
        """
        Initialize the player.
        Parameters:
            game (Connect4): The game instance.
            id (UUID): The player's unique ID.
            sense (SenseHat): The shared Sense HAT instance.
        """
        self.game = game
        self.id = id
        self.sense = sense
        self.icon = self.game.register_player(self.id)
        self.color = [255, 0, 0] if self.icon == "X" else [0, 0, 255]

    def make_move(self):
        """
        Use the joystick to select a column and make a move.
        """
        column = 0
        self.visualize_selection(column)

        while True:
            for event in self.sense.stick.get_events():
                if event.action == "pressed":
                    if event.direction == "left" and column > 0:
                        column -= 1
                    elif event.direction == "right" and column < 7:
                        column += 1
                    elif event.direction == "middle":
                        # Attempt to make a move
                        if self.game.check_move(column, self.id):
                            return column
                        else:
                            self.sense.show_message("Invalid move!", text_colour=[255, 0, 0])
                    self.visualize_selection(column)

    def visualize_selection(self, column):
        """
        Highlight the selected column on the Sense HAT.
        """
        pixels = [[0, 0, 0] for _ in range(64)]
        for row in range(8):  # Highlight the selected column
            pixels[column + row * 8] = [255, 255, 255]
        self.sense.set_pixels(pixels)

    def visualize(self):
        """
        Display the game board on the Sense HAT LED matrix with column numbers.
        """
        board = self.game.get_board()  # Fetch the board state as a flat list
        pixels = []

        # Map the board to LED colors
        for cell in board:
            if cell == "X":
                pixels.append([255, 0, 0])  # Red for X
            elif cell == "O":
                pixels.append([0, 0, 255])  # Blue for O
            else:
                pixels.append([0, 0, 0])  # Black for empty cells

        # Add column numbers as the last row
        for col in range(8):
            pixels.append([255, 255, 255])  # White for column numbers

        self.sense.set_pixels(pixels)

    def celebrate_win(self):
        """
        Celebrate the win with an animation on the Sense HAT.
        """
        for _ in range(3):
            self.sense.clear(self.color)
            self.sense.clear()
        self.sense.show_message(f"Player {self.icon} wins!", text_colour=self.color)

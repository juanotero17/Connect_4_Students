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
        column = 0  # Start with the first column
        self.visualize_selection(column)  # Highlight the column selection

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
                            self.visualize()  # Refresh the board after the move
                            return  # Exit after a successful move
                        else:
                            self.sense.show_message("Invalid move!", text_colour=[255, 0, 0])

                    # Update the selection highlight
                    self.visualize_selection(column)

    def visualize_selection(self, column):
        """
        Highlight the selected column on the Sense HAT.
        """
        # Create a blank 8x8 grid
        pixels = [[0, 0, 0] for _ in range(64)]

        # Highlight the top row of the selected column
        for row in range(8):
            pixels[column + row * 8] = [255, 255, 255]  # White for selection

        self.sense.set_pixels(pixels)

    def visualize(self):
        """
        Display the current game board on the Sense HAT LED matrix.
        """
        board = self.game.get_board()  # Get the board as a flat list (56 elements)

        # Initialize a pixel list for the 8x8 grid
        pixels = []

        # Map each cell in the board to a color
        for cell in board:
            if cell == "X":
                pixels.append([255, 0, 0])  # Red for Player X
            elif cell == "O":
                pixels.append([0, 0, 255])  # Blue for Player O
            else:
                pixels.append([0, 0, 0])  # Black for empty cells

        # Pad the board to 64 pixels to fit the Sense HAT's 8x8 grid
        while len(pixels) < 64:
            pixels.append([0, 0, 0])  # Add blank pixels for padding

        # Send the pixel list to the Sense HAT
        self.sense.set_pixels(pixels)

    def celebrate_win(self):
        """
        Celebrate the win with an animation on the Sense HAT.
        """
        for _ in range(3):
            self.sense.clear(self.color)
            self.sense.clear()
        self.sense.show_message(f"Player {self.icon} wins!", text_colour=self.color)

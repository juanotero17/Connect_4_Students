from sense_hat import SenseHat
from game import Connect4
import time

class Player_Raspi_Local:
    """
    A local player for Raspberry Pi using Sense HAT for input and output.
    """

    def __init__(self, game, id, sense):
        """
        Initialize a local player using Sense HAT.
        """
        self.game = game
        self.id = id
        self.sense = sense
        self.icon = self.game.register_player(self.id)
        self.color = [255, 0, 0] if self.icon == "X" else [0, 0, 255]

        # Debug Sense HAT initialization
        try:
            self.sense.clear()  # Clear the Sense HAT display
            print(f"Debug: Sense HAT initialized and cleared for Player {self.icon}.")
        except Exception as e:
            print(f"Error: Could not initialize Sense HAT. {e}")

    def make_move(self):
        """
        Use the joystick to select a column and make a move.
        """
        column = 0  # Start with the first column
        self.visualize(column)  # Display the grid with the movement dot

        while True:
            for event in self.sense.stick.get_events():
                print(f"Debug: Joystick event: {event}")  # Debug joystick events
                if event.action == "pressed":
                    if event.direction == "left" and column > 0:
                        column -= 1
                    elif event.direction == "right" and column < 7:
                        column += 1
                    elif event.direction == "middle":
                        # Attempt to make a move
                        if self.game.check_move(column, self.id):
                            print(f"Debug: Player {self.icon} made a move in column {column}.")
                            self.visualize()  # Refresh the board after the move
                            return  # Exit after a successful move
                        else:
                            self.sense.show_message("Invalid move!", text_colour=[255, 0, 0])

                    # Update the grid with the movement dot
                    self.visualize(column)

                # Small debounce delay to prevent rapid movement
                time.sleep(0.2)

    def visualize(self, selected_column=None):
        """
        Display the current game board and optionally highlight the selected column on the Sense HAT LED matrix.
        """
        board = self.game.get_board()  # Fetch the board as a flat list (56 elements)
        print(f"Debug: Board state (flat list): {board}")  # Debugging board state

        pixels = [[0, 0, 0] for _ in range(64)]  # Initialize the 8x8 grid

        # Highlight the selected column with a dot at the top row
        if selected_column is not None:
            for col in range(8):
                pixels[col] = [0, 0, 0]  # Clear any existing indicator
            pixels[selected_column] = [255, 255, 255]  # White dot for selection

        # Map each cell in the board to the grid, starting from row 0
        for row in range(7):  # Start from the top row (row 0)
            for col in range(8):
                cell_index = row * 8 + col
                if board[cell_index] == "X":
                    pixels[row * 8 + col] = [255, 0, 0]  # Red for Player X
                elif board[cell_index] == "O":
                    pixels[row * 8 + col] = [0, 0, 255]  # Blue for Player O

        print(f"Debug: Pixels sent to Sense HAT: {pixels}")  # Debugging pixel data

        try:
            self.sense.set_pixels(pixels)  # Send the pixels to the Sense HAT
            time.sleep(0.1)  # Add a small delay to ensure the display updates
            print("Debug: Board updated on Sense HAT.")  # Confirmation
        except Exception as e:
            print(f"Error: Failed to update Sense HAT. {e}")

    def celebrate_win(self):
        """
        Celebrate the win with an animation on the Sense HAT.
        """
        for _ in range(3):
            self.sense.clear(self.color)
            time.sleep(0.3)
            self.sense.clear()
            time.sleep(0.3)
        self.sense.show_message(f"Player {self.icon} wins!", text_colour=self.color)

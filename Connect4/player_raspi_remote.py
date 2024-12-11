import requests
import uuid
from sense_hat import SenseHat
from player import Player  # Importing the abstract base class
import time


class Player_Raspi_Remote(Player):
    """
    A remote player for Raspberry Pi using Sense HAT for input and output.
    """

    def __init__(self, server_url):
        """
        Initialize the remote Sense HAT player.
        """
        super().__init__()  # Initialize attributes from the abstract base class
        self.server_url = server_url
        self.sense = SenseHat()

        # Initialize the Sense HAT
        try:
            self.sense.clear()
            print("Debug: Sense HAT initialized.")
        except Exception as e:
            print(f"Error: Failed to initialize Sense HAT. {e}")

    def register_in_game(self):
        """
        Register the player with the server and assign an icon.
        """
        print("Registering player...")
        response = requests.post(
            f"{self.server_url}/connect4/register",
            json={"player_id": str(self.id)},
        )
        response.raise_for_status()
        self.icon = response.json()["player_icon"]
        print(f"Player registered with icon: {self.icon}")
        return self.icon

    def is_my_turn(self):
        """
        Check if it is this player's turn.
        """
        status = self.get_game_status()
        return status["active_player"] == str(self.id)

    def get_game_status(self):
        """
        Retrieve the current game status from the server.
        """
        response = requests.get(f"{self.server_url}/connect4/status")
        response.raise_for_status()
        return response.json()

    def make_move(self):
        """
        Use the joystick to select a column and send the move to the server.
        """
        column = 0  # Start with the first column
        self.visualize(column)  # Display the current state with selection

        while True:
            for event in self.sense.stick.get_events():
                print(f"Debug: Joystick event: {event}")
                if event.action == "pressed":
                    if event.direction == "left" and column > 0:
                        column -= 1
                    elif event.direction == "right" and column < 7:
                        column += 1
                    elif event.direction == "middle":
                        # Attempt to make a move on the server
                        response = requests.post(
                            f"{self.server_url}/connect4/check_move",
                            json={"column": column, "player_id": str(self.id)},
                        )
                        if response.status_code == 200:
                            print(f"Debug: Move successful in column {column}.")
                            self.visualize()  # Refresh the board
                            return
                        else:
                            self.sense.show_message("Invalid move!", text_colour=[255, 0, 0])

                    # Update the selection highlight
                    self.visualize(column)

                # Small debounce delay to prevent rapid movement
                time.sleep(0.2)

    def visualize(self, selected_column=None):
        """
        Display the current game board and highlight the selected column on the Sense HAT.
        """
        response = requests.get(f"{self.server_url}/connect4/board")
        response.raise_for_status()
        board = response.json()["board"]

        pixels = [[0, 0, 0] for _ in range(64)]  # Initialize an 8x8 grid

        # Highlight the selected column
        if selected_column is not None:
            for col in range(8):
                pixels[col] = [0, 0, 0]
            pixels[selected_column] = [255, 255, 255]  # White for selection

        # Map the game board to the grid
        for row in range(7):
            for col in range(8):
                cell_index = row * 8 + col
                if board[cell_index] == "X":
                    pixels[(row + 1) * 8 + col] = [255, 0, 0]  # Red for Player X
                elif board[cell_index] == "O":
                    pixels[(row + 1) * 8 + col] = [0, 0, 255]  # Blue for Player O

        try:
            self.sense.set_pixels(pixels)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error: Failed to update Sense HAT. {e}")

    def celebrate_win(self):
        """
        Display a winning animation on the Sense HAT.
        """
        for _ in range(3):
            self.sense.clear([255, 255, 0])  # Yellow flash
            time.sleep(0.3)
            self.sense.clear()
            time.sleep(0.3)
        self.sense.show_message(f"Player {self.icon} wins!", text_colour=[255, 255, 0])

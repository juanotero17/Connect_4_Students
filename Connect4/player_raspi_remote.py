import requests
from sense_hat import SenseHat
from player import Player


class Player_Raspi_Remote(Player):
    """
    A remote player for Raspberry Pi using Sense HAT for input and output.
    """

    def __init__(self, server_url):
        super().__init__()  # Initialize attributes from the abstract Player class
        self.server_url = server_url
        self.sense = SenseHat()

    def register_in_game(self):
        """
        Register the player on the server and get the assigned icon.

        Returns:
            str: The player's icon.
        """
        print("Registering player...")
        response = requests.post(
            f"{self.server_url}/connect4/register",
            json={"player_id": str(self.id)},
        )
        response.raise_for_status()
        self.icon = response.json()["player_icon"]
        print(f"Player registered successfully with icon: {self.icon}")
        return self.icon

    def is_my_turn(self):
        """
        Check if it is this player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        status = self.get_game_status()
        return status["active_player"] == str(self.id)

    def get_game_status(self):
        """
        Get the game's current status.

        Returns:
            dict: The current game status from the server.
        """
        response = requests.get(f"{self.server_url}/connect4/status")
        response.raise_for_status()
        return response.json()

    def make_move(self):
        """
        Use the Sense HAT joystick to select a column for the move.

        Returns:
            int: The column chosen by the player for the move.
        """
        print("Use the joystick to select your move.")
        column = self._select_column()
        response = requests.post(
            f"{self.server_url}/connect4/check_move",
            json={"column": column, "player_id": str(self.id)},
        )
        response.raise_for_status()
        print(f"Move successful: Column {column + 1}")
        return column

    def visualize(self):
        """
        Display the current game board on the Sense HAT LED matrix.
        """
        response = requests.get(f"{self.server_url}/connect4/board")
        response.raise_for_status()
        board = response.json()["board"]
        self._display_board(board)

    def celebrate_win(self):
        """
        Display a winning animation on the Sense HAT.
        """
        print(f"Congratulations! Player {self.icon} wins!")
        self.sense.show_message("You win!", text_colour=[0, 255, 0])

    def _select_column(self):
        """
        Use the joystick to select a column.

        Returns:
            int: The selected column index.
        """
        selected = 0
        self._display_column_selector(selected)
        while True:
            for event in self.sense.stick.get_events():
                if event.action == "pressed":
                    if event.direction == "left" and selected > 0:
                        selected -= 1
                    elif event.direction == "right" and selected < self.board_width - 1:
                        selected += 1
                    elif event.direction == "middle":
                        return selected
                    self._display_column_selector(selected)

    def _display_column_selector(self, selected):
        """
        Highlight the selected column on the Sense HAT LED matrix.
        """
        matrix = [[0, 0, 0] for _ in range(64)]
        for i in range(self.board_height):  # Highlight all rows in the selected column
            matrix[selected + i * self.board_width] = [255, 255, 255]
        self.sense.set_pixels(matrix)

    def _display_board(self, board):
        """
        Display the game board on the Sense HAT LED matrix.

        Parameters:
            board (list): A flat list representing the game board state.
        """
        matrix = []
        for cell in board:
            if cell == "X":
                matrix.append([255, 0, 0])  # Red for player X
            elif cell == "O":
                matrix.append([0, 0, 255])  # Blue for player O
            else:
                matrix.append([0, 0, 0])  # Black for empty
        self.sense.set_pixels(matrix)

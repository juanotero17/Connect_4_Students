import requests
from player import Player


class Player_Remote(Player):
    """
    A remote player that interacts with a Connect4 server via REST API.
    """

    def __init__(self, server_url):
        super().__init__()  # Initialize from the abstract Player class
        self.server_url = server_url

    def register_in_game(self):
        """
        Register the player on the server and get the assigned icon.

        Returns:
            str: The player's icon.
        """
        print("Attempting to register player...")
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
        status = response.json()
        return status

    def make_move(self):
        """
        Prompt the player to make a move and send it to the server.

        Returns:
            int: The column chosen by the player for the move.
        """
        while True:
            try:
                column = int(input("Enter the column number (1-8): ")) - 1
                if 0 <= column < self.board_width:
                    response = requests.post(
                        f"{self.server_url}/connect4/check_move",
                        json={"column": column, "player_id": str(self.id)},
                    )
                    response.raise_for_status()
                    print(f"Move successful: Column {column + 1}")
                    return column
                else:
                    print(f"Column must be between 1 and {self.board_width}.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 8.")
            except requests.exceptions.RequestException as e:
                print(f"Error sending move: {e}")

    def visualize(self):
        """
        Fetch and print the current game board.
        """
        response = requests.get(f"{self.server_url}/connect4/board")
        response.raise_for_status()
        board = response.json()["board"]
        print("Current Board:")
        for i in range(0, len(board), self.board_width):
            print(" | ".join(board[i:i + self.board_width]))
        print()

    def celebrate_win(self):
        """
        Display a win celebration message for the player.
        """
        print(f"Congratulations! Player {self.icon} wins!")

import requests
from player import Player

class Player_Remote(Player):
    """
    Remote Player class interacts with the Connect4 game server.

    Attributes:
        server_url (str): The base URL of the game server.
    """

    def __init__(self, server_url: str) -> None:
        """
        Initialize a remote player.

        Parameters:
            server_url (str): URL of the Connect4 server.
        """
        super().__init__()
        self.server_url = server_url

    def register_in_game(self) -> str:
        """
        Register the player on the server and assign an icon.

        Returns:
            str: The player's icon.
        """
        response = requests.post(f"{self.server_url}/connect4/register", json={"player_id": str(self.id)})
        if response.status_code == 200:
            self.icon = response.json()["player_icon"]
            return self.icon
        else:
            raise Exception(f"Failed to register player: {response.text}")

    def is_my_turn(self) -> bool:
        """
        Check if it is the player's turn by querying the server.

        Returns:
            bool: True if it is the player's turn, False otherwise.
        """
        response = requests.get(f"{self.server_url}/connect4/status")
        if response.status_code == 200:
            return response.json()["active_player"] == str(self.id)
        else:
            raise Exception(f"Failed to get game status: {response.text}")

    def get_game_status(self):
        """
        Get the game's current status by querying the server.

        Returns:
            dict: The game status.
        """
        response = requests.get(f"{self.server_url}/connect4/status")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get game status: {response.text}")

    def make_move(self) -> int:
        """
        Prompt the player to choose a move and send it to the server.

        Returns:
            int: The column chosen for the move.
        """
        while True:
            try:
                column = int(input(f"Player {self.icon}, enter your move (0-7): "))
                response = requests.post(f"{self.server_url}/connect4/check_move", json={"player_id": str(self.id), "column": column})
                if response.status_code == 200:
                    return column
                else:
                    print(f"Invalid move: {response.json().get('error', 'Unknown error')}")
            except ValueError:
                print("Please enter a valid number.")

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect4 board by querying the server.
        """
        response = requests.get(f"{self.server_url}/connect4/board")
        if response.status_code == 200:
            board = response.json()["board"]
            for row in range(7):
                print("|".join(board[row * 8:(row + 1) * 8]))
            print("-" * 15)
        else:
            raise Exception(f"Failed to get board: {response.text}")

    def celebrate_win(self) -> None:
        """
        Celebrate the player's win.
        """
        print(f"Congratulations! Player {self.icon} wins!")

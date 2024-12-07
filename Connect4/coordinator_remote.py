import requests
import uuid

class Player_Remote:
    """
    A remote player that interacts with a Connect4 server via REST API.
    """

    def __init__(self, server_url):
        """
        Initialize a remote player.
        Parameters:
            server_url (str): The base URL of the Connect4 server.
        """
        self.server_url = server_url
        self.id = str(uuid.uuid4())  # Generate a unique ID for the player
        self.icon = None  # Will be assigned after registration

    def register_in_game(self):
        """
        Register the player on the server and get the assigned icon.
        """
        print("Attempting to register player...")
        response = requests.post(
            f"{self.server_url}/connect4/register",
            json={"player_id": self.id},
        )
        print(f"Server response: {response.status_code} - {response.text}")
        response.raise_for_status()
        self.icon = response.json()["player_icon"]
        print(f"Player registered successfully with icon: {self.icon}")

    def get_game_status(self):
        """
        Query the server for the current game status.
        Returns:
            dict: The current game status.
        """
        print("Querying server for game status...")
        response = requests.get(f"{self.server_url}/connect4/status")
        print(f"Server response: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()

    def make_move(self):
        """
        Prompt the player to enter a column and send the move to the server.
        """
        column = int(input("Enter the column number (1-8): "))
        column -= 1
        response = requests.post(
            f"{self.server_url}/connect4/check_move",
            json={"column": column, "player_id": self.id},
        )
        print(f"Server response: {response.status_code} - {response.text}")
        response.raise_for_status()

    def visualize(self):
        """
        Fetch and print the current game board.
        """
        print("Fetching current board...")
        response = requests.get(f"{self.server_url}/connect4/board")
        response.raise_for_status()
        board = response.json()["board"]
        for i in range(0, len(board), 8):
            print(" | ".join(board[i:i+8]))
        print()

    def celebrate_win(self):
        """
        Display a win celebration message for the player.
        """
        print("Congratulations, you win!")


class Coordinator_Remote:
    """
    Coordinates a remote player interacting with the Connect4 server.
    """

    def __init__(self, server_url):
        """
        Initialize the coordinator with the server URL.
        Parameters:
            server_url (str): The base URL of the Connect4 server.
        """
        self.server_url = server_url
        self.player = Player_Remote(self.server_url)

    def play(self):
        """
        Main function to manage the game flow for the remote player.
        """
        print("Starting remote game...")

        # Register the player
        print("Registering player...")
        try:
            self.player.register_in_game()
            print(f"Player registered successfully with icon: {self.player.icon}")
        except Exception as e:
            print(f"Error during player registration: {e}")
            return

        # Main game loop
        while True:
            print("Fetching game status...")
            try:
                status = self.player.get_game_status()
                print(f"Game status: {status}")
            except Exception as e:
                print(f"Error fetching game status: {e}")
                break

            if status["winner"]:
                print(f"Game over! Winner: {status['winner']}")
                if status["winner"] == self.player.icon:
                    self.player.celebrate_win()
                else:
                    print(f"Player {status['winner']} wins!")
                break

            if status["active_player"] == self.player.id:
                print("It's your turn!")
                self.player.visualize()
                self.player.make_move()
            else:
                print("Waiting for the other player...")


if __name__ == "__main__":
    # Ask for the server URL
    server_url = input("Enter the server URL (e.g., http://127.0.0.1:5000): ")
    # Add protocol if missing
    if not server_url.startswith("http://") and not server_url.startswith("https://"):
        server_url = f"http://{server_url}"

    # Start the coordinator
    coordinator = Coordinator_Remote(server_url)
    coordinator.play()

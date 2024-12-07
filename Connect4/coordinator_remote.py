import requests
import uuid

class Connect4:
    """
    Connect4 game logic.
    This class is typically used on the server to manage the game state.
    """

    def __init__(self):
        # Initialize the board as a 7x8 grid
        self.board = [["" for _ in range(8)] for _ in range(7)]
        self.players = {}
        self.active_player = None
        self.turn_number = -1
        self.winner = None

    def get_status(self):
        return {
            "active_player": self.active_player,
            "active_id": self.players.get(self.active_player, {}).get("id"),
            "winner": self.winner,
            "turn_number": self.turn_number
        }

    def register_player(self, player_id):
        if len(self.players) >= 2:
            raise ValueError("Game already has two players.")
        icon = "X" if len(self.players) == 0 else "O"
        self.players[player_id] = {"icon": icon}
        if self.active_player is None:
            self.active_player = player_id
        self.turn_number = 0
        return icon

    def get_board(self):
        return [item for row in self.board for item in row]

    def check_move(self, column, player_id):
        if player_id != self.active_player:
            raise ValueError("Not this player's turn.")
        for row in reversed(self.board):
            if row[column] == "":
                row[column] = self.players[player_id]["icon"]
                self.turn_number += 1
                self._update_status()
                return True
        raise ValueError("Column is full.")

    def _update_status(self):
        self.active_player = next(
            (p for p in self.players if p != self.active_player), None
        )
        self.winner = self._detect_win()

    def _detect_win(self):
        # Simplified win detection logic
        for row in self.board:
            for i in range(len(row) - 3):
                if row[i] and row[i:i+4] == [row[i]] * 4:
                    return self.players[self.active_player]["icon"]
        return None


class Player_Remote:
    """
    A remote player that interacts with a Connect4 server via REST API.
    """

    def __init__(self, server_url):
        self.server_url = server_url
        self.id = str(uuid.uuid4())
        self.icon = None

    def register_in_game(self):
        print("Attempting to register player...")
        response = requests.post(
            f"{self.server_url}/connect4/register", json={"player_id": self.id}
        )
        print(f"Server response: {response.status_code} - {response.text}")
        response.raise_for_status()
        self.icon = response.json()["player_icon"]
        print(f"Player registered with icon: {self.icon}")

    def get_game_status(self):
        print("Querying server for game status...")
        response = requests.get(f"{self.server_url}/connect4/status")
        print(f"Server response: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()

    def make_move(self):
        column = int(input("Enter the column number (0-7): "))
        response = requests.post(
            f"{self.server_url}/connect4/check_move",
            json={"column": column, "player_id": self.id},
        )
        print(f"Server response: {response.status_code} - {response.text}")
        response.raise_for_status()

    def visualize(self):
        print("Fetching current board...")
        response = requests.get(f"{self.server_url}/connect4/board")
        response.raise_for_status()
        board = response.json()
        for i in range(0, len(board), 8):
            print(" | ".join(board[i:i+8]))
        print()

    def celebrate_win(self):
        print("Congratulations, you win!")


class Coordinator_Remote:
    """
    Coordinator for Remote Players.

    Manages the game flow for remote players interacting with a server via REST API.
    """

    def __init__(self, server_url):
        self.server_url = server_url
        self.player = Player_Remote(self.server_url)

    def play(self):
        print("Starting remote game...")
        print("Registering player...")
        try:
            self.player.register_in_game()
            print(f"Player registered successfully with icon: {self.player.icon}")
        except Exception as e:
            print(f"Error during player registration: {e}")
            return

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
    server_url = input("Enter the server URL (e.g., http://127.0.0.1:5000): ")
    coordinator = Coordinator_Remote(server_url)
    coordinator.play()

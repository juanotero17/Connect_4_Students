from game import Connect4
from player_local import Player_Local

class Coordinator_Local:
    """
    Coordinator for two Local players.

    Manages the game flow, player registration, turn management,
    and game status updates for local players.

    Attributes:
        game (Connect4): Local instance of a Connect4 game.
        player1 (Player_Local): First local player.
        player2 (Player_Local): Second local player.
    """

    def __init__(self) -> None:
        """
        Initialize the Coordinator_Local with a Connect4 game and two players.
        """
        self.game = Connect4()
        self.player1 = Player_Local(self.game)
        self.player2 = Player_Local(self.game)

    def play(self):
        """
        Main function to run the game with two local players.

        Handles player registration, turn management, and checking for a winner
        until the game concludes.
        """
        # Register players in the game
        print("Registering players...")
        icon1 = self.player1.register_in_game()
        icon2 = self.player2.register_in_game()

        print(f"Player 1 is {icon1}, Player 2 is {icon2}")

        # Game loop
        while True:
            # Check if there is a winner
            game_status = self.game.get_status()
            if game_status["winner"]:
                winner_icon = game_status["winner"]
                if winner_icon == self.player1.icon:
                    self.player1.celebrate_win()
                else:
                    self.player2.celebrate_win()
                break

            # Get the active player
            active_player = self.player1 if game_status["active_player"] == self.player1.id else self.player2

            # Visualize the board
            active_player.visualize()

            # Prompt the active player to make a move
            print(f"Player {active_player.icon}'s turn.")
            active_player.make_move()

if __name__ == "__main__":
    # Start the local game coordinator
    coordinator = Coordinator_Local()
    coordinator.play()

import uuid
from sense_hat import SenseHat
from game import Connect4
from player_raspi_local import Player_Raspi_Local


class Coordinator_Raspi_Local:
    """
    Coordinates the Connect4 game for two local players using Sense HAT.
    """

    def __init__(self):
        """
        Initialize the game coordinator with two local players on Raspberry Pi.
        """
        # Initialize the Sense HAT instance
        self.sense = SenseHat()

        # Initialize the game logic
        self.game = Connect4()

        # Initialize two players with the shared Sense HAT instance
        self.player1 = Player_Raspi_Local(self.game, id=uuid.uuid4(), sense=self.sense)
        self.player2 = Player_Raspi_Local(self.game, id=uuid.uuid4(), sense=self.sense)

    def play(self):
        """
        Main game loop for Connect4.
        """
        print("Starting Connect4 on Sense HAT!")
        while True:
            # Get the current game state
            state = self.game.get_game_state()
            winner = state["winner"]

            # Check if there's a winner
            if winner:
                if winner == self.player1.icon:
                    self.player1.celebrate_win()
                else:
                    self.player2.celebrate_win()
                break

            # Determine the current player
            current_player = (
                self.player1 if state["active_player"] == self.player1.id else self.player2
            )

            # Visualize the board and prompt the player to make a move
            current_player.visualize()
            current_player.make_move()


if __name__ == "__main__":
    coordinator = Coordinator_Raspi_Local()
    coordinator.play()

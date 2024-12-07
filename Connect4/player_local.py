from game import Connect4
from player import Player


class Player_Local(Player):
    """ 
    Local Player (uses Methods of the Game directly).
    """

    def __init__(self, game: Connect4) -> None:
        """ 
        Initialize a local player.

        Parameters:
            game (Connect4): Instance of Connect4 game.
        """
        super().__init__()  # Initialize id and icon from the abstract Player class
        self.game = game

    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

        Returns:
            str: The player's icon.
        """
        self.icon = self.game.register_player(self.id)
        return self.icon

    def is_my_turn(self) -> bool:
        """ 
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        game_status = self.game.get_status()
        return game_status["active_player"] == self.id

    def get_game_status(self):
        """
        Get the game status.

        Returns:
            dict: Contains active player, winner, and turn number.
        """
        return self.game.get_status()

    def make_move(self) -> int:
        """ 
        Prompt the player to enter a move via the console.

        Returns:
            int: The column chosen by the player for the move.
        """
        while True:
            try:
                column = int(input(f"Player {self.icon}, enter your move (1-8): "))
                column -= 1
                if self.game.check_move(column, self.id):
                    return column
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a valid number.")

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        """
        board = self.game.get_board()
        for row in board:
            print("|".join(row))
        print("-" * (2 * len(board[0]) - 1))

    def celebrate_win(self) -> None:
        """
        Celebrate the player's win.
        """
        print(f"Congratulations! Player {self.icon} wins!")

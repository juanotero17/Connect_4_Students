import uuid
import numpy as np


class Connect4:
    """
    Connect 4 Game Class

        Defines rules of the Game
            - what is a win
            - where can you set / not set a coin
            - how big is the playing field

        Also keeps track of the current game
            - what is its state
            - who is the active player?

        Is used by the Coordinator
            -> executes the methods of a Game object
    """

    def __init__(self) -> None:
        """
        Init a Connect 4 Game
            - Create an empty Board
            - Create two (non-registered and empty) players.
            - Set the Turn Counter to 0
            - Set the Winner to None
        """
        self.board = np.full((7, 8), " ")  # 7 rows x 8 columns
        self.players = {}
        self.active_player = None
        self.turn_number = 0
        self.winner = None

    def get_status(self):
        """
        Get the game status.
            - active player (id or icon)
            - is there a winner? if so, who?
            - what turn is it?
        """
        return {
            "active_player": self.active_player,
            "active_icon": self.players.get(self.active_player, None),
            "winner": self.winner,
            "turn_number": self.turn_number,
        }

    def register_player(self, player_id: uuid.UUID) -> str:
        """
        Register a player with a unique ID.

        Parameters:
            player_id (UUID): Unique player ID.

        Returns:
            str: Player icon ("X" or "O"), or None if registration failed.
        """
        if len(self.players) < 2:
            icon = "X" if len(self.players) == 0 else "O"
            self.players[player_id] = icon

            # Set the first player as active
            if len(self.players) == 1:
                self.active_player = player_id

            return icon
        return None

    def get_board(self):
        """
        Returns the current board state as a flat list for easier JSON serialization.
        """
        try:
            return [cell or " " for row in self.board for cell in row]  # Flatten the board
        except Exception as e:
            print(f"Error in Connect4.get_board: {e}")  # Debugging output
            raise

    def check_move(self, column: int, player_id: uuid.UUID) -> bool:
        """
        Check if a move is legal, and make the move if valid.
        """
        print(f"Debug: Player {player_id} attempting move in column {column}")  # Debug
        if self.winner:
            print("Debug: Game already has a winner.")  # Debug
            return False  # Game already won

        if player_id != self.active_player:
            print("Debug: Not this player's turn.")  # Debug
            return False  # Not the player's turn

        if column < 0 or column >= self.board.shape[1]:
            print("Debug: Invalid column.")  # Debug
            return False  # Invalid column

        for row in range(self.board.shape[0] - 1, -1, -1):
            if self.board[row, column] == " ":
                self.board[row, column] = self.players[player_id]
                self.turn_number += 1
                self.__update_status()
                print(f"Debug: Board updated:\n{self.board}")  # Debug
                return True

        print("Debug: Column is full.")  # Debug
        return False  # Column full

    def __update_status(self):
        """
        Update the game status after a successful move.
        """
        # Check for a winner
        self.winner = self.__detect_win()

        # Switch active player if no winner
        if not self.winner:
            player_ids = list(self.players.keys())
            self.active_player = player_ids[self.turn_number % 2]

    def __detect_win(self) -> str:
        """
        Detect if a player has won the game (four consecutive pieces).

        Returns:
            str: The winning player's icon, or None if no winner.
        """
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                if self.board[row, col] == " ":
                    continue

                if (
                        self.__check_direction(row, col, 1, 0) or  # Vertical
                        self.__check_direction(row, col, 0, 1) or  # Horizontal
                        self.__check_direction(row, col, 1, 1) or  # Diagonal down-right
                        self.__check_direction(row, col, 1, -1)  # Diagonal down-left
                ):
                    return self.board[row, col]

        return None

    def __check_direction(self, row: int, col: int, row_step: int, col_step: int) -> bool:
        """
        Check a specific direction for four consecutive pieces.

        Parameters:
            row (int): Starting row.
            col (int): Starting column.
            row_step (int): Row increment per step.
            col_step (int): Column increment per step.

        Returns:
            bool: True if four consecutive pieces are found, False otherwise.
        """
        player_icon = self.board[row, col]
        count = 0

        for i in range(4):
            r, c = row + i * row_step, col + i * col_step
            if 0 <= r < self.board.shape[0] and 0 <= c < self.board.shape[1] and self.board[r, c] == player_icon:
                count += 1
            else:
                break

        return count == 4

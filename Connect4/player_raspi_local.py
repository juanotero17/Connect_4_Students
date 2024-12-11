import time
from sense_hat import SenseHat
from game import Connect4
from player_local import Player_Local


class Player_Raspi_Local(Player_Local):
    """
    Local Raspi Player
    Uses Methods of Game and SenseHat for input/output.
    """

    def __init__(self, game: Connect4, **kwargs) -> None:
        """
        Initialize a local Raspi player with a shared SenseHat instance.

        Parameters:
            game (Connect4): Game instance.
            sense (SenseHat): Shared SenseHat instance for all players. (if SHARED option is used)

        Raises:
            ValueError: If 'sense' is not provided in kwargs.
        """
        # Initialize the parent class (Player_Local)
        super().__init__(game)

        # Extract the SenseHat instance from kwargs
        try:
            self.sense: SenseHat = kwargs["sense"]
        except KeyError:
            raise ValueError(f"{type(self).__name__} requires a 'sense' (SenseHat instance) attribute")

    def register_in_game(self):
        """
        Register in game
        Set Player Icon and Player Color.
        """
        # Call the parent class method to register
        self.icon = super().register_in_game()

        # Assign a color based on the icon
        self.color = [255, 0, 0] if self.icon == "X" else [0, 0, 255]
        print(f"Player {self.icon} registered with color {self.color}!")

    def visualize_choice(self, column: int) -> None:
        """
        Visualize the SELECTION process of choosing a column
        Toggles the LED on the top row of the currently selected column.

        Parameters:
            column (int): Selected column during Selection Process.
        """
        # Create a blank matrix
        matrix = [[0, 0, 0] for _ in range(64)]

        # Highlight the selected column in white
        for row in range(8):  # Add a vertical line for the column
            matrix[column + row * 8] = [255, 255, 255]

        self.sense.set_pixels(matrix)

    def visualize(self) -> None:
        """
        Override Visualization of Local Player
        Display the board on the Sense HAT.
        """
        state = self.game.get_game_state()
        board = state["board"]

        # Map the board to LED colors
        matrix = []
        for row in board:
            for cell in row:
                if cell == "X":
                    matrix.append([255, 0, 0])  # Red for X
                elif cell == "O":
                    matrix.append([0, 0, 255])  # Blue for O
                else:
                    matrix.append([0, 0, 0])  # Black for empty
        while len(matrix) < 64:
            matrix.append([0, 0, 0])  # Fill remaining pixels with black

        # Display on Sense HAT
        self.sense.set_pixels(matrix)

    def make_move(self) -> int:
        """
        Override make_move for Raspberry Pi input using the Sense HAT joystick.
        Uses joystick to move left or right and select a column.

        Returns:
            int: Selected column (0...7).
        """
        column = 0
        self.visualize_choice(column)

        while True:
            for event in self.sense.stick.get_events():
                if event.action == "pressed":
                    if event.direction == "left" and column > 0:
                        column -= 1
                    elif event.direction == "right" and column < 7:
                        column += 1
                    elif event.direction == "middle":
                        # Validate move and return the column if valid
                        if self.game.check_move(column, self.id):
                            return column
                        else:
                            self.sense.show_message("Invalid move", text_colour=[255, 0, 0])
                    self.visualize_choice(column)

    def celebrate_win(self) -> None:
        """
        Celebrate the win for the Raspberry Pi player.
        """
        print(f"Player {self.icon} wins! Celebrating on Sense HAT!")
        for _ in range(3):
            self.sense.clear(self.color)
            time.sleep(0.5)
            self.sense.clear()
            time.sleep(0.5)
        self.sense.show_message(f"{self.icon} Wins!", text_colour=self.color)

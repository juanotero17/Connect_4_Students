from player_remote import Player_Remote


class Coordinator_Remote:
    """
    Coordinates a remote player interacting with the Connect4 server.
    """

    def __init__(self, server_url: str) -> None:
        self.player = Player_Remote(server_url)

    def play(self):
        """
        Main function to manage the game flow for the remote player.
        """
        print("Starting remote game...")
        try:
            self.player.register_in_game()
        except Exception as e:
            print(f"Error during player registration: {e}")
            return

        while True:
            try:
                status = self.player.get_game_status()
                if status["winner"]:
                    print(f"Game over! Winner: {status['winner']}")
                    if status["winner"] == self.player.icon:
                        self.player.celebrate_win()
                    break

                if self.player.is_my_turn():
                    self.player.visualize()
                    self.player.make_move()
                else:
                    print("Waiting for the other player...")
            except Exception as e:
                print(f"Error during game loop: {e}")
                break


if __name__ == "__main__":
    server_url = input("Enter the Connect4 server URL (e.g., http://127.0.0.1:5000): ")
    coordinator = Coordinator_Remote(server_url)
    coordinator.play()

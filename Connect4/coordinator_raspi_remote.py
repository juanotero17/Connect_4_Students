import requests


class Coordinator_Raspi_Remote:
    """
    Coordinator for a Raspberry Pi remote player.

    Attributes:
        server_url (str): The base URL of the Connect4 server.
        player (Player_Rasp_Remote): Instance of the Raspberry Pi player.
    """

    def __init__(self, server_url):
        """
        Initialize the coordinator with the server URL.
        """
        self.server_url = server_url
        self.player = Player_Raspi_Remote(self.server_url)

    def play(self):
        """
        Main function to run the game for the Raspberry Pi remote player.
        """
        print("Starting remote game...")
        try:
            # Register the player
            self.player.register_in_game()
            print(f"Player registered with icon: {self.player.icon}")
        except Exception as e:
            print(f"Error during player registration: {e}")
            return

        # Main game loop
        while True:
            try:
                # Fetch game status
                status = self.player.get_game_status()
                if status["winner"]:
                    if status["winner"] == self.player.icon:
                        self.player.celebrate_win()
                    else:
                        print(f"Player {status['winner']} wins!")
                    break

                if status["active_player"] == self.player.id:
                    print("Your turn!")
                    self.player.visualize()
                    self.player.make_move()
                else:
                    print("Waiting for the other player...")
            except Exception as e:
                print(f"Error during game loop: {e}")
                break


if __name__ == "__main__":
    # Prompt for the server URL
    server_url = input("Enter the Connect4 server URL (e.g., http://192.168.1.14:5000): ")
    if not server_url.startswith("http"):
        server_url = f"http://{server_url}"

    coordinator = Coordinator_Raspi_Remote(server_url)
    coordinator.play()

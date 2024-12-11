from player_raspi_remote import Player_Raspi_Remote
import time
class Coordinator_Raspi_Remote:
    """
    Coordinates a remote Sense HAT player interacting with the Connect4 server.
    """

    def __init__(self, server_url):
        self.server_url = server_url
        self.player = Player_Raspi_Remote(server_url)

    def play(self):
        print("Starting remote game on Sense HAT...")
        try:
            self.player.register_in_game()
            print(f"Player registered successfully with icon: {self.player.icon}")
        except Exception as e:
            print(f"Error during registration: {e}")
            return

        while True:
            try:
                status = self.player.get_game_status()
                print(f"Debug: Game status: {status}")  # Debugging game status

                if status["winner"]:
                    if status["winner"] == self.player.icon:
                        self.player.celebrate_win()
                    else:
                        print(f"Player {status['winner']} wins!")
                    break

                if status["active_player"] == str(self.player.id):
                    print("It's your turn!")
                    self.player.visualize()
                    self.player.make_move()
                else:
                    print("Waiting for the other player...")
                    time.sleep(2)  # Add a small delay to avoid constant polling

            except Exception as e:
                print(f"Error during game loop: {e}")
                break


if __name__ == "__main__":
    server_url = input("Enter the Connect4 server URL (e.g., http://192.168.1.x:5000): ")
    coordinator = Coordinator_Raspi_Remote(server_url)
    coordinator.play()

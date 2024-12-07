from player_raspi_remote import Player_Raspi_Remote

class Coordinator_Rasp_Remote:
    """
    Coordinates a Raspberry Pi remote player interacting with the Connect4 server.
    """

    def __init__(self, server_url):
        self.server_url = server_url
        self.player = Player_Raspi_Remote(server_url)

    def play(self):
        print("Starting Raspberry Pi remote game...")
        try:
            self.player.register_in_game()
            print(f"Player registered successfully with icon: {self.player.icon}")
        except Exception as e:
            print(f"Error during registration: {e}")
            return

        while True:
            try:
                status = self.player.get_game_status()
                if status["winner"]:
                    if status["winner"] == self.player.icon:
                        self.player.celebrate_win()
                    else:
                        print(f"Player {status['winner']} wins!")
                    break

                if status["active_player"] == self.player.id:
                    self.player.visualize()
                    self.player.make_move()
                else:
                    print("Waiting for the other player...")
            except Exception as e:
                print(f"Error during game loop: {e}")
                break


if __name__ == "__main__":
    server_url = input("Enter the Connect4 server URL (e.g., http://192.168.x.x:5000): ")
    coordinator = Coordinator_Rasp_Remote(server_url)
    coordinator.play()

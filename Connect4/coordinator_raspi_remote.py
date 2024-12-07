from player_raspi_remote import Player_Raspi_Remote


class Coordinator_Raspi_Remote:
    def __init__(self, server_url: str) -> None:
        self.player = Player_Raspi_Remote(server_url)

    def play(self):
        print("Starting Raspberry Pi remote game...")
        try:
            self.player.register_in_game()
        except Exception as e:
            print(f"Error during registration: {e}")
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
    coordinator = Coordinator_Raspi_Remote(server_url)
    coordinator.play()

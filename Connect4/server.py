import socket  # To get the local IP
from flask import Flask, request, jsonify  # For API
from flask_swagger_ui import get_swaggerui_blueprint  # For Swagger documentation
from game import Connect4  # Import the Connect4 game logic


class Connect4Server:
    """
    Game Server for Connect4
        Runs on localhost and exposes REST API endpoints for gameplay.

    Attributes:
        game (Connect4): Instance of the Connect4 game.
        app (Flask): Flask app instance for handling API requests.
    """

    def __init__(self):
        """
        Initialize the Connect4 Server.
        - Set up Swagger UI documentation.
        - Expose game-related API endpoints.
        """
        self.game = Connect4()  # Initialize the Connect4 game instance
        self.app = Flask(__name__)  # Flask app instance

        # Swagger UI Configuration
        SWAGGER_URL = '/swagger/connect4/'
        API_URL = '/static/swagger.json'  # Point to your static swagger.json file

        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={"app_name": "Connect 4 API"}  # Swagger UI configuration
        )

        # Register the Swagger UI blueprint
        self.app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

        # Define API routes
        self.setup_routes()

    def setup_routes(self):
        """Set up the API endpoints for the Connect4 game."""

        # Root endpoint
        @self.app.route('/')
        def index():
            return "Welcome to the Connect 4 API!"

        # Endpoint: Get game status
        @self.app.route('/connect4/status', methods=['GET'])
        def get_status():
            try:
                status = self.game.get_status()  # Fetch the game status
                return jsonify(status), 200
            except Exception as e:
                return jsonify({"error": "Failed to fetch game status", "details": str(e)}), 500

        # Endpoint: Register a player
        @self.app.route('/connect4/register', methods=['POST'])
        def register_player():
            try:
                data = request.get_json()  # Extract JSON payload
                if not data or "player_id" not in data:
                    raise ValueError("Missing player_id in request body.")

                player_id = data['player_id']
                icon = self.game.register_player(player_id)  # Register the player
                return jsonify({"player_icon": icon}), 200
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

        # Endpoint: Get the game board
        @self.app.route('/connect4/board', methods=['GET'])
        def get_board():
            try:
                # Fetch the board state from the Connect4 game instance
                board = self.game.get_board()
                return jsonify({"board": board}), 200
            except Exception as e:
                print(f"Error in /connect4/board: {e}")  # Log the error
                return jsonify({"error": "Failed to fetch board", "details": str(e)}), 500

        # Endpoint: Make a move
        @self.app.route('/connect4/check_move', methods=['POST'])
        def check_move():
            try:
                data = request.get_json()  # Extract JSON payload
                if not data or "column" not in data or "player_id" not in data:
                    raise ValueError("Missing column or player_id in request body.")

                column = data['column']
                player_id = data['player_id']
                success = self.game.check_move(column, player_id)  # Attempt to make the move
                return jsonify({"success": success}), 200
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

    def run(self, debug=True, host='0.0.0.0', port=5000):
        """Run the server."""
        # Display the local IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Server is running on {local_ip}:{port}")

        # Start the Flask app
        self.app.run(debug=debug, host=host, port=port)


# Entry point: Run the server
if __name__ == '__main__':
    server = Connect4Server()  # Initialize the Connect4Server
    server.run()  # Start the Flask app

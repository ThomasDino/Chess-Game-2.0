<div align="center"><img src="path/to/your/chess_game_logo.png"></div>
<h1 align="center">Chess Game</h1>
<p align="center"><strong>Description</strong>
<br>A Pygame-based Chess game implementation in Python, featuring two-player mode with optional board flipping and customizable time controls.</p>
<br/>
<h2>About</h2>
- Provides a classic 8x8 Chess game.
<br/>
- Supports two-player mode on the same machine, allowing players to take turns.
<br/>
- Includes an optional board flip feature for players to view the board from their own perspective after each turn.
<br/>
- Offers customizable time controls with adjustable initial time and increment per move.
<br/>
- Features a graphical user interface with high-quality chess piece images and a visually appealing chessboard.
<br/>
- Utilizes Pygame for rendering, event handling, and user interactions.

<h2>Key Features</h2>
- Chess Logic: Implements all standard chess rules, including castling, en passant, pawn promotion, and check/checkmate detection.
<br/>
- Two-Player Support: Allows two players to play on the same computer, taking turns to make moves.
<br/>
- Board Flip Option: Includes a checkbox to enable or disable board flipping after each move.
<br/>
- Time Controls: Offers optional time controls with customizable initial time and increment per move.
<br/>
- Graphical Interface: Provides an intuitive and visually appealing interface using Pygame.
<br/>
- Captured Pieces Display: Shows captured pieces for each player.
<br/>
- Move Validation: Ensures that all moves are valid according to chess rules and prevents illegal moves.
<br/>
- Pawn Promotion: Allows players to promote pawns to a piece of their choice upon reaching the opposite side of the board.

<h2>Technologies Used</h2>
- Python
<br/>
- Pygame
<br/>
- Object-Oriented Programming

<h2>Installation</h2>

1. Clone the repository: `git clone https://github.com/your-username/chess-game.git`
2. Navigate to the project directory: `cd chess-game`
3. Install required dependencies: `pip install pygame`
4. Ensure Assets:
   - Make sure the `assets` folder contains all the necessary chess piece images (e.g., `white king.png`, `black queen.png`, etc.).
   - The images should be placed in an `assets` directory within the project folder.

<h2>Usage</h2>
- Run the game: `python chess_game.py`
<br/>
- Game Interface:
  - The game window will display the chessboard, captured pieces area, and control buttons.
  - The right side of the window includes buttons for "Restart Game" and "Play with Time," as well as a checkbox for "Flip Board."
<br/>
- Playing the Game:
  - Selecting a Piece: Click on a piece to select it. Valid moves for that piece will be highlighted.
  - Making a Move: Click on a highlighted square to move the selected piece.
  - Turn Indicator: The status bar at the bottom displays whose turn it is and prompts for action.
  - Captured Pieces: Captured pieces are displayed on the side for each player.
<br/>
- Time Controls:
  - Enabling Time Controls: Click on "Play with Time" to set custom time controls.
  - Setting Time: Enter the initial time (in minutes) and increment (in seconds) when prompted.
  - Timers: Player timers are displayed at the bottom, counting down during their turn.
<br/>
- Board Flipping:
  - Enabling Flip Board: Check the "Flip Board" checkbox to enable board flipping after each move.
  - Disabling Flip Board: Uncheck the checkbox to disable the feature.
<br/>
- Restarting the Game:
  - Click on "Restart Game" to reset the game to its initial state at any time.
<br/>
- Pawn Promotion:
  - When a pawn reaches the opposite side, a menu will appear to choose a piece for promotion.
<br/>
- Game Over:
  - The game detects checkmate and stalemate conditions, displaying the winner or declaring a draw.

<h2>Credits</h2>

- Author: Thomas Dinopoulos

</p>
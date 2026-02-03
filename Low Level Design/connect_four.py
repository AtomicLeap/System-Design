# Connect Four Board Game

# Problem Statement
"""
Build a two-player Connect Four game. Player take turns dropping discs 
into a 7-column, 6-row board. The first to align four of their own discs 
vertically, horizontally, or diagonally wins."
"""

# Ask Clarifying Questions
"""
A reliable way to structure your questions is to cover four areas:

1. Primary functionalities/capabilities
2. Error handling
3. Scope boundaries
4. Any Future features

1. Primary capabilities - Questions
- How do players interact with the game? Do they just specify a 
    column number and the disc drops?
- What are all the ways a game can end? Is it just four in a row, 
    or are there draws?

2. Error handling - Questions
- What should happen if a user tries to drop a disc in a column 
    that's already full? Should I return an error, throw an exception, 
    or just ignore it?
- And what if a player tries to move out of turn?

3. Scope boundaries - Questions
- Are we designing this to support one game at a time, or do we need to 
    handle multiple concurrent games?
- And is this design limited to backend logic only, or do we need UI 
    support as well?

4. Any Future features - Questions
- Do we need to track move history or support undo?
- What about board size—does it need to be configurable, or always 7x6?
- Do we need to support BOT/Computer vs user game?

Perfect. You've now clarified scope and ruled out unnecessary complexity.
"""

"""
------------     ----------   --------------   ----------------   ---------------
|Requirements|-->|Entities|-->|Class Design|-->|Implementation|-->|Extensibility|
------------     ----------   --------------   ----------------   ---------------
"""

# Requirements
"""
1. Two players take turns dropping discs into a 7-column, 6-row board
2. A disc falls to the lowest available row in the chosen column
3. The game ends when:
    - A player gets four discs in a row (vertical, horizontal, or diagonal). They win.
    - The board is full. It's a draw.
4. Invalid moves should be rejected clearly:
    - Dropping in a full column.
    - Moving out of turn.
    - Moving after the game is over.

Out of scope: 
- UI support
- Concurrent games
- Move history
- Undo
- Board size configuration
"""

# Entities
"""
These are the Nouns of our system, usually derived from the requirements:

- Game
- Board
- Player
- Disc
- Move (Moving a disc)
"""

# Class Design (API/Interface)
"""
Each Class should have a clear job. This is so that when requirements 
change, we should be able to point to which class needs updating 
and not re-writting the entire game (system) or changing other classes.

Thus, there should be clear Separation of Concern (SoC) and each class 
should have a Single Responsibility SRP [SOLID Principle].

-> Game - Concerned about game orchestration and flow. It is the game referee.
            It knows whose turn it is, is the game over? Who won? It uses the 
            Board as a tool to decide (know) if the game is won, or there is a draw.
            So if we add undo feature, or switch to three (3) players, only the 
            Game class changes.
-> Board - Dumb physical object that contains the discs. It doesn't know 
            about players or the rules of the game. It's only role is 
            grid physics and placement roles. Thus, when the board size 
            changes (e.g from 7 X 6 to 8 X 8) or the rules of win changes, 
            only the Board class will need updating.
-> Player

Begin implementation from the Top-down starting from Main (Game) class, focusing on 
the Public API/Interface, rather than been lost in implementation details early.

Thus for each of our requirements we derive the state and the behaviour (methods) 
of each class starting from the Game class.

NOTE: Each class has:
1. State(s) - What each class needs to know (track).
2. Behaviour (Methods)

enum GameState:
    IN_PROGRESS
    WON
    DRAW

enum DiscColor:
    RED
    YELLOW

class Game:
    - board: Board
    - player1: Player
    - player2: Player
    - currentPlayer: Player
    - state: GameState        // IN_PROGRESS, WON, DRAW
    - winner: Player | None

    + Game(player1, player2)
    + makeMove(player, column) -> bool
    + getCurrentPlayer() -> Player
    + getGameState() -> GameState
    + getWinner() -> Player | None
    + getBoard() -> Board // When player tries to put Board in Full-view Mode

class Board:
    - rows: int = 6
    - cols: int = 7
    - grid: DiscColor?[rows][cols] // To stick to SRP use DiscColor instead of Player

    + Board()
    + getRows() -> int
    + getCols() -> int
    + canPlace(column) -> bool
    + placeDisc(column, color) -> int // Returns the row the disc falls into
    + isFull() -> bool
    + checkWin(row, column, color) -> bool
    + getCell(row, column) -> DiscColor | None

class Player:
    - name: string
    - color: DiscColor

    + Player(name, color)
    + getName() -> string
    + getColor() -> DiscColor
"""

# Implementation
"""
For each method, follow a consistent pattern:

1. Define the core logic - The happy path that fulfills the requirement.
2. Consider edge cases - What can go wrong? Invalid inputs, illegal states, 
    boundary conditions

Example:
-> Implement Game makeMove method:

class Game:
    makeMove(player, column)
        '''
        Core logic:
            - Place the disc via board.placeDisc(column, player.getColor()) -> returns row
            - Check for win via board.checkWin(row, column, player.getColor())
            - If no win, check for draw via board.isFull()
            - Switch turn if game is still in progress
            - Return true

        Edge cases (reject before touching state):
            - Game is already over (state is WON or DRAW)
            - Wrong player's turn
            - Invalid column or column is full (delegated to Board)
        '''
        if state != IN_PROGRESS
            return false
        if player != currentPlayer
            return false

        row = board.placeDisc(column, player.getColor())
        if row == -1
            return false

        if board.checkWin(row, column, player.getColor())
            state = WON
            winner = player
        else if board.isFull()
            state = DRAW
        else
            currentPlayer = (player == player1) ? player2 : player1 // switch turn
        return true

-> Implement Board placeDisc method:

class Board:
    placeDisc(column, color)
        '''
        Core logic:
        - Find the lowest empty row in that column—start from row = rows - 1 and move 
            upward until you find grid[row][column] == null
        - Place the disc—set grid[row][column] = color
        - Return the row where the disc landed

        Edge cases:
        - Column index out of bounds -> return error or -1
        - Column is full -> return error or -1
        '''
        if column < 0 || column >= cols
            return -1
        if !canPlace(column)
            return -1

        for row = rows - 1 down to 0
            if grid[row][column] == null
                grid[row][column] = color
                return row
        return -1

-> Implement Board checkWin method:

class Board:
    checkWin(row, col, color)
        '''
        Core logic:
        - Define the four directions: horizontal (0, 1), vertical (1, 0), diagonal 
            down-right (1, 1), diagonal up-right (-1, -1)
        - For each direction, count contiguous discs in both directions from 
            (row, column)
        - If any direction reaches 4 or more, return true

        Edge cases:
        - Row or column out of bounds → return false
        - Cell at (row, column) doesn't match the given color → return false
        '''
        if row < 0 || row >= board.getRows() || column < 0 || column >= board.getCols()
                return false
            if board.getCell(row, column) != color
                return false

            directions = [[0,1], [1,0], [1,1], [-1,1]]
            for dr, dc in directions:
                count = 1
                count += countInDirection(row, column, dr, dc, color) # move in the direction
                count += countInDirection(row, column, -dr, -dc, color) # move in the opposite direction
                if count >= 4
                    return true
            return false

        countInDirection(row, col, dr, dc, color)
            count = 0
            r = row + dr
            c = col + dc
            while inBounds(r, c) && board.getCell(r, c) == color
                count++
                r += dr
                c += dc
            return count
"""

# Full Implementation

from enum import Enum
from typing import Optional

class Player:
    def __init__(self, name: str, color):
        self.name = name
        self.color = color  # DiscColor

class DiscColor(Enum):
    RED = "RED"
    YELLOW = "YELLOW"

class Board:
    def __init__(self, rows: int = 6, cols: int = 7):
        self.rows = rows
        self.cols = cols
        self.grid: list[list[Optional[DiscColor]]] = [
            [None for _ in range(cols)] for _ in range(rows)
        ]

    def get_rows(self) -> int:
        return self.rows

    def get_cols(self) -> int:
        return self.cols

    def can_place(self, column: int) -> bool:
        if column < 0 or column >= self.cols:
            return False
        return self.grid[0][column] is None

    def place_disc(self, column: int, color: DiscColor) -> int:
        if not self.can_place(column):
            return -1

        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][column] is None:
                self.grid[row][column] = color
                return row

        return -1

    def check_win(self, row: int, column: int, color: DiscColor) -> bool:
        if not self._in_bounds(row, column) or self.grid[row][column] != color:
            return False

        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

        for dr, dc in directions:
            count = 1
            count += self._count_in_direction(row, column, dr, dc, color)
            count += self._count_in_direction(row, column, -dr, -dc, color)
            if count >= 4:
                return True
        return False

    def is_full(self) -> bool:
        return all(self.grid[0][c] is not None for c in range(self.cols))

    def get_cell(self, row: int, column: int) -> Optional[DiscColor]:
        if not self._in_bounds(row, column):
            return None
        return self.grid[row][column]

    def _count_in_direction(
        self, row: int, column: int, dr: int, dc: int, color: DiscColor
    ) -> int:
        count = 0
        r = row + dr
        c = column + dc
        while self._in_bounds(r, c) and self.grid[r][c] == color:
            count += 1
            r += dr
            c += dc
        return count

    def _in_bounds(self, row: int, column: int) -> bool:
        return 0 <= row < self.rows and 0 <= column < self.cols

class GameState(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    WON = "WON"
    DRAW = "DRAW"

class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.state = GameState.IN_PROGRESS
        self.winner: Optional["Player"] = None

    def make_move(self, player, column: int) -> bool:
        if self.state is not GameState.IN_PROGRESS:
            return False
        if player is not self.current_player:
            return False

        row = self.board.place_disc(column, player.color)
        if row == -1:
            return False

        if self.board.check_win(row, column, player.color):
            self.state = GameState.WON
            self.winner = player
        elif self.board.is_full():
            self.state = GameState.DRAW
        else:
            self.current_player = self.player2 if self.current_player is self.player1 else self.player1

        return True

    def get_current_player(self) -> Player:
        return self.current_player

    def get_game_state(self) -> GameState:
        return self.state

    def get_winner(self) -> Optional[Player]:
        return self.winner

    def get_board(self) -> Board:
        return self.board


# Extensibility
"""
1. How would you support different board sizes?

Update the Board constructor to take any size (number of rows,
number of columns). Based on Single Responsibility Principle SRP,
our Board class is open for extension without needing to modify 
other classes.

2. How would you add undo or move history?

Undo belongs in Game because Game controls the lifecycle, turn order, 
and when state changes. I'd keep a moveHistory stack. Each time a move succeeds, 
I push a small Move record containing the player, row, and column. Undo would 
pop the last move, clear that cell in the Board, revert currentPlayer, and 
recalculate game state if needed. The Board doesn't need any new logic besides 
maybe an internal clearCell method.

We introduce a Move class:

class Move:
    - player: Player
    - row: int
    - col: int

    + Move(player, row, col)

Add a history stack in Game:

class Game:
    - moveHistory: Stack<Move>

And then makeMove would look like this, using the Move value object to store the 
move history:

makeMove(player, column)
    ...
    row = board.placeDisc(column, player.getColor())
    moveHistory.push(Move(player, row, column))
    ...

Add a clearCell helper to Board:

class Board:
    + clearCell(row, col)
        grid[row][col] = null

Then undo becomes:

undoLastMove()
    if moveHistory.isEmpty()
        return false

    last = moveHistory.pop()

    // revert board state
    board.clearCell(last.row, last.col)

    // revert turn order
    currentPlayer = last.player

    // recompute state (simplest version)
    state = IN_PROGRESS
    winner = null

    return true

You can mention that a production version might recompute win state more cleverly, 
but for an interview, this is more than enough.

3. How would you add a computer opponent?

This follow-up is testing whether you can extend behavior without ripping through all 
your existing classes. The key is that rules don't change: Game still enforces turns 
and validity, and Board still owns grid logic. A bot just chooses a column instead of 
a human.

Keep the game rules exactly where they are. Game and Board don't need to change. 
Introduce a small bot component that looks at the current board and returns a column. 
From Game's perspective, a bot move is just another call to makeMove(currentPlayer, column).”
A simple way to describe it is with a separate BotEngine:

class BotEngine:
    + chooseMove(game, bot) -> int

A trivial implementation might just pick the first valid column:

chooseMove(game, bot)
    board = game.getBoard()
    for col = 0 to board.getCols() - 1
        if board.canPlace(col)
            return col
    return -1   // no moves available

Then wherever you drive the game loop:

game = Game(humanPlayer, botPlayer)
bot = BotEngine()

while game.getGameState() == IN_PROGRESS
    current = game.getCurrentPlayer()

    if current == humanPlayer
        column = /* read from UI / input */
    else
        column = bot.chooseMove(game, current)

    game.makeMove(current, column)

The important interview point:
->  We don't change Board at all.
->  We don't change makeMove or the game rules.
->  We just add a thin decision-making layer that chooses a column on behalf of a Player.
"""

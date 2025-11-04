# Chess Board Game


# 1. Requirements

"""
1a. Functional Requirements
 - The Game should load on start.
 - Players should be able to select a play set (Color of play set).
 - A player should be able to make a move.
 - A history of each player's moves should be maintained (persisted in memory and disk upon saving).
 - The game should switch turns (alternate turns between players).
 - A Player should be notified when there is a checkmate.
 - Players should be notified when the game is over and which player has won the game.

1b. Non-Functional Requirements
 - Scalability
   -  100M DAU. Multiple games should be able to run simultaneously.
 - Human and Bot pair game.
 - The game should allow undo/redo of moves.
 - The game should allow adding/removing Spectators.
 - Consistency of Moves >> Availability.
 - Low latency of recording and displaying Moves (< 10ms)

"""

# 2. Core Entities -> (Nouns of our application)

"""
 - Game
 - Board
 - Cell
 - Player
 - Piece
 - Move (Piece Placement/Position on Board)

"""

# 3. System Interface (API) -> (Contracts with our users - returns our Nouns)

"""
 -> Game
  - whitePlayer: Player
  - blackPlayer: Player
  - isWhiteTurn: boolean
  - spectators: List<Spectators>
  - board: Board
  - moveService: MoveService

  + Game(whitePlayer, blackPlayer)

  + addSpectators(spectator): void
  + removeSpectators(spectator): void
  + notifySpectators(moveInfo): void

  + start(): void

 -> Board
  - board: Cell[][]
  + onBoardLoad(): void
  + checkIfWon(player: Player): boolean
  + printNotifcation(): void

 -> Cell
  - row: int
  - col: int
  - piece: Piece
  + Cell(row, col)

 -> Piece
  - color: ColorTypeEnum
  - numOfMoves: int
  - moveHistory: Position[]
  + Piece(color)
  + getPieceType(): PieceType
  + isValidMove(srcPos, destPos, board): boolean
  + move(srcPos, destPos, board): Move

 -> Player
  - name: String
  - color: ColorTypeEnum

  + getPlayerType(): PlayerType
  + decideMove(): String[]

 -> Move
  + isValidMove(piece, srcPos, desPos, board): boolean
  + move(piece, srcPos, desPos, board): Move

 -> MoveService
  - moveHistory: Stack<Move>
  - redoStack: Stack<Move>
  - board: Board

  + MoveService(board)

  + makeMove(piece, srcPos, desPos, board): Move
  + undo(): Move
  + redo(): Move
                     
 -> Spectator
  + addSpectator(spectator): void
  + removeSpectator(spectator): void
  + notifySpectators(moveInfo): void

 -> Action
  - movePiece: Piece
  - from: Cell
  - to: Cell
  - capturedPiece: Piece
  - moveNumber: int

"""

# 4. High-Level Design -> (Satisfies our Functional requirements).


# 5. Deep-Dive -> (Satisfies our Non-functional requirements).


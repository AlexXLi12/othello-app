# Classes and Structs

## GameEngine (Class)
### Description
Does all calculations and game state exploration to find the best move.
### Public Functions
- calculateMove
  - Takes GameBoard object, ToMove, desired depth, and time limit, and returns the best move for the current ToMove within the depth and time limit constraints.

## OthelloRules (namespace)
### Description
Static class that contains methods to handle game logic
### Public Functions
- getPossibles
  - Returns a list of possible moves for current ToMove given a GameBoard object and ToMove
- isMoveValid
  - Returns whether or not the given move is valid for the given player color and GameBoard
- isTerminal
  - Returns whether or not the game is over (no player has any moves)
- countDiscs
  - Returns disc count for black and white
- applyMove
  - Returns a new GameBoard struct with the specified move for current player applied on the GameBoard

## GameBoard (Struct)
### Description
Describes the discs on the board
### Data Members
- WhiteBB
- BlackBB
 
## GameState (Struct)
### Description
Describes all aspects of the current game's state
- Token positions
- Whose turn it is
- Winner (if game is over)
### Data Members
- GameBoard
- MoveLog
- ToMove
- Winner

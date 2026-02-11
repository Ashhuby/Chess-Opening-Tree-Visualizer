# Chess Opening Tree Visualizer
### Build with Python using the Graphviz library

Generates PDF trees of chess openings using real Grandmaster game data.


## How It Works
- It queries the GambitFlow database
- Then builds the tree recursively from any starting position
- Finally, it visualises it with Graphviz

### FEN SYNTAX
FEN = 6 pieces of info separated by spaces

| Letter | Piece |
|--------|-------|
| P/p | Pawn |
| N/n | kNight |
| B/b | Bishop |
| R/r | Rook |
| Q/q | Queen |
| K/k | King |

**Uppercase** = White  
**Lowercase** = Black  
**Numbers** = consecutive empty squares (e.g., `8` = 8 empty squares)

| Field | Description | Starting Value |
|-------|-------------|----------------|
| 1 | Pieces on each row (8 rows top to bottom) | `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR` |
| 2 | Who moves next | `w` (white) |
| 3 | Castling rights | `KQkq` (yes) |
| 4 | En passant target | `-` (no) |
| 5 | Halfmove clock | `0` |
| 6 | Fullmove number | `1` |

 
 > IN PROGRESS

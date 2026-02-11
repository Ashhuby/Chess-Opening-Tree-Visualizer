import os
import sqlite3
import json
import chess
from graphviz import Digraph

# --- SETUP ---
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"
DB_PATH = "opening_theory.db"


def normalize_fen(fen):
    return ' '.join(fen.split(' ')[:4])


def to_uci(move_str, fen):
    """Convert any move format to UCI given the position"""
    try:
        board = chess.Board(fen)
        # Try parsing as UCI first
        try:
            move = chess.Move.from_uci(move_str)
            if move in board.legal_moves:
                return move.uci()
        except:
            pass

        # Try parsing as algebraic/san
        try:
            move = board.parse_san(move_str)
            return move.uci()
        except:
            pass

        # If it's a simple pawn move like "e4"
        if len(move_str) == 2 and move_str[0] in 'abcdefgh' and move_str[1] in '12345678':
            # Assume it's a pawn move from the second rank
            file = move_str[0]
            rank = move_str[1]
            if board.turn == chess.WHITE:
                from_square = f"{file}2"
            else:
                from_square = f"{file}7"
            move = chess.Move.from_uci(f"{from_square}{move_str}")
            if move in board.legal_moves:
                return move.uci()

    except:
        pass

    return None


def get_top_moves(fen, limit=3):
    """Get top moves from a position"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "SELECT move_data, total_games FROM openings WHERE fen = ?",
        (normalize_fen(fen),)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return []

    moves_dict = json.loads(row[0])
    total_games = row[1]

    moves = []
    for move_str, stats in moves_dict.items():
        uci = to_uci(move_str, fen)
        if uci:  # Only include moves we can convert
            moves.append({
                'move': move_str,  # Original from DB
                'uci': uci,  # Converted to UCI
                'display': move_str if len(move_str) <= 4 else uci[2:4],  # What to show
                'frequency': stats['frequency'],
                'pct': (stats['frequency'] / total_games) * 100
            })

    moves.sort(key=lambda x: x['frequency'], reverse=True)
    return moves[:limit]


# --- BUILD TINY TREE ---
dot = Digraph()
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')

# Start position
start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"
dot.node("start", "Start")

# Get White's first moves
white_moves = get_top_moves(start_fen, limit=2)

for w_move in white_moves:
    # Add White's move
    w_node = f"w_{w_move['move']}"
    dot.node(w_node, f"{w_move['display']}\n{w_move['pct']:.0f}%")
    dot.edge("start", w_node, label=w_move['display'])

    # Make the move to get Black's position
    board = chess.Board(start_fen)
    board.push(chess.Move.from_uci(w_move['uci']))
    black_fen = board.fen()

    # Get Black's responses
    black_moves = get_top_moves(black_fen, limit=2)

    for b_move in black_moves:
        # Add Black's move
        b_node = f"b_{w_move['move']}_{b_move['move']}"
        dot.node(b_node, f"{b_move['display']}\n{b_move['pct']:.0f}%")
        dot.edge(w_node, b_node, label=b_move['display'])

# --- RENDER ---
print("Rendering your first chess tree...")
dot.render('first_chess_tree', view=True, format='pdf')
print("Done! Check first_chess_tree.pdf")
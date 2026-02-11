import sqlite3
import json
import chess

conn = sqlite3.connect('opening_theory.db')


def normalize_fen(fen):
    """Strip move counters from FEN for database lookup"""
    return ' '.join(fen.split(' ')[:4])


def uci_to_readable(uci):
    """Convert UCI (e2e4, g1f3, e7e5) to algebraic notation"""
    try:
        move = chess.Move.from_uci(uci)
        board = chess.Board()  # Empty board just for conversion
        return board.san(move)  # SAN = Standard Algebraic Notation
    except:
        return uci  # Fallback to UCI if conversion fails


# --- Start at the beginning ---
start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"

# --- Play e4 ---
board = chess.Board(start_fen)
move = chess.Move.from_uci("e2e4")
board.push(move)
new_fen = board.fen()

print(f"Starting position → e4")
print(f"Normalized FEN: {normalize_fen(new_fen)}\n")

# --- Query the new position ---
cursor = conn.execute(
    "SELECT move_data, total_games FROM openings WHERE fen = ?",
    (normalize_fen(new_fen),)
)
row = cursor.fetchone()

if row:
    moves_dict = json.loads(row[0])
    total_games = row[1]

    print(f"Position after 1.e4 found!")
    print(f"Total games: {total_games:,}\n")
    print("Black's responses:")
    print("-" * 70)
    print(f"{'#':2} {'Move':8} {'Played':>10} {'%':>6} {'Score':>8} {'Raw UCI':>15}")
    print("-" * 70)

    # Convert to list and sort
    moves_list = []
    for move_name, stats in moves_dict.items():
        moves_list.append({
            'move': move_name,
            'readable': uci_to_readable(move_name),
            'frequency': stats['frequency'],
            'percentage': (stats['frequency'] / total_games) * 100,
            'avg_score': stats.get('avg_score', 0)
        })

    moves_list.sort(key=lambda x: x['frequency'], reverse=True)

    # Show top 5 responses for Black
    for i, move in enumerate(moves_list[:5], 1):
        print(
            f"{i:2} {move['readable']:8} {move['frequency']:10,} {move['percentage']:6.1f}% {move['avg_score']:8.3f} {move['move']:>15}")

    # Bonus: Show what we learned
    print("\n" + "=" * 70)
    print("📊 INSIGHTS:")
    print(f"• Most popular: {moves_list[0]['readable']} ({moves_list[0]['percentage']:.1f}%)")
    print(f"• Best by score: {max(moves_list, key=lambda x: x['avg_score'])['readable']} "
          f"({max(moves_list, key=lambda x: x['avg_score'])['avg_score']:+.3f})")

else:
    print("Position not found")

conn.close()
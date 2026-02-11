import sqlite3
import json

conn = sqlite3.connect('opening_theory.db')

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"

cursor = conn.execute(
    "SELECT move_data, total_games FROM openings WHERE fen = ?",
    (fen,)
)
row = cursor.fetchone()

if row:
    moves_dict = json.loads(row[0])
    total_games = row[1]

    # --- Convert to a clean list of dictionaries ---
    moves_list = []

    for move_name, stats in moves_dict.items():
        move_info = {
            'move': move_name,
            'frequency': stats['frequency'],
            'percentage': (stats['frequency'] / total_games) * 100,
            'avg_score': stats.get('avg_score', 0)  # .get() prevents errors if key missing
        }
        moves_list.append(move_info)

    # --- Sort by frequency (most popular first) ---
    moves_list.sort(key=lambda x: x['frequency'], reverse=True)

    # --- Print the top 5 moves ---
    print(f"Starting position - {total_games:,} games\n")
    print("Top 5 moves:")
    print("-" * 50)

    for i, move in enumerate(moves_list[:5], 1):
        print(f"{i}. {move['move']:4} | "
              f"Played: {move['frequency']:7,} times | "
              f"{move['percentage']:5.1f}% | "
              f"Score: {move['avg_score']:+.3f}")

    # --- Bonus: What's the best move by score? ---
    best_by_score = sorted(moves_list, key=lambda x: x['avg_score'], reverse=True)[0]
    print("\n" + "=" * 50)
    print(f"Best move by engine evaluation: {best_by_score['move']} "
          f"({best_by_score['avg_score']:+.3f})")

conn.close()
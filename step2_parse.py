import sqlite3
import json

# 1. Connect to database
conn = sqlite3.connect('opening_theory.db')

# 2. Starting position
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"

# 3. Query the database
cursor = conn.execute(
    "SELECT move_data, total_games FROM openings WHERE fen = ?",
    (fen,)
)
row = cursor.fetchone()

# 4. Parse the JSON
if row:
    move_data_json = row[0]  # This is a string
    total_games = row[1]  # This is a number

    # Convert JSON string to Python dictionary
    moves_dictionary = json.loads(move_data_json)

    print(f"Found starting position!")
    print(f"Total games in database: {total_games}")
    print(f"Type after json.loads(): {type(moves_dictionary)}")
    print(f"Number of different moves: {len(moves_dictionary)}")
    print("\n--- Raw dictionary (first 2 moves) ---")

    # Show the structure
    count = 0
    for move, stats in moves_dictionary.items():
        print(f"\nMove: {move}")
        print(f"  Type: {type(stats)}")
        print(f"  Stats keys: {stats.keys()}")
        print(f"  Frequency: {stats['frequency']}")
        if 'avg_score' in stats:
            print(f"  Avg score: {stats['avg_score']}")
        count += 1
        if count >= 2:
            break

else:
    print("Position not found")

conn.close()
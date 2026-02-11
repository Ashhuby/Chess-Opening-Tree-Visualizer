import sqlite3
import json
from pathlib import Path

db_path = Path('../opening_theory.db')

if not db_path.exists():
    print(f"****Database not found at {db_path.absolute()}")
    print("Download it from:")
    print("https://huggingface.co/datasets/GambitFlow/Opening-Database/resolve/main/opening_theory.db")
    exit()

# Connect and check
conn = sqlite3.connect(str(db_path))
cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"***Database found. Tables: {tables}")

# Try a simple query
cursor = conn.execute("SELECT COUNT(*) FROM openings")
count = cursor.fetchone()[0]
print(f"**{count} positions in database")

# Test the starting position
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"
cursor = conn.execute("SELECT move_data FROM openings WHERE fen = ?", (fen,))
row = cursor.fetchone()

if row:
    moves = json.loads(row[0])
    print(f"**Starting position found! {len(moves)} moves available")
    # Show top 3 moves
    sorted_moves = sorted(moves.items(), key=lambda x: x[1]['frequency'], reverse=True)[:3]
    for move, stats in sorted_moves:
        print(f"   {move}: {stats['frequency']} games")
else:
    print("**Starting position not found in da database")

conn.close()
import sqlite3
import json

# 1. Connect to database
conn = sqlite3.connect('../opening_theory.db')

# 2. Starting position FEN
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"

# 3. Query the database
cursor = conn.execute(
    "SELECT move_data FROM openings WHERE fen = ?",
    (fen,)
)
row = cursor.fetchone()

# 4. What did we get?
if row:
    print("Found starting position!")
    print(f"Raw data type: {type(row[0])}")
    print(f"First 100 characters: {row[0][:100]}...")
else:
    print("Position not found")

conn.close()
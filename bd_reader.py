import sqlite3
import json

# Path to your SQLite DB file
DB_PATH = "shared_memory/db.sqlite3"

def read_all_entries():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Read all entries
        cursor.execute("SELECT * FROM memory")
        rows = cursor.fetchall()

        print("=== Memory Table Contents ===")
        for row in rows:
            entry_id, json_data = row
            print(f"\nEntry ID: {entry_id}")
            try:
                parsed = json.loads(json_data)
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print("Raw JSON:", json_data)

        conn.close()

    except sqlite3.Error as e:
        print("SQLite error:", e)

if __name__ == "__main__":
    read_all_entries()

import sqlite3
import json
from datetime import datetime
import os,threading

class SharedMemory:
    def __init__(self, db_path="shared_memory/db.sqlite3"):
        # abs_path = os.path.abspath(db_path)
        print(f"[DEBUG] Connecting to DB at: {os.path.dirname(db_path)}")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.lock = threading.Lock()
        self.cursor = self.conn.cursor()
        self._create_table()
        

    def __getitem__(self, entry_id):
        # with self.lock:
        self.cursor.execute("SELECT * FROM memory WHERE id = ?", (entry_id,))
        row = self.cursor.fetchone()
        print(50*'*')
        print(row)
        print(50*'*')
        if row:
            return {
                "id": row[0],
                "timestamp": row[1],
                "input_source": row[2],
                "format": row[3],
                "intent": row[4],
                "extracted_fields": json.loads(row[5]) if row[5] else {},
                "action_triggered": row[6],
                "trace": json.loads(row[7]) if row[7] else []
            }
        else:
            # Create empty record if it doesn't exist
            default_data = {
                "id": entry_id,
                "timestamp": datetime.utcnow().isoformat(),
                "input_source": "",
                "format": "",
                "intent": "",
                "extracted_fields": {},
                "action_triggered": "",
                "trace": []
            }
            self.write(entry_id=entry_id)
            return default_data

    # def __setitem__(self, entry_id, value):
    #     with self.lock:
    #         json_data = json.dumps(value)
    #         self.cursor.execute("REPLACE INTO memory (id, data) VALUES (?, ?)", (entry_id, json_data))
    #         self.conn.commit()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                input_source TEXT,
                format TEXT,
                intent TEXT,
                extracted_fields TEXT,
                action_triggered TEXT,
                trace TEXT
            );
        """)
        self.conn.commit()

    def write(self, entry_id, input_source=None, format=None, intent=None,
              extracted_fields=None, action_triggered=None, trace=None):
        timestamp = datetime.utcnow().isoformat()
        self.cursor.execute("""
            INSERT OR REPLACE INTO memory (
                id, timestamp, input_source, format, intent,
                extracted_fields, action_triggered, trace
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry_id,
            timestamp,
            input_source,
            format,
            intent,
            json.dumps(extracted_fields or {}),
            action_triggered or "",
            json.dumps(trace or [])
        ))
        self.conn.commit()

    def read(self, entry_id):
        self.cursor.execute("SELECT * FROM memory WHERE id = ?", (entry_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "timestamp": row[1],
                "input_source": row[2],
                "format": row[3],
                "intent": row[4],
                "extracted_fields": json.loads(row[5]),
                "action_triggered": row[6],
                "trace": json.loads(row[7]),
            }
        return None

    def append_trace(self, entry_id, message):
        data = self.read(entry_id)
        if data:
            trace = data["trace"]
            trace.append(message)
            self.cursor.execute("""
                UPDATE memory SET trace = ? WHERE id = ?
            """, (json.dumps(trace), entry_id))
            self.conn.commit()

    def update_field(self, entry_id, field, value):
        data = self[entry_id]
        data[field] = value
        self[entry_id] = data

    # def append_trace(self, entry_id, message):
    #     data = self[entry_id]
    #     data.setdefault("trace", []).append(message)
    #     self[entry_id] = data



    def update_action(self, entry_id, action):
        self.cursor.execute("""
            UPDATE memory SET action_triggered = ? WHERE id = ?
        """, (action, entry_id))
        self.conn.commit()

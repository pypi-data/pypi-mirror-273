import os
import uuid
import pickle
import sqlite3

db_file = 'chat_logs.db'

# Check if the database file exists
if os.path.exists(db_file):
    conn = sqlite3.connect(db_file)
else:
    # Create a new database file if it doesn't exist
    conn = sqlite3.connect(db_file)

c = conn.cursor()
chat_history = {}

# Create table to store chat logs if not exists
c.execute('''CREATE TABLE IF NOT EXISTS chat_logs
             ( chat_id TEXT PRIMARY KEY, timestamp DATETIME, engine TEXT, query TEXT, response TEXT, index_data BLOB, session_id TEXT)''')
conn.commit()

# Function to log chat interactions to the database
def log_chat(timestamp, query, response, engine, index_data=None, session_id=None):
    chat_id = str(uuid.uuid4())  # Generate unique chat ID
    session_id = None

    if index_data in chat_history:
        session_id = chat_history[index_data]
        c.execute("INSERT INTO chat_logs (chat_id, timestamp, engine, query, response, index_data, session_id ) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (chat_id, timestamp, engine, query, response, None , session_id))

    else:
        session_id = str(uuid.uuid4())  # Generate unique session ID
        chat_history[index_data] = session_id
        c.execute("INSERT INTO chat_logs (chat_id, timestamp, engine, query, response, index_data, session_id ) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (chat_id, timestamp, engine, query, response, index_data, session_id))


    # Store the chat with the determined session ID
    
    conn.commit()

# Function to retrieve and display chat logs by chat ID
def view_chat_by_id(session_id):
    c.execute("SELECT * FROM chat_logs WHERE session_id=?", (session_id,))
    row = c.fetchone()
    if row:
        print("\n")
        print("session_id: ", row[6])
        print("Chat ID:", row[0])
        print("Timestamp:", row[1])
        print("Engine:", row[2])
        print("Query:", row[3])
        print("Response:", row[4])
        index = pickle.loads(row[5])
        print("\n")
    else:
        print("Chat with ID '{}' not found.".format(session_id))
    return index

# Function to retrieve and display all chat logs
def view_chat_logs():
    c.execute("SELECT * FROM chat_logs")
    rows = c.fetchall()
    logs =[]
    for row in rows:
        log = {
            "session": row[6],
            "chat_id": row[0],
            "timestamp": row[1],
            "engine": row[2],
            "query": row[3],
            "response": row[4]
        }
        logs.append(log)
    return logs
        


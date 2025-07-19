import sqlite3

# Connect to a database file (or create one if not there)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Load and run the SQL commands from sample_data.sql
with open("sample_data.sql", "r") as file:
    sql_script = file.read()
cursor.executescript(sql_script)

conn.commit()
conn.close()

print("✅ Database created with sample data!")

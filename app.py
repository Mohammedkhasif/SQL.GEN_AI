import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")  # Replace with your actual API key

model = genai.GenerativeModel("gemini-1.5-flash")



from flask import Flask, render_template_string, request
import sqlite3
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-latest')


app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Natural Language to SQL</title>
</head>
<body>
    <h2>💬 Natural Language to SQL (Powered by Gemini)</h2>
    <form method="POST">
        <label>🔍 Ask your SQL-related question:</label><br>
        <input type="text" name="user_query" style="width:400px;" required>
        <button type="submit">Ask</button>
    </form>
    {% if sql_query %}
        <h3>🧠 Generated SQL:</h3>
        <pre>{{ sql_query }}</pre>
    {% endif %}
    {% if result %}
        <h3>📊 Result:</h3>
        <pre>{{ result }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    sql_query = None
    result = None

    if request.method == "POST":
        user_query = request.form["user_query"]

        prompt = f"""
You are a helpful AI that translates plain English to SQL.
The database has this table:
customers(id INTEGER PRIMARY KEY, name TEXT, city TEXT, age INTEGER)

Convert this: "{user_query}" into a valid SQLite SQL query.
Only output the SQL. No explanation.
        """

        response = model.generate_content(prompt)
        sql_query = response.text.strip().strip("```sql").strip("```")

        # Execute SQL
        try:
            conn = sqlite3.connect("customers.db")
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            result = "\n".join(str(row) for row in rows)
            conn.close()
        except Exception as e:
            result = f"❌ Error: {e}"

    return render_template_string(HTML_TEMPLATE, sql_query=sql_query, result=result)

if __name__ == "__main__":
    app.run(debug=True)

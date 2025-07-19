from flask import Flask, request, jsonify, render_template
from bot.logic import search_employee
from openai import OpenAI
import re
import os

# Initialize Flask app
app = Flask(__name__, static_url_path='/static')

# ✅ Set your OpenAI API key 
openai_api_key = os.getenv("OPENAI_API_KEY", "sk-.....")  # REPLACE THE API KEY HERE ..!!
client = OpenAI(api_key=openai_api_key)

# Home page 
@app.route("/")
def home():
    return render_template("index.html")

# Text normalization (basic Hindi-English transliteration support)
def normalize_query(query):
    query = query.lower()
    replacements = {
        "ki mail id do": "email of",
        "ka email id": "email of",
        "ka mail id": "email of",
        "mail id of": "email of",
        "id": "email",
        "btao": "tell",
        "do": "give",
        "hai?": "do we have?",
        "hai": "",
    }
    for k, v in replacements.items():
        query = query.replace(k, v)
    return query.strip()

# Chat API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "").strip()

    # Normalize for informal Hindi-English
    normalized_query = normalize_query(query)

    # 1st: Search employee dataset
    company_response = search_employee(normalized_query)
    if company_response:
        return jsonify({"response": company_response})
    else:
        # If not found, fallback to OpenAI GPT (for general questions)
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=200,
            )
            reply = response.choices[0].message.content.strip()
            return jsonify({"response": reply})
        except Exception as e:
            return jsonify({"response": f"❌ Error: {str(e)}"})

# Run the app
if __name__ == "__main__":
    print("🚀 Server running at http://127.0.0.1:5000")
    app.run(debug=True)

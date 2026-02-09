from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Debug API key
API_KEY = os.getenv("GROQ_API_KEY")
print("GROQ KEY LOADED:", API_KEY[:5] if API_KEY else "NOT FOUND")

# Init app
app = Flask(__name__)

# Init Groq client
client = Groq(api_key=API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").strip()

    if not user_msg:
        return jsonify({"reply": "Please type something."})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a premium AI Library Assistant. "
                        "Help users with books, library rules, timings, research guidance, "
                        "citations, summaries, and academic support. Be clear and polite."
                    )
                },
                {"role": "user", "content": user_msg}
            ],
            temperature=0.4,
            max_tokens=500
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("AI ERROR:", e)
        return jsonify({"reply": "AI service temporarily unavailable."}), 500


if __name__ == "__main__":
    app.run(debug=True)

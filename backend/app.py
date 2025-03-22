from flask import Flask, request, jsonify, session
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Set a secret key for session management
app.secret_key = "your_secret_key"

prompt_template = """
You are a supportive mental health assistant.
Your goal is to provide encouragement and helpful advice, not medical diagnoses.
Always use empathetic and calming language.
if user stressed or angry or dpressed then suggest cops strategis foe stress relieving.
If a user is distressed, recommend professional help and share helplines.


Here are some resources that might be helpful:
- India: Call Vandrevala Foundation Helpline at 1860 266 2345 or Snehi at +91 9582208181.
- US: Call the National Suicide Prevention Lifeline at 988.
- UK: Call Samaritans at 116 123.

For more resources, visit: [https://www.nami.org/](https://www.nami.org/).

Conversation History:
{history}

User: {user_message}
Assistant:
"""


api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found!")

genai.configure(api_key=api_key)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Retrieve the conversation history from session
    history = session.get("history", "")

    # Format the prompt with history
    formatted_prompt = prompt_template.format(history=history, user_message=user_message)

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  
        response = model.generate_content(formatted_prompt)

        if hasattr(response, "text"):
            # Append the new exchange to history
            history += f"\nUser: {user_message}\nAssistant: {response.text}\n"
            session["history"] = history  # Store updated history in session

            return jsonify({"response": response.text})
        else:
            return jsonify({"error": "No valid response received"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

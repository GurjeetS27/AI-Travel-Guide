import os
from flask import Flask, request, render_template, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set up OpenAI API client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Predefined list of top tourist places per city
TOP_PLACES = {
    "Paris": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Montmartre", "Seine River Cruise"],
    "New York": ["Times Square", "Central Park", "Empire State Building", "Statue of Liberty", "Brooklyn Bridge"],
    "Tokyo": ["Shibuya Crossing", "Tokyo Tower", "Asakusa Temple", "Akihabara", "Ginza Shopping"],
    "London": ["Big Ben", "London Eye", "Tower of London", "Buckingham Palace", "Hyde Park"]
}


@app.route('/')
def home():
    """
    Renders the main HTML page for the AI Travel Guide.
    """
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask_openai():
    """
    Handles user queries for travel recommendations.
    
    Accepts:
    - city (str): The city for which the user wants travel information.
    - question (str): The travel-related question.

    Returns:
    - JSON object with the city, question, and AI-generated answer.
    """
    city = request.form.get("city", "Paris")  # Default city is Paris
    question = request.form.get("question")

    if not question:
        return jsonify({"error": "Please enter a question"}), 400

    # Construct AI prompt
    prompt = f"""
    You are a highly knowledgeable travel assistant specializing in {city}.
    Answer the following question accurately and informatively:

    Question: {question}

    If the question is directly related to **travel, tourism, attractions, hotels, food, or activities in {city}**, provide a helpful response.
    Otherwise, if the question is **completely unrelated to travel**, respond with:
    "I'm here to help with travel-related questions about {city}. Please ask about destinations, hotels, attractions, or things to do."

    Assume the user is asking about travel unless explicitly stated otherwise.
    Provide only the answer; do not repeat the question.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=500,
            temperature=0.3
        )
        answer = response.choices[0].message.content
    except Exception as e:
        return jsonify({"error": f"Error fetching AI response: {str(e)}"}), 500

    return jsonify({"city": city, "question": question, "answer": answer})

if __name__ == '__main__':
    app.run(debug=True)

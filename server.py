"""
server.py - Flask server for Emotion Detection Application.
Provides routes to analyze text and return emotion scores.
"""

from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route('/emotionDetector', methods=['GET', 'POST'])
def detect_emotion():
    """
    Flask route to detect emotions from a given text.
    Accepts GET or POST requests.
    GET: text provided as query parameter 'textToAnalyze'
    POST: text provided as form field 'statement' or JSON {'statement': ...}

    Returns:
        str: Formatted string with emotion scores and dominant emotion,
             or 'Invalid text! Please try again!' if input is blank or invalid.
    """
    text_to_analyze = None

    # Get text safely based on request type
    if request.method == 'GET':
        text_to_analyze = request.args.get('textToAnalyze')
    if request.method == 'POST' and request.form.get('statement'):
        text_to_analyze = request.form.get('statement')
    if request.method == 'POST' and request.is_json:
        text_to_analyze = request.json.get('statement')

    # Handle blank input
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "Invalid text! Please try again!", 200

    # Run emotion detection
    result = emotion_detector(text_to_analyze)

    # Handle None dominant emotion
    if result['dominant_emotion'] is None:
        return "Invalid text! Please try again!", 200

    # Format response text
    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    return response_text


@app.route('/')
def index():
    """
    Flask route to render the homepage of the Emotion Detection application.
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

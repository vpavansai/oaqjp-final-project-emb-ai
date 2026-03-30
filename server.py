from flask import Flask, request, render_template, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['GET', 'POST'])
def detect_emotion():
    # Get text safely
    text_to_analyze = None
    if request.method == 'GET':
        text_to_analyze = request.args.get('textToAnalyze')
    if request.method == 'POST' and request.form.get('statement'):
        text_to_analyze = request.form.get('statement')
    if request.method == 'POST' and request.is_json:
        text_to_analyze = request.json.get('statement')

    # Handle blank input or None dominant emotion
    if not text_to_analyze or text_to_analyze.strip() == "":
        return "Invalid text! Please try again!", 200  # <- changed from 400
     
    result = emotion_detector(text_to_analyze)

    if result['dominant_emotion'] is None:
        return "Invalid text! Please try again!", 200  # <- changed from 400

    # Normal response
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
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
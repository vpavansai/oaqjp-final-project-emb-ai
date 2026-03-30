from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

# Flask route as requested
@app.route('/emotionDetector', methods=['GET', 'POST'])
def detect_emotion():
    # Get text from GET query or POST form/JSON
    text_to_analyze = request.args.get('textToAnalyze') or request.form.get('statement') or (request.json and request.json.get('statement'))
    
    if not text_to_analyze:
        return "No text provided", 400
    
    result = emotion_detector(text_to_analyze)
    
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

# Optional: serve index.html at root
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, request, render_template, url_for
from app import synthesize_speech
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    audio_url = None

    if request.method == "POST":
        text = request.form["text"]
        output_path = os.path.join("static", "output.mp3")
        synthesize_speech(text, output_path)

        audio_url = url_for('static', filename='output.mp3')

    return render_template("index.html", audio_url=audio_url)

if __name__ == "__main__":
    app.run(debug=True)

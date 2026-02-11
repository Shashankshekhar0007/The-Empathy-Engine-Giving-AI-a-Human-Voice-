🎧 The Empathy Engine — Emotion-Aware AI Voice Synthesis

    An AI-powered service that transforms text into expressive human-like speech by dynamically modulating voice characteristics based on detected emotional intent.

🚀 Features

    🧠 Transformer-based emotion detection
    🎭 Emotion-aware voice modulation
    📈 Intensity-scaled expressiveness
    🌐 Flask web interface
    🎧 High-quality MP3 output

------------------------------------------------------------------------------------------------

Design Choices & Emotion-to-Voice Mapping Logic

      Emotion Detection

          * Implemented using a transformer-based classifier from Hugging Face.

          * The model predicts emotion labels with confidence scores.

          * The highest-confidence label is selected as the dominant emotional state.

      Emotion Categories

            Internal model outputs (joy, anger, sadness, fear, surprise, etc.) are mapped into three core synthesis categories:

           * Happy (joy, surprise)

           * Frustrated (anger, sadness, fear, disgust)

           * Neutral (fallback state)

      Intensity Scaling

            * The model’s confidence score (0–1) is treated as emotional intensity.

            * Higher intensity results in stronger modulation of voice parameters.

      Voice Modulation Strategy

              Emotion	             Stability	          Style	                Effect
-----------------------------------------------------------------------------------------------                          |                |                                   |
              Happy	Lower|	       Higher |        Energetic                  | bright
              Frustrated |	       Higher |	       Lower	Controlled          | tense
              Neutral	   |         Medium |	       Medium	Balanced            | natural

      This mapping ensures:

             * Clear audible contrast between emotional states

             * Dynamic expressiveness

             * Human-like prosodic variation

 -----------------------------------------------------------------------------------------------

 System Architecture

    User Text (Web UI)
          ↓
    Transformer Emotion Classifier
          ↓
    Emotion + Intensity Scaling
          ↓
    Voice Parameter Mapping
          ↓
    Expressive TTS Engine
          ↓
    Playable MP3 Output

------------------------------------------------------------------------------------------------

🛠️ Tech Stack

    Layer            |     Technology
  ---------------------------------------------
    Language	       |     Python
    Emotion Analysis |     Hugging Face Transformers (Detects emotional intent from text)
    TTS	             |     ElevenLabs API            (Generates expressive human-like speech)
    Web Interface	   |     Flask                     (Serves the web interface)
    NLP	             |     NLTK                       (Splits text into sentences for                                               fine-grained emotional modulation)

------------------------------------------------------------------------------------------------

📂 Project Structure

    empathy-engine/
    ├── app.py
    ├── web.py
    ├── templates/
    │   └── index.html
    ├── static/
    │   └── output.mp3
    ├── requirements.txt
    └── .env

------------------------------------------------------------------------------------------------

⚙️ Setup Instructions

    1️⃣ Install dependencies
    
        pip install -r requirements.txt

    2️⃣ Configure API key

        Create a .env file:
        ELEVENLABS_API_KEY=your_api_key_here

    3️⃣ Run the app
        python web.py

🌐 Open in browser

       http://127.0.0.1:5000

-----------------------------------------END OF DOCUMENT----------------------------------------
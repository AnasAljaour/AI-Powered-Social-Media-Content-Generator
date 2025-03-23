import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from flask import Flask, request, jsonify
from PromptEngineering import PromptEngineer
import io
import speech_recognition as sr
from pydub import AudioSegment


if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyA8gZZmHcw5VPPMkISi1jy61M47flND1iI"


app = Flask(__name__)



@app.route('/generate_content', methods = ['POST'])
async def generate_content():
    pe = PromptEngineer()
    data = request.get_json()
    if not data or 'text_input' not in data:
        return jsonify({"error": "Invalid input, 'text' is required"}), 400
    platform = data['platform']
    text_input = data['text_input']
    try:
        if not text_input:
            return jsonify({"error": "No input provided"})
        
        full_prompt = pe.create_prompt(platform=platform, user_input=text_input)
        
        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.8,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        
        response = model.invoke(full_prompt)
        
        return jsonify({"generated_content": response.content})
    except Exception as e:
        return jsonify({"error": str(e)})
    


@app.route('/speech_to_text', methods = ['POST'])
def speech_to_text():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    audio_file = request.files['audio_file']
    audio_bytes = io.BytesIO(audio_file.read())

    if audio_file.filename.endswith(".mp3"):
        sound = AudioSegment.from_file(audio_bytes, format="mp3")
    if audio_file.filename.lower().endswith('.m4a'):
        sound = AudioSegment.from_file(audio_bytes, format="m4a")
    sound = AudioSegment.from_file(audio_bytes)

    audio_bytes = io.BytesIO()
    sound.export(audio_bytes, format="wav")
    audio_bytes.seek(0)

    
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_bytes) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='ar-SA')
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand the audio"}), 400
        except sr.RequestError:
            return jsonify({"error": "Google API not available"}), 500

    return jsonify({'transcription': text})


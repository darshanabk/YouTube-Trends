import os
import re
import html
import emoji
import streamlit as st
import pandas as pd
from datetime import datetime
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import whisper
from google.generativeai import GenerativeModel, configure

# Set your API keys
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
configure(api_key=GEMINI_API_KEY)

openai.api_key = st.secrets["OPENAI_API_KEY"]
whisper_model = whisper.load_model("base")

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([^&]+)", url)
    return match.group(1) if match else None

def datacleaning(text: str) -> str:
    text = emoji.replace_emoji(text, replace='')
    text = html.unescape(text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fetch_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        english_transcripts = [t.language_code for t in transcript_list if t.language_code.startswith('en')]
        if english_transcripts:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            transcript_text = " ".join([t['text'] for t in transcript])
            return datacleaning(transcript_text)
        else:
            return None
    except:
        return None

def download_audio(video_id, output_dir="audio"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{video_id}_{timestamp}.mp4"
    output_path = os.path.join(output_dir, filename)

    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(filename=output_path)
        return output_path
    except Exception as e:
        st.error(f"Audio download failed: {e}")
        return None

def whisper_transcribe(audio_path):
    try:
        result = whisper_model.transcribe(audio_path)
        return datacleaning(result['text'])
    except Exception as e:
        st.error(f"Whisper transcription failed: {e}")
        return None

def summarize_with_any_model(text):
    # List of Gemini models to try
    gemini_models = [
        "models/gemini-1.5-pro", "models/gemini-1.5-pro-001", "models/gemini-1.5-pro-002",
        "models/gemini-1.5-flash", "models/gemini-1.5-flash-latest", "models/gemini-1.5-flash-001",
        "models/gemini-2.0-flash", "models/gemini-2.0-pro-exp", "models/gemini-2.0-flash-001"
    ]

    # Try Gemini models first
    for model_name in gemini_models:
        try:
            model = GenerativeModel(model_name)
            gemini_response = model.generate_content(f"Summarize the following transcript:\n\n{text}")
            return  gemini_response.text
        except Exception as gemini_error:
            st.warning(f"Gemini model {model_name} failed. Trying next...")

    st.warning("All Gemini models failed. Falling back to OpenAI...")

    # Try OpenAI GPT-4
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Summarize the following transcript."},
                      {"role": "user", "content": text}],
            max_tokens=1024,
            temperature=0.7
        )
        return "[GPT-4] " + response.choices[0].message.content.strip()
    except Exception as gpt4_error:
        st.warning("GPT-4 failed. Trying GPT-3.5...")

    # Fallback to GPT-3.5
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Summarize the following transcript."},
                      {"role": "user", "content": text}],
            max_tokens=1024,
            temperature=0.7
        )
        return "[GPT-3.5] " + response.choices[0].message.content.strip()
    except Exception as gpt35_error:
        st.error("All summarization models failed. Please try again later.")
        return None


# Streamlit UI
st.title("🎬 YouTube Summarizer with Gemini + Whisper")

url = st.text_input("Enter YouTube URL:")

if url:
    video_id = extract_video_id(url)
    if not video_id:
        st.error("Invalid YouTube URL.")
    else:
        st.info("Processing...")
        transcript = fetch_transcript(video_id)

        if transcript:
            st.success("Transcript fetched successfully!")
        else:
            st.warning("Transcript not available. Downloading audio and using Whisper...")
            audio_path = download_audio(video_id)
            if audio_path:
                transcript = whisper_transcribe(audio_path)
                if transcript:
                    st.success("Audio transcribed successfully using Whisper!")

        if transcript:
            st.subheader("📄 Transcript")
            st.write(transcript[:3000])  # Display part of it

            st.subheader("🧠 Summary")
            summary = summarize_with_any_model(transcript)
            st.write(summary)
        else:
            st.error("Could not extract transcript or transcribe audio.")

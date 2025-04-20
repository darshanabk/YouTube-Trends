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

def summarize_with_gemini(text):
    model = GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(
        f"Summarize the following transcript:\n\n{text}"
    )
    return response.text

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

            st.subheader("🧠 Gemini Summary")
            summary = summarize_with_gemini(transcript)
            st.write(summary)
        else:
            st.error("Could not extract transcript or transcribe audio.")

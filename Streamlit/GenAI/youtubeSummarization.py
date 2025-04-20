import os
import re
import html
import emoji
import streamlit as st
import pandas as pd
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
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
    filename = f"{video_id}_{timestamp}.%(ext)s"
    output_path = os.path.join(output_dir, filename)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
    return output_path.replace("%(ext)s", "mp3")

def whisper_transcribe(audio_path):
    result = whisper_model.transcribe(audio_path)
    return result['text']

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
            transcript = whisper_transcribe(audio_path)
            st.success("Audio transcribed successfully using Whisper!")

        st.subheader("📄 Transcript")
        st.write(transcript[:3000])  # Limit for display

        if transcript:
            st.subheader("🧠 Gemini Summary")
            summary = summarize_with_gemini(transcript)
            st.write(summary)

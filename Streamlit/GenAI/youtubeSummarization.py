import streamlit as st
import pandas as pd
import os
import re
import html
import emoji
import tempfile
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract
import yt_dlp
import whisper
from openai import OpenAI

# Whisper model
whisper_model = whisper.load_model("base")  # can also use "small", "medium", "large"

# Extract Video ID from URL
def extract_video_id(url):
    try:
        return extract.video_id(url)
    except Exception:
        return None

# Clean transcript text
def datacleaning(text: str) -> str:
    text = emoji.replace_emoji(text, replace='')
    text = html.unescape(text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Download audio
@st.cache_data(show_spinner=False)
def download_audio(video_id, output_dir="audio"):
    try:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"{video_id}_{timestamp}.%(ext)s"
        filepath = os.path.join(output_dir, filename)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filepath,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])

        return filepath.replace('%(ext)s', 'mp3')
    except Exception as e:
        st.error(f"Error downloading audio: {e}")
        return None

# Transcribe audio with Whisper
@st.cache_data(show_spinner=False)
def audio_to_text_whisper(audio_path):
    try:
        result = whisper_model.transcribe(audio_path)
        return result['text']
    except Exception as e:
        st.error(f"Whisper transcription error: {e}")
        return ""

# Try to get transcript
def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        english_transcripts = [t.language_code for t in transcript_list if t.language_code.startswith('en')]

        if english_transcripts:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[english_transcripts[0]])
            return datacleaning(" ".join([t['text'] for t in transcript]))

        for t in transcript_list:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[t.language_code])
                return datacleaning(" ".join([t['text'] for t in transcript]))
            except:
                continue
    except:
        return None

# Get summary using Gemini API (mocked for now)
def get_summary_gemini(text):
    # Replace this with real Gemini API integration with structured prompt
    return {
        "summary": text[:300] + ("..." if len(text) > 300 else ""),
        "key_points": re.split(r'(?<=[.!?]) +', text[:500])[:5],
        "tags": ["AI", "Video", "Transcript"]
    }

# Streamlit UI
st.title("YouTube Transcript & Audio Summarizer")
youtube_url = st.text_input("Enter YouTube URL")

if youtube_url:
    video_id = extract_video_id(youtube_url)
    if not video_id:
        st.error("Invalid YouTube URL")
    else:
        with st.spinner("Fetching transcript or downloading audio..."):
            transcript = get_transcript(video_id)
            if transcript:
                st.success("Transcript found.")
                input_text = transcript
            else:
                st.warning("No transcript found, downloading audio...")
                audio_path = download_audio(video_id)
                if audio_path:
                    st.success("Audio downloaded.")
                    input_text = audio_to_text_whisper(audio_path)
                else:
                    input_text = None

        if input_text:
            with st.spinner("Generating structured summary..."):
                summary_data = get_summary_gemini(input_text)

            st.subheader("Structured Summary")
            st.json(summary_data)
        else:
            st.error("Failed to extract or transcribe content.")

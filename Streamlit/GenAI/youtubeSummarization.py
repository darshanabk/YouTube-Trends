import os
import re
import html
import emoji
import streamlit as st
import pandas as pd
from datetime import datetime
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import whisper
from google.generativeai import GenerativeModel, configure
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googlesearch import search


# Set your API keys
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
configure(api_key=GEMINI_API_KEY)

openai.api_key = st.secrets["OPENAI_API_KEY"]

# YouTube Data API v3 setup
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([^&]+)", url)
    return match.group(1) if match else None


def datacleaning(text: str) -> str:
    text = emoji.replace_emoji(text, replace='')  # Remove emojis
    text = html.unescape(text)  # Decode HTML entities
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text


def fetch_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en']).fetch()
        transcript_text = " ".join([t['text'] for t in transcript])
        return datacleaning(transcript_text)
    except Exception:
        return None

def download_and_transcribe(video_id, output_dir="audio"):
    """
    Download YouTube audio in native format (no FFmpeg conversion)
    and transcribe using Whisper
    """
    try:
        # 1. Download audio in native format
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.m4a"
        output_path = os.path.join(output_dir, filename)
        
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]',  # Direct M4A download
            'outtmpl': output_path.replace('.m4a', '.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 30,
            'retries': 3
        }
        
        with st.spinner(f"🎧 Downloading audio for {video_id}..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"https://youtube.com/watch?v={video_id}"])
        
        # Verify download
        if not os.path.exists(output_path):
            st.error("Download completed but file not found")
            return None, None

        # 2. Transcribe with Whisper (no FFmpeg needed)
        with st.spinner("🔊 Transcribing with Whisper..."):
            model = whisper.load_model("base")
            result = model.transcribe(output_path)
            return output_path, result['text']
            
    except Exception as e:
        st.error(f"Processing failed: {str(e)}")
        return None, None




def search_and_summarize(title, description):
    try:
        query = f"{title} {description}"
        search_results = search(query, num_results=3)
        web_content = ""
        for url in search_results:
            web_content += f"\nURL: {url}\nExtracted Content: This is a top search result related to the title and description.\n"

        prompt = f"""
You are a helpful assistant. Based on the following YouTube video metadata and search results, generate a concise summary:

Title: {title}
Description: {description}

Search Result Context:
{web_content}

Summarize the content above in 5-7 sentences focusing on the key takeaways or subject matter.
"""
        # Use Gemini or fallback to GPT
        summary = summarize_with_any_model(prompt)
        return summary

    except Exception as e:
        st.error(f"Error searching the web: {e}")
        return None


def fetch_metadata_youtube_api(video_id):
    try:
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()
        title = response['items'][0]['snippet']['title']
        description = response['items'][0]['snippet']['description']
        return title, description
    except HttpError as e:
        st.warning(f"YouTube API metadata fetch failed: {e}")
        return None, None


def summarize_with_any_model(text):
    gemini_models = [
        "models/gemini-1.5-pro", "models/gemini-1.5-pro-001", "models/gemini-1.5-pro-002",
        "models/gemini-1.5-flash", "models/gemini-1.5-flash-latest", "models/gemini-1.5-flash-001",
        "models/gemini-2.0-flash", "models/gemini-2.0-pro-exp", "models/gemini-2.0-flash-001"
    ]
    for model_name in gemini_models:
        try:
            model = GenerativeModel(model_name)
            with st.spinner(f"Trying Gemini model: {model_name}"):
                gemini_response = model.generate_content(f"Summarize the following transcript:\n\n{text}")
            return gemini_response.text
        except Exception:
            st.warning(f"Gemini model {model_name} failed.")

    st.warning("All Gemini models failed. Trying OpenAI GPT...")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Summarize the following transcript."},
                {"role": "user", "content": text}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        return "[GPT-4] " + response.choices[0].message.content.strip()
    except Exception:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Summarize the following transcript."},
                    {"role": "user", "content": text}
                ],
                max_tokens=1024,
                temperature=0.7
            )
            return "[GPT-3.5] " + response.choices[0].message.content.strip()
        except Exception as e:
            st.error("All summarization models failed.")
            return None

# Example usage in your Streamlit UI:

# --- Streamlit UI ---
st.set_page_config(page_title="YouTube Summarizer Pro", layout="centered")
st.title("🎬 YouTube Summarizer Pro")

url = st.text_input("Enter YouTube URL:")

if url:
    video_id = url.split("v=")[-1].split("&")[0]  # Simple ID extraction
    if not video_id:
        st.error("Invalid YouTube URL")
    else:
        # Try direct transcript first
        transcript = fetch_transcript(video_id)  # Your existing function
        
        if not transcript:
            # Fallback to audio transcription
            audio_path, transcript = download_and_transcribe(video_id)
            
            if audio_path:
                st.audio(audio_path)
                
            if not transcript:
                # Final fallback to metadata
                title, description = fetch_metadata_youtube_api(video_id)
                if title and description:
                    transcript = f"Title: {title}\n\nDescription: {description}"
        
        # Display results
        if transcript:
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("📜 Full Transcript"):
                    st.write(transcript)
            with col2:
                summary = summarize_with_any_model(transcript)
                st.subheader("🧠 Summary")
                st.write(summary or "Summary unavailable")

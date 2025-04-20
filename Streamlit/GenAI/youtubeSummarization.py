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


def download_audio(video_id, output_dir="audio"):
    try:
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]',  # Downloads YouTube's native audio
            'outtmpl': os.path.join(output_dir, f'{video_id}.%(ext)s'),
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://youtube.com/watch?v={video_id}", download=True)
            filename = ydl.prepare_filename(info)
            
        with open(filename, "rb") as f:
            st.download_button(
                label="⬇️ Download Audio",
                data=f,
                file_name=os.path.basename(filename),
                mime="audio/mp4"  # M4A uses mp4 MIME type
            )
        return filename
        
    except Exception as e:
        # st.error(f"Download failed: {str(e)}")
        st.error(f"Download failed")
        return None




def whisper_transcribe(audio_path):
    try:
        with st.spinner("Transcribing with Whisper..."):
            whisper_model = whisper.load_model("base")
            result = whisper_model.transcribe(audio_path)
            return datacleaning(result['text'])
    except Exception as e:
        st.error(f"Whisper transcription failed: {e}")
        return None


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


# --- Streamlit UI ---
st.set_page_config(page_title="YouTube Summarizer", layout="centered")
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
            st.warning("Transcript not available. Trying audio transcription...")
            audio_path = download_audio(video_id)
            if audio_path:
                transcript = whisper_transcribe(audio_path)
                if transcript:
                    st.success("Audio transcribed successfully!")
        
        if not transcript:
            st.warning("Audio unavailable. Fetching metadata and searching the web...")
            title, description = fetch_metadata_youtube_api(video_id)

            if title and description:
                metadata_text = f"**Title:** {title}\n\n**Description:** {description}"
                st.write(metadata_text)

                web_summary = search_and_summarize(title, description)
                if web_summary:
                    st.subheader("🧠 Web Search Summary")
                    st.write(web_summary)
        else:
            st.subheader("📄 Transcript")
            with st.expander("Click to expand full transcript"):
                st.write(transcript)

            st.subheader("🧠 Summary")
            summary = summarize_with_any_model(transcript)
            if summary:
                st.write(summary)
            else:
                st.error("Summarization failed.")

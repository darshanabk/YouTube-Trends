import os
import re
import html
import emoji
import streamlit as st
from datetime import datetime
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import whisper
from google.generativeai import GenerativeModel, configure
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googlesearch import search

# --- Configuration ---
def setup_apis():
    """Initialize all API clients with error handling"""
    try:
        # Set API keys from Streamlit secrets
        configure(api_key=st.secrets["GEMINI_API_KEY"])
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        youtube = build("youtube", "v3", developerKey=st.secrets["YOUTUBE_API_KEY"])
        return youtube
    except Exception as e:
        st.error(f"API initialization failed: {str(e)}")
        return None

youtube = setup_apis()

# --- Core Functions ---
def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r"(?:v=|youtu\.be/)([^&]+)",  # Standard URLs
        r"embed/([^?]+)",              # Embed URLs
        r"shorts/([^?]+)"              # Shorts URLs
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def clean_text(text: str) -> str:
    """Clean text by removing emojis, HTML entities, and non-ASCII characters"""
    if not isinstance(text, str):
        return ""
    text = emoji.replace_emoji(text, replace='')
    text = html.unescape(text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def get_transcript(video_id: str) -> str:
    """Fetch transcript with fallback to different languages"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try English variants first
        for lang in ['en', 'en-US', 'en-GB', 'en-AU']:
            try:
                transcript = transcript_list.find_transcript([lang]).fetch()
                return " ".join([t['text'] for t in transcript])
            except:
                continue
                
        # Fallback to any available transcript
        transcript = transcript_list.find_manually_created_transcript().fetch()
        return " ".join([t['text'] for t in transcript])
        
    except Exception as e:
        st.warning(f"Transcript unavailable: {str(e)}")
        return None

def download_audio(video_id: str, output_dir: str = "audio") -> str:
    """Download audio with robust error handling"""
    try:
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.m4a"
        output_path = os.path.join(output_dir, filename)
        
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]',
            'outtmpl': output_path.replace('.m4a', '.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 30,
            'retries': 3
        }
        
        with st.spinner(f"Downloading audio for {video_id}..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"https://youtube.com/watch?v={video_id}"])
        
        return output_path if os.path.exists(output_path) else None
        
    except Exception as e:
        st.error(f"Audio download failed: {str(e)}")
        return None

def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio with configurable model size"""
    try:
        model_size = st.selectbox(
            "Select Whisper model", 
            ["tiny", "base", "small", "medium", "large"],
            index=1
        )
        
        with st.spinner(f"Loading Whisper {model_size} model..."):
            model = whisper.load_model(model_size)
            
        with st.spinner("Transcribing audio..."):
            result = model.transcribe(audio_path)
            
        return clean_text(result['text'])
        
    except Exception as e:
        st.error(f"Transcription failed: {str(e)}")
        return None

# --- Summarization Functions ---
def generate_summary(text: str, model_type: str = "gemini") -> str:
    """Generate summary using selected model"""
    try:
        if model_type == "gemini":
            model = GenerativeModel("models/gemini-1.5-pro")
            response = model.generate_content(
                f"Create a concise 5-7 sentence summary of this content:\n\n{text}"
            )
            return clean_text(response.text)
            
        elif model_type == "openai":
            model = "gpt-4" if "gpt-4" in openai.Model.list() else "gpt-3.5-turbo"
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Summarize in 5-7 concise sentences."},
                    {"role": "user", "content": text}
                ],
                temperature=0.7
            )
            return clean_text(response.choices[0].message.content)
            
    except Exception as e:
        st.warning(f"{model_type} failed: {str(e)}")
        return None

# --- Streamlit UI ---
def main():
    st.set_page_config(page_title="YouTube Summarizer Pro", layout="wide")
    st.title("🎬 YouTube Summarizer Pro")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")
        
    with col2:
        model_choice = st.selectbox("Summary Model", ["Gemini", "OpenAI"], index=0)
    
    if url and st.button("Generate Summary"):
        with st.spinner("Processing..."):
            video_id = extract_video_id(url)
            if not video_id:
                st.error("Invalid YouTube URL")
                return
                
            # Try transcript first
            transcript = get_transcript(video_id)
            
            # Fallback to audio transcription
            if not transcript:
                audio_path = download_audio(video_id)
                if audio_path:
                    st.audio(audio_path)
                    transcript = transcribe_audio(audio_path)
            
            # Final fallback to metadata
            if not transcript:
                try:
                    title, description = fetch_metadata_youtube_api(video_id)
                    transcript = f"Title: {title}\n\nDescription: {description}"
                    st.warning("Using video metadata only")
                except:
                    st.error("Could not retrieve any content")
                    return
            
            # Display results
            with st.expander("📜 Full Transcript", expanded=False):
                st.write(transcript)
                
            summary = generate_summary(transcript, model_type=model_choice.lower())
            if summary:
                st.subheader("📝 Summary")
                st.write(summary)
                
                # Additional features
                with st.expander("🔍 Key Insights"):
                    insights = generate_summary(transcript, model_type="gemini")
                    st.write(insights or "No insights generated")
                    
                with st.expander("📌 Chapter Markers"):
                    chapters = generate_chapters(transcript)
                    st.write(chapters or "No chapters detected")

if __name__ == "__main__":
    main()

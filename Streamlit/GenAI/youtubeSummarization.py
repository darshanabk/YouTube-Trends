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
    text = emoji.replace_emoji(text, replace='')
    text = html.unescape(text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
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
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{video_id}_{timestamp}.mp3"
    output_path = os.path.join(output_dir, filename)
    try:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
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
            ydl.download([video_url])
        return output_path
    except Exception as e:
        st.error(f"Audio download failed: {e}")
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


# def search_and_summarize(query, title, description):
#     try:
#         # Perform a web search using the query
#         search_results = search(query, num_results=3)
#         web_content = f"**Title:** {title}\n**Description:** {description}\n\n"
        
#         # Collect relevant URLs and extract basic content for summarization
#         for url in search_results:
#             web_content += f"URL: {url}\nExtracted Content: {url}\n\n"
        
#         # Now summarize this combined content using Gemini or OpenAI
#         web_summary = summarize_with_any_model(web_content)
#         return web_summary
#     except Exception as e:
#         st.error(f"Error searching the web: {e}")
#         return None

def search_and_summarize(query, title, description):
    try:
        # Perform a web search using the query
        search_results = search(query, num_results=3)
        
        # Start constructing the input for the summarization model
        web_content = f"**Title:** {title}\n**Description:** {description}\n\n"
        
        # Collect relevant URLs and their extracted content for summarization
        for url in search_results:
            web_content += f"URL: {url}\nExtracted Content: [Placeholder for content extraction from {url}]\n\n"

        # RAG (Retrieval Augmented Generation) and Few-shot prompting:
        # We'll use the search results and example prompts to help the model understand what content to extract and summarize

        # Few-shot prompting setup: provide example contexts and instructions to the AI model
        example_prompt = """
        You are a helpful assistant. Here's how you should summarize web content:

        - Read the title, description, and extracted content from the web pages.
        - Identify the key points, trends, or main topics discussed in the content.
        - Provide a concise summary of the content, adding relevant context from the title and description.

        Here are the details to summarize:
        """

        # Add the example prompt and web-based content
        model_input = example_prompt + web_content
        
        # Use either Gemini or OpenAI for summarization
        web_summary = summarize_with_any_model(model_input)
        
        return web_summary
    except Exception as e:
        st.error(f"Error searching the web: {e}")
        return None

def fetch_metadata_yt_dlp(url):
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', 'No title found')
            description = info_dict.get('description', 'No description found')
            return title, description
    except Exception as e:
        st.warning(f"yt-dlp metadata fetch failed: {e}")
        return None, None


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
    
    # First try Gemini models
    for model_name in gemini_models:
        try:
            model = GenerativeModel(model_name)
            with st.spinner(f"Trying Gemini model: {model_name}"):
                gemini_response = model.generate_content(f"Summarize the following content:\n\n{text}")
            return gemini_response.text
        except Exception:
            st.warning(f"Gemini model {model_name} failed.")

    # If Gemini models fail, try OpenAI GPT-4 and fallback to GPT-3.5
    st.warning("All Gemini models failed. Trying OpenAI GPT...")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Summarize the following content."},
                      {"role": "user", "content": text}],
            max_tokens=1024,
            temperature=0.7
        )
        return "[GPT-4] " + response.choices[0].message.content.strip()
    except Exception:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Summarize the following content."},
                          {"role": "user", "content": text}],
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

        # Fetch transcript or audio transcription
        transcript = fetch_transcript(video_id)
        
        if transcript:
            st.success("Transcript fetched successfully!")
        else:
            st.warning("Transcript not available. Fetching metadata and searching the web...")            

            title, description = fetch_metadata_yt_dlp(url)
            if not title or not description:
                title, description = fetch_metadata_youtube_api(video_id)

            # if title and description:
            #     metadata_text = f"**Title:** {title}\n\n**Description:** {description}"
            #     st.write(metadata_text)

                # Use metadata + search results for summarization
                web_search_summary = search_and_summarize(f"{title} {description}", title, description)
                if web_search_summary:
                    st.subheader("🧠 Web Search Summary")
                    st.write(web_search_summary)
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

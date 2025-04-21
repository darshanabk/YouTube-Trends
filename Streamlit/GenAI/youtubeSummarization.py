# import os
# import re
# import html
# import emoji
# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import yt_dlp
# from youtube_transcript_api import YouTubeTranscriptApi
# import openai
# import whisper
# from google.generativeai import GenerativeModel, configure
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from googlesearch import search


# # Set your API keys
# GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
# configure(api_key=GEMINI_API_KEY)

# openai.api_key = st.secrets["OPENAI_API_KEY"]

# # YouTube Data API v3 setup
# YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
# youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


# def extract_video_id(url):
#     match = re.search(r"(?:v=|youtu\.be/)([^&]+)", url)
#     return match.group(1) if match else None


# def datacleaning(text: str) -> str:
#     text = emoji.replace_emoji(text, replace='')  # Remove emojis
#     text = html.unescape(text)  # Decode HTML entities
#     text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
#     text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
#     return text


# def fetch_transcript(video_id):
#     try:
#         transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
#         transcript = transcript_list.find_transcript(['en']).fetch()
#         transcript_text = " ".join([t['text'] for t in transcript])
#         return datacleaning(transcript_text)
#     except Exception:
#         return None


# # def download_audio(video_id, output_dir="audio"):
# #     os.makedirs(output_dir, exist_ok=True)
# #     timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# #     filename = f"{video_id}_{timestamp}.mp3"
# #     output_path = os.path.join(output_dir, filename)
# #     try:
# #         video_url = f"https://www.youtube.com/watch?v={video_id}"
# #         ydl_opts = {
# #             'format': 'bestaudio/best',
# #             'outtmpl': output_path,
# #             'postprocessors': [{
# #                 'key': 'FFmpegExtractAudio',
# #                 'preferredcodec': 'mp3',
# #                 'preferredquality': '192',
# #             }],
# #         }
# #         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
# #             ydl.download([video_url])
# #         return output_path
# #     except Exception as e:
# #         # st.error(f"Audio download failed: {e}")
# #         return None

# # def download_audio(video_id, output_dir="audio"):
# #     """Download YouTube audio in native format without FFmpeg conversion"""
# #     try:
# #         os.makedirs(output_dir, exist_ok=True)
# #         timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
# #         # Use native M4A format (no conversion needed)
# #         filename = f"{video_id}_{timestamp}.m4a"
# #         output_path = os.path.join(output_dir, filename)
        
# #         ydl_opts = {
# #             'format': 'bestaudio[ext=m4a]',  # Directly download M4A format
# #             'outtmpl': output_path.replace('.m4a', '.%(ext)s'),  # Preserve extension
# #             'quiet': True,
# #             'no_warnings': True,
# #             'socket_timeout': 30,
# #             'retries': 3
# #         }
        
# #         with st.spinner(f"Downloading audio for {video_id}..."):
# #             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
# #                 ydl.download([f"https://youtube.com/watch?v={video_id}"])
        
# #         # Verify download completed
# #         if os.path.exists(output_path):
# #             return output_path
# #         return None
        
# #     except Exception as e:
# #         # st.error(f"Audio download failed: {str(e)}")
# #         return None


# # def whisper_transcribe(audio_path):
# #     try:
# #         with st.spinner("Transcribing with Whisper..."):
# #             whisper_model = whisper.load_model("base")
# #             result = whisper_model.transcribe(audio_path)
# #             return datacleaning(result['text'])
# #     except Exception as e:
# #         st.error(f"Whisper transcription failed: {e}")
# #         return None

# def get_audio_transcription(video_id, output_dir="audio"):
#     """Combined function to download audio and transcribe with Whisper"""
#     try:
#         # 1. Download audio
#         audio_path = download_audio(video_id, output_dir)
#         if not audio_path or not os.path.exists(audio_path):
#             st.warning("Audio download failed")
#             return None

#         # 2. Transcribe with Whisper
#         with st.spinner("Transcribing with Whisper..."):
#             # Let user select model size
#             model_size = st.selectbox(
#                 "Select Whisper model size",
#                 ["tiny", "base", "small", "medium", "large"],
#                 index=1,
#                 key=f"whisper_{video_id}"
#             )
            
#             model = whisper.load_model(model_size)
#             result = model.transcribe(audio_path)
            
#             # Clean and return text
#             return datacleaning(result['text'])

#     except Exception as e:
#         st.error(f"Audio transcription failed: {str(e)}")
#         return None


# def search_and_summarize(title, description):
#     try:
#         query = f"{title} {description}"
#         search_results = search(query, num_results=3)
#         web_content = ""
#         for url in search_results:
#             web_content += f"\nURL: {url}\nExtracted Content: This is a top search result related to the title and description.\n"

#         prompt = f"""
# You are a helpful assistant. Based on the following YouTube video metadata and search results, generate a concise summary:

# Title: {title}
# Description: {description}

# Search Result Context:
# {web_content}

# Summarize the content above in 5-7 sentences focusing on the key takeaways or subject matter.
# """
#         # Use Gemini or fallback to GPT
#         summary = summarize_with_any_model(prompt)
#         return summary

#     except Exception as e:
#         st.error(f"Error searching the web: {e}")
#         return None


# def fetch_metadata_youtube_api(video_id):
#     try:
#         request = youtube.videos().list(part="snippet", id=video_id)
#         response = request.execute()
#         title = response['items'][0]['snippet']['title']
#         description = response['items'][0]['snippet']['description']
#         return title, description
#     except HttpError as e:
#         st.warning(f"YouTube API metadata fetch failed: {e}")
#         return None, None


# def summarize_with_any_model(text):
#     gemini_models = [
#         "models/gemini-1.5-pro", "models/gemini-1.5-pro-001", "models/gemini-1.5-pro-002",
#         "models/gemini-1.5-flash", "models/gemini-1.5-flash-latest", "models/gemini-1.5-flash-001",
#         "models/gemini-2.0-flash", "models/gemini-2.0-pro-exp", "models/gemini-2.0-flash-001"
#     ]
#     for model_name in gemini_models:
#         try:
#             model = GenerativeModel(model_name)
#             with st.spinner(f"Trying Gemini model: {model_name}"):
#                 gemini_response = model.generate_content(f"Summarize the following transcript:\n\n{text}")
#             return gemini_response.text
#         except Exception:
#             st.warning(f"Gemini model {model_name} failed.")

#     st.warning("All Gemini models failed. Trying OpenAI GPT...")

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "Summarize the following transcript."},
#                 {"role": "user", "content": text}
#             ],
#             max_tokens=1024,
#             temperature=0.7
#         )
#         return "[GPT-4] " + response.choices[0].message.content.strip()
#     except Exception:
#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "Summarize the following transcript."},
#                     {"role": "user", "content": text}
#                 ],
#                 max_tokens=1024,
#                 temperature=0.7
#             )
#             return "[GPT-3.5] " + response.choices[0].message.content.strip()
#         except Exception as e:
#             st.error("All summarization models failed.")
#             return None


# # --- Streamlit UI ---
# st.set_page_config(page_title="YouTube Summarizer", layout="centered")
# st.title("🎬 YouTube Summarizer with Gemini + Whisper")

# url = st.text_input("Enter YouTube URL:")

# if url:
#     video_id = extract_video_id(url)
#     if not video_id:
#         st.error("Invalid YouTube URL.")
#     else:
#         st.info("Processing...")
#         transcript = fetch_transcript(video_id)

#         if transcript:
#             st.success("Transcript fetched successfully!")
#         else:
#             st.warning("Transcript not available. Trying audio transcription...")
#             transcript = get_audio_transcription(video_id)
#             # if audio_path:
#             #     transcript = whisper_transcribe(audio_path)
#             if transcript:
#                 st.success("Audio transcribed successfully!")
        
#         if not transcript:
#             st.warning("Audio unavailable. Fetching metadata and searching the web...")
#             title, description = fetch_metadata_youtube_api(video_id)

#             if title and description:
#                 metadata_text = f"**Title:** {title}\n\n**Description:** {description}"
#                 st.write(metadata_text)

#                 web_summary = search_and_summarize(title, description)
#                 if web_summary:
#                     st.subheader("🧠 Web Search Summary")
#                     st.write(web_summary)
#         else:
#             st.subheader("📄 Transcript")
#             with st.expander("Click to expand full transcript"):
#                 st.write(transcript)

#             st.subheader("🧠 Summary")
#             summary = summarize_with_any_model(transcript)
#             if summary:
#                 st.write(summary)
#             else:
#                 st.error("Summarization failed.")


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


# def download_audio(video_id, output_dir="audio"):
#     os.makedirs(output_dir, exist_ok=True)
#     timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#     filename = f"{video_id}_{timestamp}.mp3"
#     output_path = os.path.join(output_dir, filename)
#     try:
#         video_url = f"https://www.youtube.com/watch?v={video_id}"
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'outtmpl': output_path,
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#         }
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([video_url])
#         return output_path
#     except Exception as e:
#         # st.error(f"Audio download failed: {e}")
#         return None


# def whisper_transcribe(audio_path):
#     try:
#         with st.spinner("Transcribing with Whisper..."):
#             whisper_model = whisper.load_model("base")
#             result = whisper_model.transcribe(audio_path)
#             return datacleaning(result['text'])
#     except Exception as e:
#         st.error(f"Whisper transcription failed: {e}")
#         return None

def download_audio(video_id):
    """Download YouTube audio in native format to a temporary location"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"{video_id}_{timestamp}.%(ext)s"
        output_path = f"/tmp/{filename}"  # Use Streamlit's temporary path

        video_url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,  # Save to /tmp/
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 30,
            'retries': 3
        }

        with st.spinner(f"Downloading audio for {video_id}..."):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                actual_path = ydl.prepare_filename(info)  # This resolves final filename with extension

        return actual_path if os.path.exists(actual_path) else None

    except Exception as e:
        st.error(f"Audio download failed: {str(e)}")
        return None


def whisper_transcribe(audio_path):
    try:
        with st.spinner("Transcribing with Whisper..."):
            # Load appropriate model based on audio length
            audio_duration = get_audio_duration(audio_path)
            model_size = "base" if audio_duration < 600 else "small"  # Use larger model for longer audio
            
            model = whisper.load_model(model_size)
            result = model.transcribe(audio_path)
            
            # Clean and return text
            return datacleaning(result['text'])
            
    except Exception as e:
        st.error(f"Transcription failed: {str(e)}")
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




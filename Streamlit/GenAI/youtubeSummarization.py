import streamlit as st
import pandas as pd
import os
import re
import html
import emoji
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def datacleaning(text: str) -> str:
    text = emoji.replace_emoji(text, replace='')
    text = html.unescape(text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def Transcript(df, api_key):
    for index, row in df.iterrows():
        video_id = row['videoId']
        df.at[index, 'videoTranscript'] = None
        df.at[index, 'videoTranscriptLog'] = ""
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            english_transcripts = [t.language_code for t in transcript_list if t.language_code.startswith('en')]
            df.at[index, 'videoTranscriptLog'] +=(f"english:{english_transcripts}. ")
            
            transcript_text = ""
            for lang in (['en'] + english_transcripts):
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                    transcript_text = " ".join([t['text'] for t in transcript])
                    if transcript_text.strip():
                        break
                except:
                    continue

            if not transcript_text:
                available_langs = [t.language_code for t in transcript_list]
                for lang in available_langs:
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                        transcript_text = " ".join([t['text'] for t in transcript])
                        if transcript_text.strip():
                            break
                    except:
                        continue

            if transcript_text.strip():
                df.at[index, 'videoTranscript'] = datacleaning(transcript_text)
            else:
                df.at[index, 'videoTranscriptLog'] += 'No usable transcript found.'

        except Exception as e:
            df.at[index, 'videoTranscriptLog'] += (f"Error getting transcript: {str(e)} ")

    return df

def download_audio(video_id, output_dir="audio"):
    try:
        os.makedirs(output_dir, exist_ok=True)
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"{video_id}_{timestamp}.%(ext)s"
        filepath = os.path.join(output_dir, filename.replace('%(ext)s', 'mp3'))

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, filename),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return filepath
    except Exception as e:
        return None

def transcribe_audio_with_gemini(audio_path):
    try:
        uploaded_file = genai.upload_file(audio_path, mime_type="audio/mp3")
        model_vision = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        response = model_vision.generate_content([
            "Please transcribe this audio to text.",
            uploaded_file
        ])
        return response.text
    except Exception as e:
        return f"Error in audio transcription: {str(e)}"

def get_structured_summary(transcript_text):
    prompt = f"""
    Summarize the transcript below into:
    - Title
    - Key topics
    - Actionable insights
    - Target audience
    Transcript:
    {transcript_text}
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def few_shot_summary(transcript_text):
    prompt = f"""
    Based on this transcript, write a short summary as if you're explaining it to someone in a tweet:
    {transcript_text}
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def rag_summary(transcript_text):
    prompt = f"""
    Use RAG-like reasoning: First retrieve major facts from this transcript, then generate a thoughtful summary.
    {transcript_text}
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# ---------- Streamlit App -------------
st.set_page_config(page_title="YouTube Transcript Summarizer", layout="wide")
st.title("🎥 YouTube Transcript + Gemini Audio-to-Text")

video_url = st.text_input("Enter YouTube Video URL:")

if video_url:
    try:
        video_id = video_url.split("v=")[-1].split("&")[0]
        df = pd.DataFrame({'videoId': [video_id]})

        df = Transcript(df, api_key=os.getenv("GOOGLE_API_KEY"))
        transcript = df.loc[0, 'videoTranscript']

        if transcript:
            st.success("Transcript fetched successfully!")
            st.markdown("### Transcript Preview")
            st.write(transcript[:500] + "...")

            st.info("Generating summaries using Gemini...")
            structured = get_structured_summary(transcript)
            few_shot = few_shot_summary(transcript)
            rag = rag_summary(transcript)

            st.subheader("📦 Structured Summary")
            st.json(structured)

            st.subheader("✍️ Few-shot Summary")
            st.write(few_shot)

            st.subheader("📚 RAG Summary")
            st.write(rag)

        else:
            st.warning("No transcript available. Trying audio transcription via Gemini...")
            audio_path = download_audio(video_id)

            if audio_path:
                st.info("Audio downloaded. Transcribing with Gemini...")
                transcript = transcribe_audio_with_gemini(audio_path)

                if transcript:
                    st.success("Transcript from audio generated.")
                    st.markdown("### Transcript Preview")
                    st.write(transcript[:500] + "...")

                    st.info("Generating summaries using Gemini...")
                    structured = get_structured_summary(transcript)
                    few_shot = few_shot_summary(transcript)
                    rag = rag_summary(transcript)

                    st.subheader("📦 Structured Summary")
                    st.json(structured)

                    st.subheader("✍️ Few-shot Summary")
                    st.write(few_shot)

                    st.subheader("📚 RAG Summary")
                    st.write(rag)
                else:
                    st.error("Failed to transcribe audio.")
            else:
                st.error("Audio download failed.")

    except Exception as e:
        st.error(f"Error processing video: {str(e)}")

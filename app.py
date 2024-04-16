import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define prompt
prompt = """You are YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 1000 words. Please provide the summary of the text given here:  """

# Getting the transcript data from YouTube videos
def extract_transcript_details(youtube_video_url, language="en"):
    try:
        video_id = youtube_video_url.split("=")[1]
        print(video_id)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e


# Getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


# Main function to render the Streamlit app
def main():
    # Set page background color to red
    st.markdown(
        """
        <style>
        body {
            background-color: red;
            color: white;
        }
        .reportview-container .main .block-container {
            background-color: #f2f2f2;
            color: #1f1f1f;
        }
        .stTextInput>div>div>div>input::placeholder {
            color: #ffffff;
        }
        .stButton>button {
            background-color: #008000;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("YouTube Transcript to Detailed Notes Converter")

    youtube_link = st.text_input("Enter YouTube Video Link:")

    languages = ["English", "Spanish", "French", "German", "Hindi", "Other"]
    language = st.selectbox("Select Language:", languages)

    if language == "Other":
        language_code = st.text_input("Enter Language Code (e.g., 'es' for Spanish):")
    else:
        language_mapping = {"English": "en", "Spanish": "es", "French": "fr", "German": "de", "Hindi": "hi"}
        language_code = language_mapping[language]

    if youtube_link:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    if st.button("Get Summary"):
        if youtube_link:
            try:
                transcript_text = extract_transcript_details(youtube_link, language_code)
                if transcript_text:
                    summary = generate_gemini_content(transcript_text, prompt)
                    st.markdown("## Detailed Notes:")
                    st.write(summary)
                else:
                    st.write("Transcript not available for the provided video or language.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid YouTube video link.")


if __name__ == "__main__":
    main()

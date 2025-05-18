import streamlit as st
from dotenv import load_dotenv
load_dotenv() #load all the environment variables from the .env file
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import os
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) #set the api key for google generative ai

prompt="""You are Youtube video summarizer. You will be taking the transcript text and summarizing the entire video and providing the important summary in points
within 350 words.Please provide the summary of the text given here:"""

def extract_transcript_details(youtube_video_url):
    try:
        video_id= youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id) # will be in the form of list of dictionaries
        # print(transcript_text)
        transcript =""
        for i in transcript_text: #convert the list of dictionaries to a single string
            transcript += i['text']+" "
        return transcript
    except Exception as e:
        raise e
    

def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("models/gemini-1.5-flash")
    response=model.generate_content(prompt+transcript_text)
    return response.text
    
st.title("Youtube Transcript to Detailed Notes Converter")
youtube_link=st.text_input("Enter Youtube Video URL")

if youtube_link:
    video_id= youtube_link.split("=")[1]
    st.image(f"https://img.youtube.com/vi/"+video_id+"/0.jpg",use_container_width=True) #display the thumbnail of the video
    
if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)
    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes")
        st.write(summary)

    # def fetch_transcript()
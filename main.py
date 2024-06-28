import streamlit as st
import asyncio
from utility.script.script_generator import generate_script
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals

def add_custom_css():
    st.markdown("""
        <style>
        .main {
            background-color: #060608;
            padding: 20px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        .stTextInput input {
            border-radius: 4px;
            padding: 10px;
            font-size: 16px;
        }
        .stMarkdown {
            font-family: 'Arial', sans-serif;
        }
        .stMarkdown h1 {
            color: #4CAF50;
            font-weight: bold;
        }
        .stMarkdown p {
            font-size: 16px;
            line-height: 1.6;
        }
        .custom-spinner {
            margin: 20px 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        </style>
    """, unsafe_allow_html=True)

def display_title():
    st.markdown("<h1>🎥 Video Generator from Topic</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p>
        Enter a topic and generate a video with corresponding background visuals and captions.
        This tool leverages advanced AI models to create a cohesive and engaging video experience.
        </p>
    """, unsafe_allow_html=True)

def display_input_section():
    topic = st.text_input("Enter a topic for the video", help="Type the topic you want the video to be about")
    return topic

def display_loading_animation():
    st.markdown("""
        <div class="custom-spinner">
            <img src="https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif" width="100">
        </div>
    """, unsafe_allow_html=True)

def generate_video(topic):
    SAMPLE_FILE_NAME = "audio_tts.wav"
    VIDEO_SERVER = "pexel"

    st.write("Generating script...")
    response = generate_script(topic)
    st.write("Script generated: {}".format(response))

    st.write("Generating audio...")
    asyncio.run(generate_audio(response, SAMPLE_FILE_NAME))
    st.write("Audio generated.")

    st.write("Generating timed captions...")
    timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
    #st.write("Timed captions: ", timed_captions)

    st.write("Generating search terms...")
    search_terms = getVideoSearchQueriesTimed(response, timed_captions)
    #st.write("Search terms: ", search_terms)

    background_video_urls = None
    if search_terms is not None:
        st.write("Generating background video URLs...")
        background_video_urls = generate_video_url(search_terms, VIDEO_SERVER)
        #st.write("Background video URLs: ", background_video_urls)
    else:
        st.write("No background video found.")

    background_video_urls = merge_empty_intervals(background_video_urls)

    if background_video_urls is not None:
        st.write("Generating final video...")
        video = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
        st.write("Video generated.")
        st.video(video)
    else:
        st.write("No video generated.")

def main():
    add_custom_css()
    display_title()

    topic = display_input_section()

    if st.button("Generate Video"):
        if not topic:
            st.error("Please enter a topic.")
            return
        
        display_loading_animation()
        generate_video(topic)

if __name__ == "__main__":
    main()

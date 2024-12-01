from main import main
from chatllm import RunLLM
import streamlit as st
from Tools import clear_database,GetVideos

# Clear the database at the start
clear_database()

def ReadJson():
    with open("Informations.json") as f:
        Informations = f.read()
    return Informations

# Configure the Streamlit page
st.set_page_config(layout="wide")

# Sidebar for user input
st.sidebar.title("ScrapYoutuber")
st.sidebar.write("Enter YouTube Handle")

youtube_handle = st.sidebar.text_input("YouTube Handle (Include the @)")

if youtube_handle:
    # Fetch videos as soon as a handle is entered
    Video_metadata = GetVideos(youtube_handle)
    Channel_name = Video_metadata[0]['channel_name']
    st.markdown(f"### Scraping <span style='color:#C6373C;'>{Channel_name}</span> videos",unsafe_allow_html=True)
    # Display videos immediately
    
    for i in range(0, len(Video_metadata), 3):
        cols = st.columns(3)  # Create three columns
        for col, video in zip(cols, Video_metadata[i:i+3]):
            with col:
                st.image(video['thumbnail'], use_container_width=True)
                with st.expander("Video Details"):
                    st.write(f"**Title**: {video['title']}")
                    st.write(f"**Release Date**: {video['release_date']}")
                    st.write(f"[Watch on YouTube]({video['url']})")
    
    if st.sidebar.button("Scrap"):
        with st.spinner("Scraping..."):
            main(youtube_handle)
            st.sidebar.success("Scraping Completed")
            
            Informations = ReadJson()
            Report = RunLLM(Informations)
            st.write(Report.content)

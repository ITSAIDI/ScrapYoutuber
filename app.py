from main import main
from chatllm import RunLLM
import streamlit as st




def ReadJson():
    with open("Informations.json") as f:
        Informations = f.read()
    return Informations



st.set_page_config(layout="wide")

st.sidebar.title("ScrapYoutuber")
st.sidebar.write("Enter Youtube Handle")

youtube_handle = st.sidebar.text_input("Youtube Handle (Include the @)")
if youtube_handle:
    if st.sidebar.button("Scrap"):
        with st.spinner("Scraping..."):
            main(youtube_handle)
            st.sidebar.success("Scraping Completed")
            
            st.write("The youtuber 5 last videos")

            Informations = ReadJson()
            Report = RunLLM(Informations)
            st.write(Report.content)



#main()




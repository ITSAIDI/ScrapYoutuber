from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from tqdm import tqdm
from langchain.schema import Document
from colorama import init, Fore, Back, Style
import shutil


# Initialize colorama
init(autoreset=True)
load_dotenv()
################ Featch Youtube Videos details ################################################
################################################################################################################################

api_key = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)

def resolve_handle_to_channel_id(handle):
    response = youtube.search().list(part='snippet',q=handle,type='channel').execute()
    if 'items' in response and len(response['items']) > 0:
        return response['items'][0]['snippet']['channelId']
    else:
        print(f"Error: No channel found for handle '{handle}'.")
        return None
    
def get_upload_playlist_id(channel_id):
    try:
        response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()

        # Check if 'items' key is present in the response
        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        else:
            print(f"Error: 'items' key not found in response or the channel ID '{channel_id}' may be incorrect.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_latest_videos(playlist_id, max_results=6):
    try:
        response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=max_results
        ).execute()
        return response['items']
    except Exception as e:
        print(f"An error occurred while fetching latest videos: {e}")
        return []

def get_video_details(video_id):
    try:
        response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()
        return response['items'][0]['snippet']
    except Exception as e:
        print(f"An error occurred while fetching video details: {e}")
        return {}

def get_video_transcription(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        # Fetch the first available transcript
        for transcript in transcript_list:
            if transcript.language_code == 'en':
                return " ".join([t['text'] for t in transcript.fetch()])
        return None
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        print(f"An error occurred while fetching video transcription: {e}")
        return None

def Get_Video_Details(handle):
    
    print(Style.BRIGHT + f"Fetching video details for handle '{handle}'...")
    channel_id = resolve_handle_to_channel_id(handle)
    if not channel_id:
        return []

    playlist_id = get_upload_playlist_id(channel_id)
    if not playlist_id:
        return []

    latest_videos = get_latest_videos(playlist_id)
    Documents = []
    for video in tqdm(latest_videos):
        video_id = video['snippet']['resourceId']['videoId']
        video_details = get_video_details(video_id)
        transcription = get_video_transcription(video_id)
        document = Document(
                            page_content=transcription,
                            metadata={
                                        'url'         : f"https://www.youtube.com/watch?v={video_id}",
                                        'title'       : video_details.get('title', 'No title'),
                                        'release_date': video_details.get('publishedAt', 'No date'),
                                    },
                            )
        Documents.append(document)
    return Documents

def GetVideos(Handle):
    Channelid = resolve_handle_to_channel_id(Handle)
    playlistId = get_upload_playlist_id(Channelid)
    Latest_videos = get_latest_videos(playlistId)
    Videos_metadata = []

    for video in Latest_videos:
        video_id = video['snippet']['resourceId']['videoId']
        video_details = get_video_details(video_id)
        
        # Attempt to get higher-quality thumbnails
        thumbnails = video_details.get('thumbnails', {})
        thumbnail_url = (
            thumbnails.get('maxres', {}).get('url') or
            thumbnails.get('standard', {}).get('url') or
            thumbnails.get('high', {}).get('url') or
            thumbnails.get('medium', {}).get('url') or
            thumbnails.get('default', {}).get('url', 'No thumbnail')
        )

        Video_metadata = {
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'title': video_details.get('title', 'No title'),
            'release_date': video_details.get('publishedAt', 'No date'),
            'channel_name': video_details.get('channelTitle', 'No channel name'),
            'thumbnail': thumbnail_url,
        }
        Videos_metadata.append(Video_metadata)

    return Videos_metadata

################ Featch Web Informations ################################################
################################################################################################################################

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults

SERPER_API_KEY = os.getenv('SERPER_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

Serper = GoogleSerperAPIWrapper()
Tavily = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    # include_domains=[...],
    # exclude_domains=[...],
    # name="...",            # overwrite default tool name
    # description="...",     # overwrite default tool description
    # args_schema=...,       # overwrite default args_schema: BaseModel
)

def Get_Web_Details(query):
    print(Style.BRIGHT + f"Fetching Web details for query '{query}'...")
    Documents = []
    document = Document(page_content=Serper.run(query), metadata={"name": "SERPER"})
    Documents.append(document)
    for result in Tavily.invoke({"query": query}):
        document = Document(page_content=result["content"], metadata={"name": "Tavily","url": result["url"]})
        Documents.append(document)
    return Documents

################ RAG ################################################
################################################################################################################################

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_fireworks import FireworksEmbeddings


FIREWORKS_API_KEY = os.getenv('FIREWORKS_API_KEY')
CHROMA_PATH = "Chroma"


#### Chunking Function 
def Split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=400,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(Style.BRIGHT + f"Split {len(documents)} documents into {len(chunks)} chunks.")

    chunk = chunks[1]
    #print(chunk.page_content)
    #print(chunk.metadata)
    print(Style.BRIGHT + f"len(chunk[1])  = {len(chunk.page_content)}")

    return chunks

def Save_to_chroma(documents):
    chunks = Split_text(documents)
    if os.path.exists(CHROMA_PATH):
        db = Chroma(persist_directory=CHROMA_PATH,embedding_function=FireworksEmbeddings(api_key=FIREWORKS_API_KEY))
        print(f"Loaded existing database from {CHROMA_PATH}.")
    else:
        db = Chroma(persist_directory=CHROMA_PATH,embedding_function=FireworksEmbeddings(api_key=FIREWORKS_API_KEY))
        print(f"Created a new database at {CHROMA_PATH}.")
        
    for i in range(0, len(chunks), 200):
        print(Style.BRIGHT + f"Adding {len(chunks[i:i+200])} chunks to the database...")
        batch_chunks = chunks[i:i+200]
        db.add_documents(batch_chunks)
        
    print(Fore.GREEN + f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    print(Style.BRIGHT + f"Total chunks count: {len(db.get()['ids'])}")
 
    

def Search_from_chroma(query,k):
    print(Style.BRIGHT + f"Searching for '{query}' in the database...")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=FireworksEmbeddings(api_key=FIREWORKS_API_KEY))
    results = db.similarity_search_with_relevance_scores(query, k)
    context_text = "\n\n---\n\n".join([chunk.page_content for chunk, _score in results])
    return context_text



def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    print(Style.BRIGHT+Fore.GREEN + f"Deleted the database at {CHROMA_PATH}.")


#clear_database()

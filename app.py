import streamlit as st 
import youtube_dl
from configure import auth_key
import requests
from time import sleep

if 'status' not in st.session_state:
    st.session_state['status'] = 'submitted'

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'ffmpeg-location': './',
    'outtmpl': "./%(id)s.%(ext)s",
}

transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
upload_endpoint = 'https://api.assemblyai.com/v2/upload'

headers_auth_only = {'authorization': auth_key}
headers = {
    "authorization": auth_key,
    "content-type": "application/json"
}
CHUNK_SIZE=5242880

@st.cache
def transcribe_from_link(link, categories):
    _id = link.strip()

    def get_vid(_id):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(_id)

    meta = get_vid(_id)
    save_location = meta['id'] + ".mp3"

    print('Save mp3 to', save_location)

    def read_file(filename):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    # upload audio file to assemblyai
    upload_response = requests.post(
        upload_endpoint,
        headers=headers_auth_only,
        data=read_file(save_location))

    audio_url = upload_response.json()['upload_url']
    print("Uploaded to ", audio_url)

    transcript_request = {
        'audio_url': audio_url,
        "iab_categories": 'True' if categories else 'False',
    }

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    
    transcript_id = transcript_response.json()['id']
    polling_endpoint = transcript_endpoint + "/" + transcript_id

    print("Transcribing at", polling_endpoint)
    
    return polling_endpoint

def get_status(polling_endpoint):
    polling_response = requests.get(polling_endpoint, headers=headers)
    st.session_state['status'] = polling_response.json()['status']

def refresh_status():
    st.session_state['status'] = 'submitted'

st.header("Transcribe video")

link = st.text_input("Enter the link", value="https://youtu.be/Ji1DKxzJ-js", on_change=refresh_status)
st.video(link)
st.text('The transcription is ' + st.session_state['status'])

polling_endpoint = transcribe_from_link(link, False)
st.button('check_status', on_click=get_status, args=(polling_endpoint,))

transcript = ''
if st.session_state['status'] == 'completed':
    polling_response = requests.get(polling_endpoint, headers=headers)
    transcript = polling_response.json()['text']

st.write(transcript)

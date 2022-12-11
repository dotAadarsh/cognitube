from deepgram import Deepgram
import json
import youtube_dl
import streamlit as st
from languages import languages
from itranslate import itranslate as itrans

st.header("TL;DW")
st.caption("Too Long Didn't Watch")

DEEPGRAM_API_KEY =  st.secrets["DEEPGRAM_API_KEY"]
PATH_TO_FILE = ''

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

@st.cache
def download_video(link):
    _id = link.strip()

    def get_vid(_id):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(_id)

    meta = get_vid(_id)
    save_location = meta['id'] + ".mp3"

    print('Save mp3 to', save_location)
    return save_location

@st.cache
def transcribe(PATH_TO_FILE):
    # Initializes the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    # Open the audio file
    with open(PATH_TO_FILE, 'rb') as audio:
        # ...or replace mimetype as appropriate
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = deepgram.transcription.sync_prerecorded(source, {'summarize': True, 'punctuate': True, "diarize": True, "utterances": True })
        # response_result = json.dumps(response, indent=4)
    
    return response

@st.cache
def translate(text, to_lang):
    return itrans(text, to_lang = to_lang)

link = st.text_input("Enter the YT URL", value="https://youtu.be/4WEQtgnBu0I")
st.video(link)

PATH_TO_FILE = download_video(link)
response = transcribe(PATH_TO_FILE)

tab1, tab2, tab3 = st.tabs(["📜 TL;DW", "🗣️ Translate", "📎Resources"])

with tab1:

    transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
    summary = response["results"]["channels"][0]["alternatives"][0]["summaries"][0]["summary"]
    st.json(json.dumps(response, indent=4),expanded=False)
    
    with st.expander("TL;DW"):
        st.write(summary, expanded=True)

    with st.expander("Transcript", expanded=False):
        st.write(transcript)


if tab2:
    with tab2:
        to_lang = st.selectbox("Select the language", languages.values())
        dest = list(languages.keys())[list(languages.values()).index(to_lang)]
        st.write("language: ", dest)
        st.write(translate(transcript, dest))

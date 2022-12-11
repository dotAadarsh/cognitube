from deepgram import Deepgram
import json
import youtube_dl
import streamlit as st
from languages import languages
from itranslate import itranslate as itrans
from pathlib import Path
import openai

st.header("TL;DW")
st.caption("Too Long Didn't Watch")

DEEPGRAM_API_KEY =  st.secrets["DEEPGRAM_API_KEY"]
openai.api_key = st.secrets["OPEN_AI_API "]

PATH_TO_FILE = ''

@st.cache
def download_video(link):

    videoinfo = youtube_dl.YoutubeDL().extract_info(url = link, download=False)
    filename = f"{videoinfo['id']}.mp3"

    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([videoinfo['webpage_url']])

    base = Path.cwd()
    PATH_TO_FILE = f"{base}/{filename}"

    return PATH_TO_FILE

@st.cache
def transcribe(PATH_TO_FILE):
    # Initializes the Deepgram SDK
    deepgram = Deepgram(DEEPGRAM_API_KEY)
    # Open the audio file
    with open(PATH_TO_FILE, 'rb') as audio:
        # ...or replace mimetype as appropriate
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = deepgram.transcription.sync_prerecorded(source, {'summarize': True, 'punctuate': True, "diarize": True, "utterances": True, "detect_topics": True, "numerals": True})
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

def extract_keywords(transcript):

    response_openai = openai.Completion.create(
    model="text-davinci-002",
    prompt=f'Extract keywords from this text:\n\n{transcript}',
    temperature=0.3,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.8,
    presence_penalty=0.0
    )
    keywords_results = response_openai["choices"][0]["text"].split(',')

    return keywords_results


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
if tab3:
    with tab3:
        topics = response["results"]["channels"][0]["alternatives"][0]["topics"][0]["topics"]
        col1, col2 = st.columns([1, 2])
        with col1:
            if len(topics) == 0:
                st.info("No topics detected!")
            else:
                for t in topics:
                    # topic_list.append(t["topic"])
                    st.button(label=t["topic"], disabled=False)

        with col2:
            keywords = extract_keywords(transcript)
            for keyword in keywords:
                st.write(keyword)
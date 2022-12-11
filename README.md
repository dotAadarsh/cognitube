## CogniTube | Cognitive + YouTube

### Inspiration

Over the past few months, AI has been booming and new project are coming out day by day. ChatGPT, Nvidia’s Magic3D, Stable diffusion and more awe-some projects are released. I just came an idea with why not implement AI in videos. The goal is to create a complete AI enhanced platform for videos.

### What it does

CogniTube is an application that implements AI to the video and provides transcript, summary, resources, translation, AI generated blog and export options.

### How I built it

Initially I've created a [GitHub project board](https://github.com/users/dotaadarsh/projects/15) to keep track on what to do. Then I've implemented each feature one-by-one with the following technologies:
- [youtube-dl](https://github.com/ytdl-org/youtube-dl/blob/master/README.md#readme) - To download YouTube videos
- [Deepgram](https://deepgram.com/) - Implemented Automatic Speech Recognition (ASR) technology to extract transcript, summary and topics.
- [Streamlit](https://streamlit.io/) - Time's running! So for faster UI developement, Streamlit comes into play.
- [OpenAI](https://openai.com/) - With the next-gen powerful AI models, we are able to create a blog posts based on the transcript and also extract the relevant information mentioned in the video. 
- [Gitpod](https://www.gitpod.io/) - It provides me a complete dev environment. 

### Challenges we ran into

- Parsing JSON data - Thanks to StackOverflow!
- Exposed the API Key - GitGuardian informed it!

### Accomplishments that we're proud of

- TL;DW - Too Long Did'nt Watch | Now you can read what's the video is all about!
- Translate to different languages | வெவ்வேறு மொழிகளில் மொழிபெயர்க்க முடியும்
- Topics, Keywords, and external links - Extracts brands, topics and keywords
- Create AI generated blogs - Blogs reimagined!
- Export to audio and PDF - Share as you wish!

### What I've learned
- Learned about ASR
- Explored API's
- Some new Python techniques and concepts
- Streamlit features

### What's next for CogniTube

- Platform for content creator to work on their videos
- Use AI to create content and simplifies their work
- Integrate various platforms
- Analyze feedbacks and audiences

*The thumbnail is created by AI*

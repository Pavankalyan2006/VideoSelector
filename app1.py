import streamlit as st
import requests
import subprocess
import tempfile
import pandas as pd

# ------------------ Hugging Face Token ------------------
HUGGINGFACE_API_KEY = "API_KEY_HERE"  # Replace with your Hugging Face API key
HF_MODEL_URL = "https://api-inference.huggingface.co/models/openai/whisper-base"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# ------------------ Transcription ------------------
def transcribe_audio_huggingface(audio_path):
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    response = requests.post(HF_MODEL_URL, headers=HEADERS, data=audio_bytes)
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        return f"❌ Transcription failed: {response.status_code} - {response.text}"

# ------------------ YouTube Utilities ------------------
def get_video_title(url):
    cmd = f'yt-dlp --get-title {url}'
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
    return result.stdout.decode().strip()

def download_audio(url, out_path):
    command = [
        "yt-dlp", "-f", "bestaudio",
        "--extract-audio", "--audio-format", "mp3",
        "-o", out_path, url
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="🎥 Video Ranker (User-Based)", layout="centered")
st.title("🎥 YouTube Learning Video Ranker by User Evaluation")

# Input YouTube links
urls_input = st.text_area("🔗 Paste YouTube Links (1 per line)", height=150)
urls = [u.strip() for u in urls_input.split("\n") if u.strip()]

# Form for manual input
st.markdown("## 📋 Rate Based on These Fields")

fields = [
    "Topic Relevance", "Clarity of Explanation", "Teaching Style", "Visual Aids / Examples",
    "Pace of the Video", "Real-Life Examples", "Accent & Language Clarity", "Subtitles / Captions",
    "Concept Depth", "Recap at End", "Video Length Suitability", "Comments & Community Help",
    "Exercises or Practice", "Playlist Availability", "Free to Watch"
]

ratings = {}
notes = {}

with st.form("ratings_form"):
    for field in fields:
        st.markdown(f"**{field}**")
        col1, col2 = st.columns([1, 4])
        with col1:
            ratings[field] = st.slider(f"Rate {field}", 1, 5, 3, key=f"{field}_score")
        with col2:
            notes[field] = st.text_input(f"Notes for {field}", key=f"{field}_note")
    submitted = st.form_submit_button("🚀 Evaluate Videos")

# ------------------ Evaluation ------------------
if submitted and urls:
    st.info("⏳ Evaluating videos... This may take a minute.")
    user_score_total = sum(ratings.values())
    results = []

    for url in urls:
        try:
            title = get_video_title(url)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmpfile:
                download_audio(url, tmpfile.name)
                transcript = transcribe_audio_huggingface(tmpfile.name)

            results.append({
                "Title": title,
                "URL": url,
                "Total Score": user_score_total,
                "Transcript Preview": transcript[:250] + "..." if isinstance(transcript, str) else transcript
            })
        except Exception as e:
            results.append({
                "Title": "Error fetching video",
                "URL": url,
                "Total Score": 0,
                "Transcript Preview": f"Error: {str(e)}"
            })

    st.success("✅ Evaluation Complete!")

    # Display the result table
    df = pd.DataFrame(results)
    st.dataframe(df[["Title", "URL", "Total Score"]])

    # Detailed feedback section
    for result in results:
        with st.expander(f"📄 {result['Title']}"):
            st.markdown(f"**Video URL**: {result['URL']}")
            st.markdown(f"**Total Score**: {result['Total Score']} / 75")
            st.markdown("### 📝 Transcript Preview")
            st.code(result["Transcript Preview"])
            st.markdown("### 🧾 Notes")
            for field in fields:
                st.markdown(f"- **{field}**: {ratings[field]}/5 – _{notes[field] or 'No notes'}_")

# VideoSelector


# 🎓 LearnVidRanker

> A personalized YouTube video recommendation system powered by AI transcription and user-defined learning preferences.

---

## 📌 Overview

**LearnVidRanker** helps learners find the most relevant educational YouTube videos based on their personal learning styles. It automatically downloads video audio, transcribes it using the Hugging Face Whisper model, evaluates key learning features (like clarity, pace, visuals), and ranks the videos according to user input.

This project is built using **Streamlit**, **Python**, and **Hugging Face APIs**, making it lightweight, powerful, and user-friendly.

---

## 🚀 Features

- ✅ Accepts multiple YouTube video links
- ✅ User scoring of 15 learning traits via sliders
- ✅ Transcribes audio using Whisper (`openai/whisper-large`) on Hugging Face
- ✅ Scores each video based on transcript analysis and user preferences
- ✅ Displays ranked results with transcript previews
- ✅ One-click best video recommendation
- ✅ Clean, responsive UI (Streamlit)

---

## 🎓 Use Case

**Problem:** Too many videos. No clear way to find which one explains best.

**Solution:** Analyze transcript + match it to what *you* care about (clarity, examples, depth, etc.).

---

## 🧠 Tech Stack

| Layer       | Technology                              |
|-------------|------------------------------------------|
| Frontend    | Streamlit (Python)                      |
| Transcription | Hugging Face API (`openai/whisper-large`) |
| Video Audio | `yt-dlp` for downloading audio          |
| Backend     | Python (Requests, Pandas, Tempfile)     |
| Deployment  | Localhost / Streamlit Cloud / Hugging Face Spaces |

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/learnvidranker.git
cd learnvidranker

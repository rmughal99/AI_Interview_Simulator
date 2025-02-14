# 🎙️ AI Interview Simulator  
An **AI-powered interview practice tool** for **Software Engineering questions**. It uses **Whisper AI** for speech recognition, **Gemini AI** for feedback, and **Streamlit** for a user-friendly interface.

---

## 🚀 Features
✅ **Random Question Generation** – Practice Software Engineering interview questions.  
✅ **Voice-Based Answering** – Upload an audio response, transcribed using **Whisper AI**.  
✅ **AI-Powered Feedback** – Get structured feedback from **Gemini AI** on:  
   - Technical accuracy  
   - Missing key points  
   - Clarity & structure  
   - Suggested improvements  
   - Model answer  
✅ **Multiple Attempts** – Retry and compare different responses.  
✅ **Score Visualization** – Track your progress with a **radar chart**.  

---

## 🛠️ Tech Stack
- **Python** 🐍  
- **Streamlit** 🎨  
- **Whisper AI** 🎙️ (Speech-to-text)  
- **Gemini AI** 🤖 (AI feedback)  
- **Plotly** 📊 (Score visualization)  

---

## 📦 Installation

1️⃣ **Clone the repository**
```sh
git clone https://github.com/yourusername/ai-interview-simulator.git
cd ai-interview-simulator
```

2️⃣ Create a virtual environment
```py
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```
3️⃣ Install dependencies
```py
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```
4️⃣ Set up API Keys
Create a .env file and add your Gemini API key:
```sh
GEMINI_API_KEY=your_api_key_here
```
5️⃣ Run the app
```sh
streamlit run app.py
```

**Usage**
1️⃣ Choose a category & difficulty level
2️⃣ Generate a random question
3️⃣ Record & upload your answer
4️⃣ Get AI-generated feedback & score
5️⃣ Retry and compare previous attempts

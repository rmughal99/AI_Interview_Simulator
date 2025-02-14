import os
import whisper
import pandas as pd
import streamlit as st
import google.generativeai as genai
import plotly.express as px
import re
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Load Whisper
whisper_model = whisper.load_model("base")

# Load dataset
@st.cache_data
def load_questions():
    df = pd.read_csv("software_questions.csv")
    return df

# Streamlit UI
st.title("AI Interview Simulator 💻")
st.subheader("Practice Software Engineering Questions")

# Sidebar filters
st.sidebar.header("Filters")
category = st.sidebar.selectbox("Select Category", ["All"] + list(load_questions()["Category"].unique()))
difficulty = st.sidebar.selectbox("Select Difficulty", ["All", "Easy", "Medium", "Hard"])

# Filter questions
def get_filtered_questions():
    df = load_questions()
    if category != "All":
        df = df[df["Category"] == category]
    if difficulty != "All":
        df = df[df["Difficulty"] == difficulty]
    return df.sample(1).iloc[0]  # Get a random question

# Session state for multiple attempts
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "attempts" not in st.session_state:
    st.session_state.attempts = []

# Generate question
if st.button("Generate New Question"):
    st.session_state.current_question = get_filtered_questions()
    st.session_state.attempts = []  # Reset attempts for new question
    st.write("---")
    st.markdown(f"### 📝 **Question** ({st.session_state.current_question['Difficulty']})")
    st.markdown(f"**{st.session_state.current_question['Question']}**")
    st.write(f"*Category: {st.session_state.current_question['Category']}*")

# Answer section
if st.session_state.current_question is not None:
    st.write("---")
    st.markdown("### 🎙️ Record Your Answer")

    # Upload audio file
    audio_file = st.file_uploader("Upload audio response (MP3/WAV)", type=["wav", "mp3"])

    # Process audio
    if audio_file:
        # Save uploaded audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_file_path = tmp_file.name

        # Transcribe with Whisper
        with st.spinner("Analyzing your answer..."):
            transcription = whisper_model.transcribe(tmp_file_path)["text"]
            
            # Display transcription
            st.write("---")
            st.markdown("### 📝 Transcription")
            st.write(transcription)

            # Generate feedback with Gemini
            prompt = f"""
            Act as a technical interview coach. Analyze this answer to the following question:

            Question: {st.session_state.current_question['Question']}
            Answer: {transcription}

            Provide structured feedback:
            1. **Technical accuracy** (0-5 score)
            2. **Missing key points**
            3. **Clarity/structure** (0-5 score)
            4. **Suggested improvements**
            5. **Example model answer**
            """

            response = model.generate_content(prompt)
            feedback_text = response.text  # Get the full feedback

            # Function to extract scores using regex
            def extract_score(text, category):
                match = re.search(fr"{category}.*?(\d+)", text)
                return int(match.group(1)) if match else 3  # Default to 3 if not found

            # Extract scores safely
            tech_accuracy = extract_score(feedback_text, "Technical accuracy")
            clarity = extract_score(feedback_text, "Clarity/structure")

            # Store attempt
            st.session_state.attempts.append({
                "transcription": transcription,
                "feedback": feedback_text,
                "tech_accuracy": tech_accuracy,
                "clarity": clarity
            })

            # Display feedback
            st.write("---")
            st.markdown("### 📊 Feedback Report")
            st.markdown(feedback_text)

    # Show previous attempts
    if len(st.session_state.attempts) > 1:
        st.write("---")
        st.markdown("### 🔄 Compare Attempts")

        # Prepare data for visualization
        attempt_numbers = list(range(1, len(st.session_state.attempts) + 1))
        tech_scores = [attempt["tech_accuracy"] for attempt in st.session_state.attempts]
        clarity_scores = [attempt["clarity"] for attempt in st.session_state.attempts]

        # Radar chart
        df_chart = pd.DataFrame({
            "Attempt": attempt_numbers,
            "Technical Accuracy": tech_scores,
            "Clarity": clarity_scores
        })

        fig = px.line_polar(
            df_chart.melt(id_vars=["Attempt"], var_name="Metric", value_name="Score"),
            r="Score",
            theta="Metric",
            color="Attempt",
            line_close=True,
            markers=True,
            title="Performance Across Attempts"
        )
        st.plotly_chart(fig)

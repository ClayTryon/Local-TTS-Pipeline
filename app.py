import streamlit as st
from src.scraper import get_article_text
from src.pipeline import run_pipeline

st.set_page_config(page_title="NLP News Analyzer", layout="wide")
st.title("NLP News Analyzer")

# ----------------------------
# Controls
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    use_prosody = st.toggle("Enable Prosody (Sentiment-driven narration)", value=True)

with col2:
    developer_mode = st.toggle("Developer Mode", value=False)

# ----------------------------
# Input Tabs
# ----------------------------
tab_url, tab_text = st.tabs(["Article URL", "Paste Text"])

url = ""
text_input = ""

with tab_url:
    url = st.text_input("Enter article URL")

with tab_text:
    text_input = st.text_area(
        "Paste article text",
        height=250
    )

# ----------------------------
# Analyze Button
# ----------------------------
if st.button("Analyze"):

    progress_bar = st.progress(0)
    status_text = st.empty()

    def update_progress(percent, message):
        progress_bar.progress(percent)
        status_text.text(message)

    try:

        # Determine input source
        if url.strip():
            update_progress(5, "Scraping article text...")
            text = get_article_text(url)

        elif text_input.strip():
            update_progress(5, "Using provided text...")
            text = text_input

        else:
            st.warning("Please enter a URL or paste text.")
            st.stop()

        # Run NLP pipeline
        sentences, sentiment, entities, narration_text, audio_file = run_pipeline(
            text,
            use_prosody=use_prosody,
            progress_callback=update_progress
        )

        status_text.success("Analysis complete.")

        # ----------------------------
        # Article Preview
        # ----------------------------
        st.subheader("Article Preview")
        st.write(text[:1500] + ("..." if len(text) > 1500 else ""))

        # ----------------------------
        # Narration Text
        # ----------------------------
        st.subheader("Narration Text")
        st.code(narration_text)

        # ----------------------------
        # Audio
        # ----------------------------
        st.subheader("Narration")
        st.audio(audio_file)

        # ----------------------------
        # Developer Mode
        # ----------------------------
        if developer_mode:

            st.divider()
            st.subheader("Developer Mode: NLP Outputs")

            with st.expander("Sentiment Analysis"):
                for s in sentiment:
                    st.write(s)

            with st.expander("Named Entities"):
                for e in entities:
                    st.write(e)

    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"Something went wrong: {e}")
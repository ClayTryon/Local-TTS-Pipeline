import re
import spacy
from src.sentiment import analyze_sentences
from src.ner import extract_entities
from src.tts import generate_speech
from src.prosody import apply_prosody

# Load the spaCy English language model.
# This model provides sentence segmentation, tokenization,
# and named entity recognition capabilities.
nlp = spacy.load("en_core_web_sm")


def clean_text(text: str) -> str:
    """
    Cleans input text before it is passed to the speech synthesis stage.
    
    This function removes excessive whitespace and any null characters
    that may appear during web scraping or text extraction. These characters
    can occasionally cause issues for downstream models such as TTS engines.
    """
    text = re.sub(r"\s+", " ", text)  # Replace multiple whitespace characters with a single space
    return text.replace("\x00", "").strip()  # Remove null characters and trim edges


def run_pipeline(text, use_prosody=True, progress_callback=None):
    """
    Main orchestration function for the NLP pipeline.

    This function runs the entire processing sequence:
    1. Sentence segmentation
    2. Sentiment analysis
    3. Named entity recognition
    4. Prosody adjustment
    5. Speech generation

    Parameters
    ----------
    text : str
        The input text to process (either scraped from a URL or pasted directly).
    
    use_prosody : bool
        Determines whether sentiment-based prosody adjustments should be applied
        to the narration text before speech synthesis.

    progress_callback : function
        Optional callback used by the Streamlit UI to update progress bars
        during execution.
    """

    # Step 1: Sentence Segmentation
    if progress_callback:
        progress_callback(10, "Segmenting sentences...")

    # spaCy processes the entire document and identifies sentence boundaries
    doc = nlp(text)

    # Extract clean sentences from the spaCy document
    sentences = [s.text.strip() for s in doc.sents if s.text.strip()]

    if not sentences:
        raise ValueError("No valid sentences extracted.")

    # Step 2: Sentiment Analysis
    if progress_callback:
        progress_callback(35, "Running sentiment analysis...")

    # Each sentence is classified as positive or negative using DistilBERT
    sentiment_results = analyze_sentences(sentences)

    # Step 3: Named Entity Recognition
    if progress_callback:
        progress_callback(60, "Extracting named entities...")

    # Extract entities such as people, organizations, locations, etc.
    # Currently these are mainly displayed for analysis, but could be used
    # for future pronunciation or emphasis adjustments.
    entities = extract_entities(text)

    # Step 4: Prepare narration text
    if progress_callback:
        progress_callback(75, "Preparing narration...")

    # If prosody is enabled, adjust punctuation based on sentiment results.
    # Otherwise, use the original sentences.
    narration_sentences = (
        apply_prosody(sentiment_results) if use_prosody else sentences
    )

    # Clean and combine all narration sentences into a single text block
    # that will be passed to the TTS engine.
    narration_text = "\n".join(clean_text(s) for s in narration_sentences)

    # Step 5: Speech synthesis
    if progress_callback:
        progress_callback(90, "Generating speech...")

    # Generate speech using Piper TTS and return the resulting audio file
    audio_file = generate_speech(narration_text)

    if progress_callback:
        progress_callback(100, "Done.")

    # Return intermediate outputs so the UI can display analysis results
    # such as sentiment labels and extracted entities.
    return sentences, sentiment_results, entities, narration_text, audio_file
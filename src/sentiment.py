from transformers import pipeline
import torch

# Detect hardware, in case the user is using a CPU
device = 0 if torch.cuda.is_available() else -1

# Load model once at module import
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=device
)


def analyze_sentences(sentences, batch_size=16):

    # Clean input
    cleaned_sentences = [s.strip() for s in sentences if s and s.strip()]

    if not cleaned_sentences:
        return []

    # Batch inference to try and improve performance. Single sequential is slower if Cuda enabled
    predictions = sentiment_model(
        cleaned_sentences,
        batch_size=batch_size,
        truncation=True,
        max_length=512
    )

    # Format results
    results = []
    for sentence, pred in zip(cleaned_sentences, predictions):
        results.append({
            "sentence": sentence,
            "label": pred["label"],
            "score": pred["score"]
        })

    return results
def apply_prosody(sentiment_results):

    sentences = []

    for item in sentiment_results:

        sentence = item["sentence"]
        label = item["label"]
        score = item["score"]

        if label == "POSITIVE" and score > 0.8:
            sentence = sentence.rstrip(".") + "!"

        elif label == "NEGATIVE" and score > 0.8:
            sentence = sentence.rstrip(".") + "..."

        sentences.append(sentence)

    return sentences
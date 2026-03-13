import spacy
#this python file is mostly just useful if we use a tts that isn't Piper, as it adds labels 
# the labels it adds are not currently implemented in prosody.py, but this is for futureproofing

nlp = spacy.load("en_core_web_sm")


def extract_entities(text):

    doc = nlp(text)

    return [
        {"text": ent.text, "label": ent.label_}
        for ent in doc.ents
    ]
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    # best-effort: attempt download if not present
    import subprocess, sys

    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=False)
    nlp = spacy.load("en_core_web_sm")


def extract_keywords(text: str, max_keywords: int = 20):
    if not text:
        return []
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return keywords[:max_keywords]

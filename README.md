# OCR → NLP → Wikipedia Flashcards

Minimal FastAPI web app that accepts image uploads, runs Tesseract OCR, extracts keywords with spaCy, retrieves a Wikipedia summary, and helps generate flashcards (CSV).

Requirements
- Install Tesseract separately (Windows installer) and add it to PATH.
- Python packages:

```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```


## Deploy to Render.com (Free)

1. Push this repo to GitHub.
2. Go to https://dashboard.render.com and create a new Web Service from your repo.
3. Render will auto-detect `render.yaml` and run `build.sh` to install Tesseract and dependencies.
4. The backend will be available at `https://<your-app>.onrender.com`.

**Local run:**
```
uvicorn main:app --reload
```
Open http://127.0.0.1:8000 and upload an image.

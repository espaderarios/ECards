
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ocr import extract_text_from_bytes
from nlp import extract_keywords
from search import build_query, search_wikipedia
from explain import format_output
from flashcards import generate_csv
import uvicorn
import os


app = FastAPI()

# Enable CORS - MUST be added first before other middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://riosweb.tech",
        "http://localhost:3000",  # Local development
        "http://localhost:8000",  # Local backend
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Serve static docs (was frontend)
docs_path = os.path.join(os.path.dirname(__file__), "docs")
if os.path.exists(docs_path):
  app.mount("/docs", StaticFiles(directory=docs_path), name="docs")



# Redirect root to docs index.html
@app.get("/")
def root():
  return FileResponse(os.path.join(docs_path, "index.html"))



# Upload image, return OCR, keywords, query, explanation, and flashcard JSON
@app.post('/api/upload')
async def upload_image(file: UploadFile = File(...)):
  try:
    data = await file.read()
    
    # Validate file is not empty
    if not data:
      return JSONResponse(
        status_code=400,
        content={"error": "File is empty"}
      )
    
    # Extract text with error handling
    try:
      text = extract_text_from_bytes(data)
    except Exception as e:
      return JSONResponse(
        status_code=500,
        content={"error": f"OCR failed: {str(e)}"}
      )
    
    if not text:
      return JSONResponse(
        status_code=400,
        content={"error": "No text found in image"}
      )
    
    # Extract keywords
    try:
      keywords = extract_keywords(text)
    except Exception as e:
      keywords = []
    
    # Build query and search
    query = build_query(keywords)
    try:
      explanation = search_wikipedia(query)
    except Exception as e:
      explanation = f"Could not retrieve explanation: {str(e)}"
    
    card = {"front": text, "back": explanation}
    return {
      'text': text,
      'keywords': keywords,
      'query': query,
      'explanation': explanation,
      'card': card,
      'deck': [card],
    }
  except Exception as e:
    return JSONResponse(
      status_code=500,
      content={"error": f"Server error: {str(e)}"}
    )

# Download CSV for a deck (POST with JSON array of cards)
from fastapi import Request
from typing import List
@app.post('/api/export/csv')
async def export_csv(request: Request):
  data = await request.json()
  csv_str = generate_csv(data)
  return HTMLResponse(
    content=csv_str,
    media_type="text/csv",
    headers={"Content-Disposition": "attachment; filename=flashcards.csv"}
  )



if __name__ == '__main__':
  uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)

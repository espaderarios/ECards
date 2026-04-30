#!/usr/bin/env bash
set -e
apt-get update && apt-get install -y tesseract-ocr
pip install -r requirements.txt
python -m spacy download en_core_web_sm

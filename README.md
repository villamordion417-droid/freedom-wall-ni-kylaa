# Freedom Wall — Comfort Edition

A simple Django app where users can vent and receive a comforting song recommendation matched to their mood.

Quick run (Windows PowerShell):

1. python -m venv .venv
2. .\.venv\Scripts\Activate
3. pip install -r requirements.txt
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py runserver

Notes:
- The app uses NLTK VADER for sentiment detection and a small built-in song library.
- On first run NLTK will download the `vader_lexicon` corpus automatically.

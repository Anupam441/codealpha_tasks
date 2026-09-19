# Task 1 - Simple URL Shortener (CodeAlpha Backend Internship)

**Stack:** Python, Flask, SQLite, HTML/CSS/JS (basic frontend)

## Task requirements covered
- Backend server using Flask
- API endpoint that accepts a long URL and generates a unique short code (`POST /api/shorten`)
- Mapping of short code -> original URL stored in SQLite
- Redirect route: opening the short URL takes you to the original URL (`GET /<code>`)
- Optional: basic frontend to input a long URL and show the shortened one (`/`)

## Extra features
- Custom short codes, duplicate URL re-use, URL validation
- Click counter and stats endpoint (`GET /api/stats/<code>`)

## Run
```bash
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Run tests
```bash
pip install pytest
python -m pytest -q
```

## API examples
```bash
curl -X POST http://127.0.0.1:5000/api/shorten -H "Content-Type: application/json" \
  -d '{"url": "https://www.codealpha.tech"}'
curl -i http://127.0.0.1:5000/<short_code>
curl http://127.0.0.1:5000/api/stats/<short_code>
```

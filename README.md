# Kuku Finance

Kuku is a stock dashboard which uses FastAPI backend to scrape live stock data from Yahoo Finance.
React frontend (in progress) displays it.

## Backend
- FastAPI + BeautifulSoup scraper, refreshes every 5 min via APScheduler
- Falls back to live scrape on cache miss
- Run: `cd backend && uvicorn main:app --reload`
- Docs at `http://localhost:8000/docs`

## Frontend
Coming soon (React)

## Note
Built for learning purposes. Scrapes publicly available Yahoo Finance pages 
with rate limiting via scheduled refresh.

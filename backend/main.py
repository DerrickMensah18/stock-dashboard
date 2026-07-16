from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from scraper import scrape_stock, scrape_multiple
from models import Stock
from cache import load_from_cache
from scheduler import start_scheduler
from typing import List
from fastapi.middleware.cors import CORSMiddleware


scheduler = None

@asynccontextmanager
async def lifespan(app: FastAPI):
  global scheduler
  scheduler = start_scheduler()
  yield
  scheduler.shutdown()

app = FastAPI(
  title="Stock Dashboard API",
  description="Live stock data scraped from Yahoo Finance",
  version="1.0.0",
  lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
  return {"message": "Stock Dashboard API is running"}

@app.get("/stocks/{ticker}", response_model=Stock)
def get_stock(ticker: str):
  cached = load_from_cache()
  
  # 1. Search the cache for the requested ticker
  match = next((s for s in cached if s["ticker"] == ticker.upper()), None)
  
  # 2. If it is in the cache, return it immediately
  if match is not None:
    return match
      
  # 3. Cache miss: scrape live data as a fallback
  data = scrape_stock(ticker)
  if data is None:
    raise HTTPException(status_code=404, detail=f"Could not fetch data for {ticker.upper()}")
  
  return data

@app.get("/stocks", response_model=List[Stock])
def get_multiple_stocks(tickers: str):
  ticker_list = [t.strip().upper() for t in tickers.split(",")]
  cached = load_from_cache()
  
  # Filter out stocks that already exist inside our cache file
  cached_matches = [s for s in cached if s["ticker"] in ticker_list]
  missing_tickers = [t for t in ticker_list if t not in [s["ticker"] for s in cached_matches]]
  
  # If anything was missing from the cache, scrape it live
  scraped_data = []
  if missing_tickers:
    scraped_data = scrape_multiple(missing_tickers)
      
  # Combine both results to return a complete list
  total_results = cached_matches + scraped_data
  
  if not total_results:
    raise HTTPException(status_code=404, detail="Could not fetch any stock data")
      
  return total_results

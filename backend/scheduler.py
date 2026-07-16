from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scrape_multiple
from cache import save_to_cache

TICKERS = ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"]

def refresh_data():
  print("Refreshing stock data...")
  data = scrape_multiple(TICKERS)
  if data:
    save_to_cache(data)
    print(f"Cache updated with {len(data)} stocks.")
  else:
    print("Warning: Scheduled refresh returned no data. Cache not overwritten.")

def start_scheduler():
  scheduler = BackgroundScheduler()
  
  # Run every 5 minutes
  scheduler.add_job(refresh_data, "interval", minutes=5)
  
  # FIX: Trigger a separate background run to execute IMMEDIATELY on startup
  # This prevents the main execution thread from locking up
  scheduler.add_job(refresh_data, "date", run_date=datetime.now() + timedelta(seconds=2))
  
  scheduler.start()
  return scheduler

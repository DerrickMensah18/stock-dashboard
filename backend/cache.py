import json
import os

CACHE_FILE = "stocks_data.json"

def save_to_cache(data):
  # Enforcing utf-8 protects currency and company branding text symbols on Windows
  with open(CACHE_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

def load_from_cache():
  if not os.path.exists(CACHE_FILE):
    return []
    
  try:
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  except (json.JSONDecodeError, ValueError, OSError):
    # Fallback safety safety if the file is blank, empty, or corrupted
    print(f"Warning: {CACHE_FILE} was corrupted or empty. Returning default empty list.")
    return []

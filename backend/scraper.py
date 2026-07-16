import requests
from bs4 import BeautifulSoup
import json
from cache import save_to_cache

def scrape_stock(ticker):
    #the URL I'm trying to scrape
    url = f"https://finance.yahoo.com/quote/{ticker}/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        price_tag = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
        if not price_tag or price_tag.text.strip() == "":
            print(f"Ticker {ticker} not found on Yahoo Finance.")
            return None
            
        price = price_tag.get("data-value") or price_tag.text.strip()

        name_tag = soup.find("h1", class_="yf-b3z775") or soup.find("h1")
        if name_tag and "Yahoo Finance" not in name_tag.text:
            name = name_tag.text.strip()
        else:
            title_tag = soup.find("title")
            if title_tag and "Stock Price" in title_tag.text:
                name = title_tag.text.split(" (")[0].strip()
            else:
                name = ticker.upper()

        
        volume_tag = soup.find("fin-streamer", {"data-field": "regularMarketVolume"})
        volume = volume_tag["data-value"] if volume_tag else "N/A"

        market_cap_tag = soup.find("fin-streamer", {"data-field": "marketCap"})
        market_cap = market_cap_tag["data-value"] if market_cap_tag else "N/A"

        result = {
            "ticker": ticker.upper(),
            "name": name, 
            "price": float(price.replace(",", "")) if price != "N/A" else 0.0, 
            "volume": clean_volume(volume),
            "market_cap": clean_market_cap(market_cap)
        }

        
        return result
    except Exception as e:
        print(f"Error parsing {ticker}: {e}")
        return None

def scrape_multiple(tickers):
    all_stocks = []
    for ticker in tickers:
        print(f"Scraping {ticker.upper()}...")
        data = scrape_stock(ticker)
        if data:
            all_stocks.append(data)
    
    # with open("stocks_data.json", "w") as f:
    #     #json dump helps to format data in json format
    #     json.dump(all_stocks, f, indent=2)
    save_to_cache(all_stocks)
    print("\nCompleted! Data has been saved to stocks_data.json")
    return all_stocks

def clean_volume(volume_str):
    if not volume_str or volume_str == "N/A":
        return 0.0
    # Remove commas and convert to float
    return float(volume_str.replace(",", ""))

def clean_market_cap(market_cap_str):
    if not market_cap_str or market_cap_str == "N/A":
        return None
    
    # Standardize string formatting
    val = market_cap_str.upper().strip().replace(",", "")
    
    try:
        # Match alphabetical financial scale notation
        if val.endswith("T"):
            return float(val.replace("T", "")) * 1_000_000_000_000
        if val.endswith("B"):
            return float(val.replace("B", "")) * 1_000_000_000
        if val.endswith("M"):
            return float(val.replace("M", "")) * 1_000_000
        return float(val)
    except ValueError:
        return None


#results = scrape_multiple(["CCL", "TSLA", "GOOGL", "AAPL"])
#print(json.dumps(results, indent=2))
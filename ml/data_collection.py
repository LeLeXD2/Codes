import pandas as pd
import requests
import yfinance as yf
import os
import time

# ==========================================
# GET S&P500 TICKERS
# ==========================================

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

sp500 = pd.read_html(response.text)[0]

tickers = sp500["Symbol"].tolist()
tickers = [t.replace(".", "-") for t in tickers]

print(f"Total tickers found: {len(tickers)}")

# ==========================================
# CREATE FOLDER
# ==========================================

os.makedirs("data/raw", exist_ok=True)

company_info = []

downloaded = 0
skipped = 0

# ==========================================
# DOWNLOAD STOCKS
# ==========================================

for ticker in tickers:

    filepath = f"data/raw/{ticker}.csv"

    try:

        # -----------------------------
        # Download historical prices
        # -----------------------------
        if not os.path.exists(filepath):

            print(f"Downloading {ticker}...")

            df = yf.download(
                ticker,
                period="15y",
                auto_adjust=False,
                progress=False
            )

            # Flatten MultiIndex columns (new yfinance versions)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Remove incomplete last trading day
            if not df.empty and pd.isna(df.iloc[-1]["Close"]):
                df = df.iloc[:-1]


            if (
                df.empty
                or len(df) < 3000
                or df.isnull().sum().sum() > 50
            ):
                print(f"Skipping {ticker} (invalid historical data)")
                skipped += 1
                continue

            # Remove Incomplete Trading Days
            
            # Save to CSV
            df.to_csv(filepath)

        else:
            print(f"{ticker} already exists")

        downloaded += 1

        # -----------------------------
        # Company Information
        # -----------------------------
        stock = yf.Ticker(ticker)
        info = stock.info

        company_info.append({

            "Ticker": ticker,

            "Company": info.get("longName", ""),

            "Sector": info.get("sector", ""),

            "Industry": info.get("industry", ""),

            "Business Summary": info.get("longBusinessSummary", "")

        })

        # avoid Yahoo rate limiting
        time.sleep(0.2)

    except Exception as e:

        print(f"Error processing {ticker}: {e}")

        skipped += 1

# ==========================================
# SAVE COMPANY INFORMATION
# ==========================================

company_df = pd.DataFrame(company_info)

company_df.to_csv(
    "data/company_info.csv",
    index=False
)

# ==========================================
# SUMMARY
# ==========================================

print("\n========== SUMMARY ==========")

print(f"Downloaded Stocks : {downloaded}")
print(f"Skipped Stocks    : {skipped}")

print(f"\nSaved historical data to:")
print("data/raw/")

print(f"\nSaved company information:")
print("data/company_info.csv")

print("\nColumns:")
print(company_df.columns.tolist())

print("\nExample:")
print(company_df.head())
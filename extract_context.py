import pandas as pd
import re

sp500 = pd.read_csv("data/company_info.csv")

COMPANIES = {}

for _, row in sp500.iterrows():

    ticker = str(row["Ticker"]).upper().strip()

    if pd.isna(row["Company"]):
        continue

    company = str(row["Company"]).upper().strip()

    # Remove common company suffixes
    company = (
        company
        .replace(" INC.", "")
        .replace(" INC", "")
        .replace(" CORPORATION", "")
        .replace(" CORP.", "")
        .replace(" CORP", "")
        .replace(",", "")
        .replace(" LTD.", "")
        .replace(" LTD", "")
        .replace(" PLC", "")
        .replace(" COMPANY", "")
        .strip()
    )

    COMPANIES[company] = ticker


# ============================================================
# VALID TICKERS
# ============================================================

VALID_TICKERS = set(COMPANIES.values())


# Common English words that could also look like ticker symbols
TICKER_STOPWORDS = {
    "A",
    "I",
    "AN",
    "AM",
    "ARE",
    "AT",
    "BE",
    "BUY",
    "FOR",
    "GOOD",
    "HOLD",
    "IN",
    "IS",
    "IT",
    "ME",
    "MY",
    "OF",
    "ON",
    "OR",
    "SELL",
    "THE",
    "TO"
}


# ============================================================
# EXTRACT TICKER
# ============================================================

def extract_ticker(message):

    message = message.upper().strip()

    print("Searching:", message)

    # --------------------------------------------------------
    # 1. CHECK COMPANY NAMES
    # --------------------------------------------------------

    # Longer company names are checked first
    for company, ticker in sorted(
        COMPANIES.items(),
        key=lambda x: len(x[0]),
        reverse=True
    ):

        # Match complete company names rather than substrings
        pattern = r"(?<!\w)" + re.escape(company) + r"(?!\w)"

        if re.search(pattern, message):

            print("Matched company:", company)
            print("Ticker:", ticker)

            return ticker

    # --------------------------------------------------------
    # 2. CHECK EXPLICIT TICKER SYMBOLS
    # --------------------------------------------------------

    words = re.findall(r"\b[A-Z]{1,5}\b", message)

    for word in words:

        # Prevent normal English words such as "A"
        # from being interpreted as ticker symbols
        if word in TICKER_STOPWORDS:
            continue

        if word in VALID_TICKERS:

            print("Matched ticker:", word)

            return word

    # --------------------------------------------------------
    # NO SUPPORTED COMPANY FOUND
    # --------------------------------------------------------

    print("No ticker found.")

    return None

def extract_contextual_ticker(message, history):

    # First try the current message
    ticker = extract_ticker(message)

    if ticker is not None:
        return ticker

    # If no ticker found, look backwards
    # through recent conversation

    for item in reversed(history):

        if item["role"] != "user":
            continue

        previous_message = item["content"]

        ticker = extract_ticker(previous_message)

        if ticker is not None:
            return ticker

    return None

def build_contextual_query(message, history):

    previous_messages = []

    # Only use the last 4 messages
    for item in history[-4:]:

        content = item.get("content", "")

        # Limit each message to 500 characters
        content = content[:500]

        previous_messages.append(
            f"{item['role']}: {content}"
        )

    conversation = "\n".join(previous_messages)

    query = f"""
Previous conversation:

{conversation}

Current question:

{message}
"""

    # Hard limit for vector search
    return query[:4000]
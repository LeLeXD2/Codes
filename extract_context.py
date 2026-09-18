import pandas as pd
import re

sp500 = pd.read_csv("data/company_info.csv")

COMPANIES = {}

for _, row in sp500.iterrows():

    ticker = row["Ticker"].upper()

    if pd.isna(row["Company"]):
        continue

    company = (
        row["Company"]
        .replace(" Inc.", "")
        .replace(" Corporation", "")
        .replace(" Corp.", "")
        .replace(",", "")
        .replace(" Ltd.", "")
        .replace(" plc", "")
        .replace(" Company", "")
        .upper()
    )

    COMPANIES[company] = ticker

def extract_ticker(message):

    message = message.upper().strip()

    print("Searching:", message)

    # Check company names first
    for company, ticker in COMPANIES.items():

        if company in message:

            print("Matched company:", company)

            return ticker

    # Check ticker symbols
    words = re.findall(r"[A-Z]+", message)

    for word in words:

        if word in COMPANIES.values():

            print("Matched ticker:", word)

            return word

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
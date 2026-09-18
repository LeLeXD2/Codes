from unittest import result

import pandas as pd

from flask import Flask, render_template, request, jsonify, session

from predictor import recommend_stock, top_stocks

from ai_helper import explain_stock, ask_openai

from dotenv import load_dotenv

from extract_context import extract_contextual_ticker, build_contextual_query

from intent import detect_intent, extract_top_n

from rag.rag import retrieve_context

load_dotenv()

app = Flask(__name__)
app.secret_key = "your-secret-key"

# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")

# ==========================================
# PREDICT
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    message = request.form.get("message", "").strip()

    if not message:

        return jsonify({
            "reply": "Please enter a question."
        })

    # ==========================================
    # GET CONVERSATION HISTORY
    # ==========================================

    history = session.get("history", [])

    # ==========================================
    # DETECT INTENT
    # ==========================================

    intent = detect_intent(message)

    # ==========================================
    # EXTRACT TICKER
    # ==========================================

    ticker = extract_contextual_ticker(
        message,
        history
    )

    # ==========================================
    # GREETING
    # ==========================================

    if intent == "greeting":

        reply = """
        <h3>👋 Hello!</h3>

        <p>
        I'm your Financial Advisor Bot.
        You can ask me about stocks, investing concepts,
        market conditions and more.
        </p>

        <p>For example:</p>

        <p>- Should I buy Tesla?</p>
        <p>- What is diversification?</p>
        <p>- Why does inflation affect stocks?</p>
        <p>- What does market rank mean?</p>
        """

    # ==========================================
    # STOCK ANALYSIS
    # ==========================================

    elif intent in [
        "buy",
        "sell",
        "analysis",
        "explanation"
    ]:

        if ticker is None:

            # No ticker found
            rag_query = build_contextual_query(
                message,
                history
            )

            context = retrieve_context(rag_query)

            reply = ask_openai(
                message,
                context,
                history
            )

        else:

            # ==========================================
            # GET ML PREDICTION
            # ==========================================

            result = recommend_stock(ticker)

            print("\n================================")
            print("STOCK ANALYSIS")
            print("================================")
            print("Ticker:", ticker)
            print("Result:", result)


            # ==========================================
            # CHECK RESULT
            # ==========================================

            if result is None:

                reply = f"""
                <p>
                    I couldn't find a prediction for
                    <strong>{ticker}</strong>.
                </p>
                """

            else:
                # ==========================================
                # RAG CONTEXT
                # ==========================================

                rag_query = build_contextual_query(
                    message,
                    history
                )

                context = retrieve_context(
                    rag_query
                )


                # ==========================================
                # OPENAI EXPLANATION
                # ==========================================

                explanation = explain_stock(
                    result,
                    message,
                    intent,
                    context,
                    history
                )


                # ==========================================
                # FINAL RESPONSE
                # ==========================================

                reply = f"""
                {explanation}
                """
    # ==========================================
    # TOP STOCKS
    # ==========================================
    elif intent == "top_stocks":

        n = extract_top_n(message)

        stocks = top_stocks(n)

        if not stocks:

            reply = """
            <p>
                I couldn't find any stocks currently meeting
                the model's BUY criteria.
            </p>
            """

        else:

            reply = """
            <h3>📈 Top {n} Stocks Based on the ML Model</h3>

            <p>
                Based on the latest predictions, these are the {n}
                stocks with the highest predicted 5-day returns
                among stocks receiving a BUY signal.
            </p>
            """

            for i, stock in enumerate(stocks, 1):

                ticker = stock["Ticker"]
                prediction = stock["Predicted_Return"]
                rank = stock["Rank"]

                reply += f"""
                <div class="stock-result">

                    <h4>
                        {i}. {ticker}
                    </h4>

                    <p>
                        <strong>Recommendation:</strong>
                        BUY
                    </p>

                    <p>
                        <strong>Predicted 5-Day Return:</strong>
                        {prediction:.2%}
                    </p>

                    <p>
                        <strong>Market Rank:</strong>
                        {rank:.2%}
                    </p>

                </div>
                """

    # ==========================================
    # GENERAL / RAG QUESTION
    # ==========================================

    else:

        # Retrieve relevant knowledge
        rag_query = build_contextual_query(
            message,
            history
        )

        context = retrieve_context(rag_query)

        # Ask OpenAI using:
        # - current question
        # - RAG context
        # - conversation history

        reply = ask_openai(
            message,
            context,
            history
        )

    # ==========================================
    # SAVE CONVERSATION
    # ==========================================

    history.append({
        "role": "user",
        "content": message
    })

    history.append({
        "role": "assistant",
        "content": reply
    })

    # Keep only recent messages
    history = history[-10:]

    session["history"] = history

    # ==========================================
    # RETURN
    # ==========================================

    return jsonify({
        "reply": reply
    })

# ==========================================
# NEW CHAT
# ==========================================

@app.route("/new_chat", methods=["POST"])
def new_chat():

    session["history"] = []

    return jsonify({
        "success": True
    })

# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)
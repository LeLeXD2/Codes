from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def explain_stock(result, message, intent, context, history):

    # ==========================================
    # FORMAT CONVERSATION HISTORY
    # ==========================================

    conversation_history = ""

    if history:

        for item in history[-6:]:

            role = item.get("role", "user")
            content = item.get("content", "")

            conversation_history += (
                f"{role.upper()}: {content}\n"
            )

    else:

        conversation_history = "No previous conversation."


    # ==========================================
    # FORMAT RAG CONTEXT
    # ==========================================

    if context:

        rag_context = context

    else:

        rag_context = "No additional knowledge was retrieved."


    # ==========================================
    # CREATE PROMPT
    # ==========================================

    prompt = f"""

    You are a helpful and educational financial assistant.

    Your job is to explain the machine-learning stock
    prediction clearly to a beginner investor.

    IMPORTANT:

    - Do not guarantee investment returns.
    - Do not claim that a prediction is certain.
    - Clearly distinguish the model's prediction from facts.
    - Do not invent financial information.
    - Only use information provided in the stock data,
    retrieved knowledge, and conversation history.
    - If information is not provided, say that it is not
    available.
    - Do not pretend that you have access to current news
    unless it is included in the provided context.


    ========================================
    CONVERSATION HISTORY
    ========================================

    {conversation_history}


    ========================================
    CURRENT USER QUESTION
    ========================================

    {message}


    ========================================
    USER INTENT
    ========================================

    {intent}


    ========================================
    STOCK MODEL RESULTS
    ========================================

    Ticker:
    {result["Ticker"]}

    Recommendation:
    {result["Signal"]}

    Predicted 5-day return:
    {result["Predicted_Return"]:.2%}

    Market Rank:
    {result["Rank"]:.2%}


    ========================================
    RETRIEVED KNOWLEDGE
    ========================================

    {rag_context}


    ========================================
    INSTRUCTIONS
    ========================================

    Use the conversation history to understand
    follow-up questions.

    For example, if the previous conversation was
    about Tesla and the user asks "Why?", understand
    that they are referring to Tesla.

    Use the retrieved knowledge to explain financial
    concepts when relevant.

    If the user asked whether to BUY:

    - Explain what the model's BUY signal means.
    - Explain the predicted return.
    - Explain the market rank.
    - Explain relevant risks.
    - Make clear that the model prediction is not a
    guarantee of future performance.

    If the user asked whether to SELL:

    - Explain what the model's SELL signal means.
    - Explain the predicted return.
    - Explain the market rank.
    - Explain relevant risks.
    - Make clear that the model prediction is not a
    guarantee of future performance.

    If the user asked for an ANALYSIS:

    - Explain the model's current prediction.
    - Explain the predicted return.
    - Explain the market rank.
    - Explain relevant information from the retrieved
    knowledge.
    - Discuss relevant risks and limitations.

    If the user asks a follow-up question such as:

    "Why?"

    "What does that mean?"

    "What about the risk?"

    "Is that good?"

    use the conversation history to determine what
    "that" refers to.

    Do not repeat the entire previous answer unless
    necessary.

    Keep the response professional, clear, and
    beginner-friendly.

    ========================================
    RESPONSE FORMAT
    ========================================

    Return the explanation using HTML formatting.

    Use <h3> for section headings.

    Use <p> for normal paragraphs.

    Use <strong>...</strong> for important terms.

    Use <p> - ..... </p> for lists.
    Separate major sections into separate paragraphs.

    Do NOT use Markdown.

    Do NOT use Markdown bold such as **text**.

    Do NOT use Markdown bullet points.

    Do NOT use code blocks.

    The response will be inserted directly into
    an HTML chat bubble.

    Add a final summart of the model's prediction (ticker, recommendation, predicted return, and market rank) in a separate section at the end of the response.
    """


    # ==========================================
    # OPENAI
    # ==========================================

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",
                "content":
                "You are a helpful educational "
                "financial assistant."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.3
    )


    # ==========================================
    # GET RESPONSE
    # ==========================================

    explanation = response.choices[0].message.content

    print("AI Explanation:")
    print(explanation)

    return explanation

def ask_openai(message, context, history):

    conversation = ""

    for item in history[-10:]:

        conversation += (
            f"{item['role'].upper()}: "
            f"{item['content']}\n"
        )

    prompt = f"""
        You are a beginner-friendly financial advisor chatbot.

        Use the supplied knowledge and conversation history
        to answer the user's question clearly and accurately.

        If the supplied knowledge is insufficient, you may use
        general financial knowledge, but do not fabricate
        specific facts, stock predictions, prices, or statistics.

        Never fabricate stock predictions.

        If the question asks about a specific stock and the user
        is asking for a recommendation, tell the user to analyse
        the stock instead so that the machine-learning prediction
        can be used.

        Use the conversation history to understand follow-up
        questions such as:

        - "Why?"
        - "What about it?"
        - "What does that mean?"
        - "What about the risk?"

        If the user refers to "it", "that stock", or similar
        phrasing, use the conversation history to determine
        what they are referring to.

        ========================================
        CONVERSATION HISTORY
        ========================================

        {conversation}


        ========================================
        RETRIEVED KNOWLEDGE
        ========================================

        {context}


        ========================================
        CURRENT QUESTION
        ========================================

        {message}

        ========================================
        RESPONSE FORMAT
        ========================================
    
        Return the explanation using HTML formatting.
    
        Use <h3> for section headings.
    
        Use <p> for normal paragraphs.
    
        Use <strong>...</strong> for important terms.
    
        Use <p> - ..... </p> for lists.
        Separate major sections into separate paragraphs.
    
        Do NOT use Markdown.
    
        Do NOT use Markdown bold such as **text**.
    
        Do NOT use Markdown bullet points.
    
        Do NOT use code blocks.
    
        The response will be inserted directly into
        an HTML chat bubble.

        Keep it within 500 words and beginner-friendly.
        """

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text
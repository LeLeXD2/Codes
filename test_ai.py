from predictor import recommend_stock
from rag.rag import retrieve_context
from ai_helper import explain_stock


ticker = "TSLA"

message = "Why?"

intent = "explanation"


history = [

    {
        "role": "user",
        "content": "Should I buy Tesla?"
    },

    {
        "role": "assistant",
        "content":
        "Tesla currently has a BUY signal."
    },

    {
        "role": "user",
        "content": "Why?"
    }
]


result = recommend_stock(ticker)

context = retrieve_context(
    "Why should I buy Tesla?"
)


answer = explain_stock(
    result,
    message,
    intent,
    context,
    history
)


print(answer)
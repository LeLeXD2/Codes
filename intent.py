import re
import joblib


# ==========================================
# LOAD INTENT MODEL
# ==========================================

intent_model = joblib.load(
    "model/intent_classifier.pkl"
)
# ==========================================
# DETECT INTENT
# ==========================================

def detect_intent(message):

    text = message.lower().strip()

    # ==========================================
    # HIGH-CONFIDENCE RULES
    # ==========================================

    if re.search(
        r"\b(hi|hello|hey)\b",
        text
    ):

        return "greeting"


    if re.search(
        r"\bshould i buy\b",
        text
    ):

        return "buy"


    if re.search(
        r"\bshould i sell\b",
        text
    ):

        return "sell"

    probabilities = (
        intent_model.predict_proba(
            [message]
        )[0]
    )


    best_index = probabilities.argmax()


    intent = (
        intent_model.classes_[
            best_index
        ]
    )


    confidence = (
        probabilities[
            best_index
        ]
    )


    print("\n================================")
    print("INTENT CLASSIFICATION")
    print("================================")

    print("Message:", message)
    print("Intent:", intent)

    print(
        f"Confidence: {confidence:.2%}"
    )

    # ==========================================
    # LOW CONFIDENCE FALLBACK
    # ==========================================

    if confidence < 0.20:

        return "general"

    return intent

def extract_top_n(message, default=5, maximum=10):

    message = message.lower()

    # ==========================================
    # DIGIT NUMBERS
    # ==========================================

    match = re.search(
        r"\b(?:top|best|strongest)\s+(\d+)\b",
        message
    )

    if match:

        number = int(match.group(1))

        return min(
            max(number, 1),
            maximum
        )


    # ==========================================
    # WRITTEN NUMBERS
    # ==========================================

    number_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10
    }


    for word, number in number_words.items():

        if re.search(
            rf"\b{word}\b",
            message
        ):

            return number


    # ==========================================
    # DEFAULT
    # ==========================================

    return default
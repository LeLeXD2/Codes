import joblib


model = joblib.load(
    "model/intent_classifier.pkl"
)


tests = [

    "Would Tesla be worth purchasing?",

    "Do you think I should get rid of Apple?",

    "Give me your assessment of Nvidia",

    "Which companies have the strongest predictions?",

    "Why did you recommend that?",

    "What is diversification?",

    "Hello!"

]


for message in tests:

    prediction = model.predict(
        [message]
    )[0]

    probabilities = model.predict_proba(
        [message]
    )[0]

    confidence = probabilities.max()

    print("\n-------------------------")

    print("Message:", message)

    print("Intent:", prediction)

    print(
        f"Confidence: {confidence:.2%}"
    )
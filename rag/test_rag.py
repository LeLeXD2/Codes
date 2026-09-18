from rag import retrieve_context

questions = [
    "What is an ETF?",
    "What is fundamental analysis?",
    "What is compound interest?",
]

for question in questions:

    print("\n================================")
    print("QUESTION:", question)
    print("================================")

    context = retrieve_context(question)

    print(context[:1500])

print("\n==============================")
print("RETRIEVED CONTEXT")
print("==============================\n")

print(context)
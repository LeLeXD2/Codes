import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

VECTOR_STORE_ID = os.getenv(
    "RAG_VECTOR_STORE_ID"
)


# ==========================================
# RETRIEVE CONTEXT
# ==========================================

def retrieve_context(question):

    if not VECTOR_STORE_ID:

        print("ERROR: RAG_VECTOR_STORE_ID is missing.")

        return ""

    question = question[:4000]

    try:

        results = client.vector_stores.search(
            vector_store_id=VECTOR_STORE_ID,
            query=question
        )

        print("\n==============================")
        print("RAG SEARCH")
        print("==============================")

        print("Query:", question)
        print("Results found:", len(results.data))

        context_parts = []

        for result in results.data:

            if hasattr(result, "content"):

                for item in result.content:

                    if hasattr(item, "text"):

                        context_parts.append(
                            item.text
                        )

        context = "\n\n".join(context_parts)

        return context

    except Exception as e:

        print("\nRAG retrieval error:")
        print(e)

        return ""
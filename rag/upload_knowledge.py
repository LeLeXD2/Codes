import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

KNOWLEDGE_DIR = Path("knowledge")


def get_markdown_files():

    return list(KNOWLEDGE_DIR.rglob("*.md"))


def upload_files():

    files = get_markdown_files()

    print(f"Found {len(files)} markdown files.")

    if not files:

        print("No markdown files found.")

        return

    # ==========================================
    # CREATE VECTOR STORE
    # ==========================================

    vector_store = client.vector_stores.create(
        name="Financial Advisor Knowledge Base"
    )

    print("\nCreated vector store:")
    print(vector_store.id)

    # ==========================================
    # UPLOAD FILES
    # ==========================================

    for path in files:

        print(f"\nUploading: {path}")

        with open(path, "rb") as f:

            uploaded_file = client.files.create(
                file=f,
                purpose="assistants"
            )

        print("File ID:", uploaded_file.id)

        client.vector_stores.files.create(
            vector_store_id=vector_store.id,
            file_id=uploaded_file.id
        )

        print("Added to vector store.")

    # ==========================================
    # OUTPUT
    # ==========================================

    print("\n================================")
    print("VECTOR STORE CREATED")
    print("================================")

    print(vector_store.id)

    print("\nAdd this to your .env file:")

    print(
        f"RAG_VECTOR_STORE_ID={vector_store.id}"
    )


if __name__ == "__main__":

    upload_files()
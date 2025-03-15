import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Index configuration
INDEX_NAME = "economic-survey-index"
DIMENSION = 384  # Adjust based on embedding model
METRIC = "cosine"

def create_pinecone_index():
    """Creates a new Pinecone index if it doesn't exist."""
    existing_indexes = pc.list_indexes().names()

    if INDEX_NAME in existing_indexes:
        print(f"✅ Index '{INDEX_NAME}' already exists.")
    else:
        print(f"🚀 Creating index '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric=METRIC,
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print(f"🎯 Index '{INDEX_NAME}' created successfully!")

if __name__ == "__main__":
    create_pinecone_index()

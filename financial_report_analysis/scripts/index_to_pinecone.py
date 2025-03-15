import os
import time
import pinecone
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "economic-survey-index"
PROCESSED_TEXT_DIR = "financial_report_analysis/processed_text"
METADATA_LIMIT = 400  # Limit metadata size (Safe limit < 500 chars)

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if the index exists; if not, create one
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,  # Embedding size for all-MiniLM-L6-v2
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-west-2")  # Update region if needed
    )
    time.sleep(10)  # Wait for index creation

# Connect to the index
index = pc.Index(INDEX_NAME)

# Load Sentence-Transformers model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Function to index documents
def index_documents():
    for file_name in os.listdir(PROCESSED_TEXT_DIR):
        file_path = os.path.join(PROCESSED_TEXT_DIR, file_name)
        print(f"🔄 Processing: {file_name}")

        # Read text content
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        # Split text into chunks
        chunks = text.split("\n\n")  # Split by paragraphs

        # Generate embeddings
        embeddings = model.encode(chunks, convert_to_numpy=True)

        # Prepare data for Pinecone
        vectors = []
        for i, (embedding, chunk) in enumerate(zip(embeddings, chunks)):
            metadata_text = chunk[:METADATA_LIMIT]  # Truncate metadata
            vectors.append(
                (f"{file_name}_{i}", embedding.tolist(), {"text": metadata_text})
            )

        # Upload to Pinecone in batches (handle size errors)
        try:
            index.upsert(vectors)
            print(f"✅ Indexed {len(vectors)} chunks from {file_name}")
        except Exception as e:
            print(f"❌ Error uploading {file_name}: {str(e)}")

# Run the indexing process
index_documents()
print("🎯 All documents indexed successfully!")

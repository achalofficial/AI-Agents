import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, CrossEncoder
from pinecone import Pinecone

# Load API keys from .env
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define index name
INDEX_NAME = "economic-survey-index"

# Check if index exists
if INDEX_NAME not in pc.list_indexes().names():
    raise ValueError(f"❌ Index '{INDEX_NAME}' not found in Pinecone. Check the index name.")

# Connect to index
index = pc.Index(INDEX_NAME)

# Load embedding model (for vector search)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load cross-encoder for re-ranking
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def get_embedding(text):
    """Generate embeddings using Sentence Transformers."""
    return embedding_model.encode(text).tolist()

def query_pinecone(user_query, top_k=10, final_results=3):
    """Query Pinecone and re-rank results using a cross-encoder."""
    try:
        # Step 1: Retrieve from Pinecone
        query_vector = get_embedding(user_query)
        response = index.query(vector=query_vector, top_k=top_k, include_metadata=True)

        if "matches" not in response or not response["matches"]:
            print("\n⚠️ No relevant results found.")
            return

        # Step 2: Extract text for re-ranking
        candidate_texts = [match["metadata"]["text"] for match in response["matches"]]
        if not candidate_texts:
            print("\n⚠️ No relevant text found in retrieved results.")
            return

        # Step 3: Re-rank using cross-encoder
        scores = reranker.predict([(user_query, text) for text in candidate_texts])

        # Step 4: Sort by relevance
        ranked_results = sorted(zip(candidate_texts, scores), key=lambda x: x[1], reverse=True)

        # Step 5: Display top results
        print("\n🔎 Re-ranked Query Results:")
        for i, (text, score) in enumerate(ranked_results[:final_results]):
            print(f"\n📌 Rank {i+1} (Score: {score:.4f})")
            print(f"📝 Text: {text[:500]}...")  # Show first 500 chars

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    user_query = input("Enter your query: ")
    query_pinecone(user_query)

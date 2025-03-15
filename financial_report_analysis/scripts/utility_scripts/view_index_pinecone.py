import os
import pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# List all indexes
print("\n📌 Available Pinecone Indexes:")
print(pc.list_indexes().names())
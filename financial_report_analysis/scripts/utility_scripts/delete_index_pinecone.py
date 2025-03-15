import os
import pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Delete the index
INDEX_TO_DELETE = "economic-survey-index"

if INDEX_TO_DELETE in pc.list_indexes().names():
    print(f"\n🛠️ Deleting Pinecone index: {INDEX_TO_DELETE}...")
    pc.delete_index(INDEX_TO_DELETE)
    print("✅ Index deleted successfully!")
else:
    print("⚠️ Index not found.")
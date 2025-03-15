import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# List existing indexes
existing_indexes = pc.list_indexes().names()
print("Existing indexes:", existing_indexes)

# Define index name
index_name = "my-index"

# Check if the index exists; if not, create one
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=1536,  # Set according to your data
        metric="euclidean",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),  # Free-tier supported region
    )
    print(f"Created index: {index_name}")
else:
    print(f"Index '{index_name}' already exists.")

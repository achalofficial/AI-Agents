from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Pinecone API key
pinecone_api_key = os.getenv("PINECONE_API_KEY")

if pinecone_api_key:
    print("Pinecone API Key found!")
else:
    print("Pinecone API Key NOT found. Check your .env file.")

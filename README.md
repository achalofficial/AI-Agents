# Economic Survey AI Agent

## Overview
This project is an AI-powered agent that analyzes and answers questions related to Economic Survey documents. It processes, indexes, and queries large financial documents using a vector database to provide relevant responses.

## Algorithms Used
1. **Text Chunking & Preprocessing**
   - Converts Economic Survey PDFs into text.
   - Splits text into manageable chunks.
   - Cleans and preprocesses the text before indexing.

2. **Embedding Generation**
   - Generates vector embeddings using a free, open-source embedding model (e.g., `all-MiniLM-L6-v2`).
   - Ensures each chunk is transformed into an efficient numerical representation.

3. **Vector Storage & Retrieval**
   - Stores embeddings in **Pinecone**, a vector database.
   - Uses **semantic search** to find relevant chunks based on user queries.

4. **Hybrid Query Re-Ranking**
   - Retrieves top-k results using vector similarity.
   - Re-ranks the results using an LLM to improve answer relevance.

## AI Agent Architecture
- **Retrieval-Augmented Generation (RAG)**
  - The agent first retrieves relevant Economic Survey document chunks from Pinecone.
  - The retrieved content is used as context to generate final answers using an LLM.

## Tech Stack
- **Python** - Core development language.
- **Pinecone** - Vector database for storing and querying document embeddings.
- **Hugging Face Transformers** - Used for open-source embedding generation.
- **FastAPI (Future Scope)** - Planned for API deployment.
- **PyMuPDF / pdfplumber** - PDF processing.
- **dotenv** - Manages environment variables securely.

## Running the Project

### 1. Setup
Ensure you have Python and virtual environment set up:
```bash
python -m venv myenv
source myenv/bin/activate  # On macOS/Linux
myenv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

### 2. Indexing New Data
If new Economic Survey documents need to be indexed:
```bash
python financial_report_analysis/scripts/index_to_pinecone.py
```
This will process and store the new document chunks in Pinecone.

### 3. Querying the AI Agent
To ask questions from the indexed data:
```bash
python financial_report_analysis/scripts/query_pinecone.py
```
Enter your query when prompted.

## Additional Scripts & Files
- **`utility_scripts/`** - Contains helper scripts such as:
  - `delete_index.py` - Deletes an existing Pinecone index.
  - `list_indexes.py` - Lists all available Pinecone indexes.
- **`.env`** - Stores API keys securely.
- **`financial_report_analysis/scripts/`** - Core scripts for indexing and querying data.
- **`data/`** - Directory containing Economic Survey PDFs.

## Future Enhancements
- Improve LLM integration for better responses.
- Develop a FastAPI-based web interface.
- Implement more advanced re-ranking techniques.

---
This project enables efficient and AI-driven analysis of Economic Survey documents. 🚀


import os
import fitz  # PyMuPDF

# Define data directory
DATA_DIR = os.path.abspath("financial_report_analysis/data")
OUTPUT_DIR = os.path.abspath("financial_report_analysis/extracted_text")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extract text from a single PDF file."""
    print(f"Extracting from: {pdf_path}")  # Debug print
    text = ""

    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text("text")
            print(f"Page {page_num}: {len(page_text)} chars extracted")  # Debug print
            text += page_text + "\n"

    return text

def process_all_pdfs():
    """Process all PDFs in the data directory."""
    print("Processing PDFs...")  # Debug print

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(DATA_DIR, filename)
            print(f"Reading: {pdf_path}")  # Debug print
            
            extracted_text = extract_text_from_pdf(pdf_path)

            # Save extracted text
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(OUTPUT_DIR, txt_filename)

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            
            print(f"✅ Saved extracted text to: {txt_path}")

if __name__ == "__main__":
    process_all_pdfs()

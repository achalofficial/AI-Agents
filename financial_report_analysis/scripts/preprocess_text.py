import os
import re

# Get absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get `financial_report_analysis`
EXTRACTED_TEXT_DIR = os.path.join(BASE_DIR, "extracted_text")
PROCESSED_TEXT_DIR = os.path.join(BASE_DIR, "processed_text")

# Ensure processed_text directory exists
os.makedirs(PROCESSED_TEXT_DIR, exist_ok=True)

def clean_text(text):
    """Preprocess text by removing special characters and normalizing spaces."""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'[^a-zA-Z0-9.,!?;:\-\s]', '', text)  # Remove special characters
    return text.strip()

def preprocess_text(file_path):
    """Read, clean, and save preprocessed text."""
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    
    cleaned_text = clean_text(text)

    # Save the cleaned text
    file_name = os.path.basename(file_path)
    output_path = os.path.join(PROCESSED_TEXT_DIR, file_name)
    
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(cleaned_text)
    
    print(f"✅ Processed and saved: {output_path}")

if __name__ == "__main__":
    print("🔄 Preprocessing extracted text...")

    if not os.path.exists(EXTRACTED_TEXT_DIR):
        print(f"❌ ERROR: Extracted text directory not found: {EXTRACTED_TEXT_DIR}")
        exit(1)

    for file_name in os.listdir(EXTRACTED_TEXT_DIR):
        file_path = os.path.join(EXTRACTED_TEXT_DIR, file_name)
        preprocess_text(file_path)

    print("✅ Preprocessing complete!")

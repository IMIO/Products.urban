from PyPDF2 import PdfReader
import json

# Path to your existing local PDF
pdf_path = "src/Products.urban/src/Products/urban/scripts/rubriques_theme.pdf"

# Read the PDF
reader = PdfReader(pdf_path)

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text() or ""

# Convert text to JSON
data = {"content": text}

# Save as JSON file
with open("output_rubrics.json", "w",) as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(" Saved JSON with extracted text to output_rubrics.json")


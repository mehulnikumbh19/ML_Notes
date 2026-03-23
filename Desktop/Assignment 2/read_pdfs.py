import pypdf

def extract_text(pdf_path):
    print(f"--- Extracting from {pdf_path} ---")
    try:
        reader = pypdf.PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            print(f"Page {i+1}:")
            print(page.extract_text())
            print("-" * 40)
    except Exception as e:
        print(f"Error: {e}")

extract_text("Gaming Ballot Data Description.pdf")
extract_text("IS670-Assignment2-2.pdf")

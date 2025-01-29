import PyPDF2

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.

    Raises:
        FileNotFoundError: If the PDF file is not found.
        PyPDF2.PdfReadError: If there's an error reading the PDF.
    """

    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() or ""  # Handle empty pages
            return text
    except FileNotFoundError:
        print(f"PDF file not found: {pdf_path}")
        return ""
    except PyPDF2.PdfReadError as e:
        print(f"Error reading PDF: {e}")
        return ""
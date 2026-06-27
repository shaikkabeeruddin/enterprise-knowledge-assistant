from PyPDF2 import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:  # handle empty pages
            text += extracted + "\n"

    return text
import pypdf
from io import BytesIO

async def extract_text_from_pdf(pdf_file: BytesIO) -> str:
    pdf_reader = pypdf.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text 
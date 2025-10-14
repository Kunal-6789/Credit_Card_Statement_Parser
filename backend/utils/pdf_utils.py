import pdfplumber
from pdf2image import convert_from_bytes # pyright: ignore[reportMissingImports]
import pytesseract # pyright: ignore[reportMissingImports]
from fastapi import UploadFile
from io import BytesIO

async def extract_text_from_uploadfile(file: UploadFile):
    """
    Extract text from a PDF UploadFile using pdfplumber.
    Returns extracted text.
    """
    file_bytes = await file.read()
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


async def extract_text_from_uploadfile_with_ocr(file: UploadFile):
    """
    Extract text from a PDF UploadFile using OCR fallback.
    Returns extracted text.
    """
    file_bytes = await file.read()
    pages = convert_from_bytes(file_bytes)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page) + "\n"
    return text


# # utils/pdf_utils.py
# import pdfplumber # pyright: ignore[reportMissingImports]
# from typing import List
# import tempfile


# def extract_text_from_pdf_file(file_path: str) -> str:
#     text_parts: List[str] = []
#     with pdfplumber.open(file_path) as pdf:
#         for page in pdf.pages:
#             text_parts.append(page.extract_text() or "")
#     return "\n".join(text_parts)


# # helper to read from UploadFile (Starlette UploadFile)
# async def extract_text_from_uploadfile(upload_file) -> str:
# # write to a temp file and reuse extract_text_from_pdf_file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         contents = await upload_file.read()
#         tmp.write(contents)
#         tmp.flush()
#         tmp_path = tmp.name
#         text = extract_text_from_pdf_file(tmp_path)
#         return text

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


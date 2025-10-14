# # main.py
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from utils.pdf_utils import extract_text_from_uploadfile
# from utils.detect_bank import detect_bank_from_text
# from parsers import PARSERS
# import uvicorn


# app = FastAPI()


# # allow CORS from frontend dev server
# app.add_middleware(
# CORSMiddleware,
# allow_origins=["http://localhost:5173"],
# allow_credentials=True,
# allow_methods=["*"],
# allow_headers=["*"],
# )


# @app.post("/parse")
# async def parse_pdf(file: UploadFile = File(...)):
# 	if not file.filename.lower().endswith(".pdf"):
# 		raise HTTPException(status_code=400, detail="Only PDF files are supported")

# 	text = await extract_text_from_uploadfile(file)
# 	bank_key = detect_bank_from_text(text)
# 	if bank_key == "unknown":
# 		# fall back: try generic quick extraction
# 		# simple heuristics
# 		return {"bank": "unknown", "data": {"raw_text_snippet": text[:1000]}}

# 	parser_cls = PARSERS.get(bank_key)
# 	if not parser_cls:
# 		raise HTTPException(status_code=500, detail="Parser not implemented")

# 	parser = parser_cls(text)
# 	data = parser.parse()
# 	return {"bank": bank_key, "data": data}


# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.pdf_utils import extract_text_from_uploadfile, extract_text_from_uploadfile_with_ocr
from utils.detect_bank import detect_bank_from_text
from parsers import PARSERS
import uvicorn

app = FastAPI()

# allow CORS from frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/parse")
async def parse_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # 1️⃣ Try normal text extraction
    text = await extract_text_from_uploadfile(file)
    ocr_used = False

    # If text is too short, fallback to OCR
    if not text or len(text.strip()) < 50:
        text = await extract_text_from_uploadfile_with_ocr(file)
        ocr_used = True

    # Detect bank
    bank_key = detect_bank_from_text(text)
    if bank_key == "unknown":
        # fall back: simple heuristics / raw text snippet
        return {"bank": "unknown", "data": {"raw_text_snippet": text[:1000]}, "ocr_used": ocr_used}

    # Get parser for detected bank
    parser_cls = PARSERS.get(bank_key)
    if not parser_cls:
        raise HTTPException(status_code=500, detail="Parser not implemented")

    parser = parser_cls(text)
    data = parser.parse()
    data["ocr_used"] = ocr_used  # optional flag for frontend

    return {"bank": bank_key, "data": data}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)

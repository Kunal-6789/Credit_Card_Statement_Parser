# utils/detect_bank.py
import re

def detect_bank_from_text(text: str) -> str:
    txt = text.lower()
    if "hdfc" in txt or "hdfc bank" in txt:
        return "hdfc"
    if "state bank of india" in txt or "sbi" in txt:
        return "sbi"
    if "icici" in txt or "icici bank" in txt:
        return "icici"
    if "axis bank" in txt or "axis" in txt:
        return "axis"
    if "american express" in txt or "amex" in txt:
        return "amex"
    return "unknown"

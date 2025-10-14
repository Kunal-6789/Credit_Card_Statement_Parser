# parsers/hdfc_parser.py
import re
from .base_parser import BaseParser

class SBIParser(BaseParser):
    def parse(self):
        t = self.text
        clean_text = t.replace("\n", " ").replace("\r", " ").strip()
        out = {"issuer": "SBI Bank"}

        # --- Last 4 digits (supports both patterns) ---
        m = re.search(r"Card No.*?(\d{4})", t)  # old pattern
        if not m:
            m = re.search(r"Card Number:\s*XXXX-XXXX-XXXX-(\d{4})", t)  # new pattern
        out["last4"] = m.group(1) if m else None

        # --- Billing cycle (supports both patterns) ---
        m = re.search(r"Statement Period\s*:?([0-9/ -]+to[0-9/ -]+)", t)  # old format
        if not m:
            # new format like '01 Sep 2025 - 30 Sep 2025'
            m = re.search(r"Statement Period:\s*(\d{2} \w+ \d{4})\s*-\s*(\d{2} \w+ \d{4})", t)
            if m:
                out["billing_cycle"] = f"{m.group(1)} - {m.group(2)}"
            else:
                out["billing_cycle"] = None
        else:
            out["billing_cycle"] = m.group(1).strip()

        # --- Payment due date ---
        m = re.search(r"Payment Due Date\s*:?(\d{2}/\d{2}/\d{4})", t)  # old pattern
        if not m:
            m = re.search(r"Payment Due Date:\s*(\d{2} \w+ \d{4})", t)  # new pattern
        out["due_date"] = m.group(1) if m else None

        # --- Total amount due ---
        # Try multiple patterns
        m = re.search(r"Total Amount Due\s*[:\-]?\s*([₹]?[0-9,]+\.\d{2})", clean_text, re.IGNORECASE)
        if not m:
            m = re.search(r"Total Due\s*[:\-]?\s*([₹]?[0-9,]+\.\d{2})", clean_text, re.IGNORECASE)
        out["total_due"] = m.group(1) if m else None

        return out

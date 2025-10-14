# parsers/base_parser.py
from typing import Dict

class BaseParser:
    def __init__(self, text: str):
        self.text = text

def parse(self) -> Dict:
    """Return a dict with keys: issuer, last4, billing_cycle, due_date, total_due"""
    raise NotImplementedError
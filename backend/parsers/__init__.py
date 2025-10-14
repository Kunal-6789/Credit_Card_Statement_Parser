# parsers/__init__.py
from .hdfc_parser import HDFCParser
from .sbi_parser import SBIParser
from .icici_parser import ICICIParser
from .axis_parser import AxisParser
from .amex_parser import AmexParser


PARSERS = {
"hdfc": HDFCParser,
"sbi": SBIParser,
"icici": ICICIParser,
"axis": AxisParser,
"amex": AmexParser,
}
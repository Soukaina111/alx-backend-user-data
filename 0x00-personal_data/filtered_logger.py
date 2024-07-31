#!/usr/bin/env python3
""" 0. Regex-ing """

import re
from typing import List, Tuple, Callable, Match


def filter_datum(fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    # Create regex pattern to match fields
    pattern = r'|'.join(rf'({field})=\w+' for field in fields)
    # Replace matched fields with redaction
    return re.sub(pattern, lambda m: f'{m.groups()[0]}={redaction}', message)

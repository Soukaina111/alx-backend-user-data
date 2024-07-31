#!/usr/bin/env python3
""" 0. Regex-ing """

import re


def filter_datum(fields, redaction, message, separator):
    # Create regex pattern to match fields
    pattern = r'|'.join(rf'({field})=\w+' for field in fields)
    # Replace matched fields with redaction
    return re.sub(pattern, lambda m: f'{m.groups()[0]}={redaction}', message)

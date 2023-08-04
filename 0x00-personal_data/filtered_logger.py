#!/usr/bin/env python3
"""filtered logger module"""
from typing import List
import re


def filter_datum(fields: List, redaction: str, message: str, separator: str) -> str:  # nopep8
    """filter user data function"""
    for field in fields:
        sub_pattern = fr'{field}.*?(?={separator})'
        message = re.sub(sub_pattern, f'{field}={redaction}', message)
    return message

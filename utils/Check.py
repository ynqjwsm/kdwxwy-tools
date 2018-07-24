import re


def is_float(content):
    pattern = re.compile('-?\d*\.\d+')
    return pattern.fullmatch(content) is not None


def is_int(content):
    pattern = re.compile('-?\d+')
    return pattern.fullmatch(content) is not None



import re, queue


def is_float(content):
    pattern = re.compile('-?\d*\.\d+')
    return pattern.fullmatch(content) is not None


def is_int(content):
    pattern = re.compile('-?\d+')
    return pattern.fullmatch(content) is not None


def is_float_list(source):
    wq = queue.Queue()
    wq.put(source)
    while not wq.empty():
        for item in wq.get():
            if type(item) == list:
                wq.put(item)
            else:
                if not is_float(item):
                    return False
    return True

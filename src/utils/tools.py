import re

def cycle(items:tuple, idx):
    """
    Cycle between each item in the `items` list based on the give index `idx`
    """
    item_count = len(items)
    choice = idx % item_count
    return items[choice]


def is_numeric(value:str):
    """
    Is the given string value number-like?
    """
    is_num = False
    if re.match(r"^(-|\+)?\d+(\.\d+)?$", value):
        is_num = True

    return is_num

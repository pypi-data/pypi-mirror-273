from itertools import chain
import re

from more_itertools import chunked

from .utils import get_date


def split_badge(item):
    """some merit badges are too long like "Emergency Preparedness* 06/20/22"
    fortunately these are all longer than 22 characters, so we split them at the *"""
    if len(item) > 23:
        output = list(item.rsplit(" ", 1))
        return output
    return [item]


def get_full_merit_badges(lines):
    """take a stream of merit badge lines from a pdf"""
    output = chain.from_iterable([split_badge(m) for m in lines])
    data = {}
    for item, date_str in chunked(output, 2):
        badge = parse_merit_badge(item)
        badge["Date"] = get_date(date_str)

        data[badge["Name"]] = badge
    return data


def parse_merit_badge(text):
    pat = re.compile(
        r"""^(.*?)          # merit badge name
                          (\ \((.*)\))?  # optional space and version name
                          (\*)?$         # optional * to denote eagle required
                      """,
        re.X,
    )
    m = pat.match(text)
    if m:
        badge = {
            "Name": m.group(1),
            "Version": m.group(3) or None,
            "Eagle Required": bool(m.group(4)),
        }
    else:
        badge = {
            "Name": text,
            "Version": None,
            "Eagle Required": False,
        }
    return badge

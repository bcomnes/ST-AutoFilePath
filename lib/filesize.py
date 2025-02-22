#!/usr/bin/env python

"""Bits and bytes related humanization."""

from typing import Dict, Iterable, Union


suffixes = {
    "decimal": ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"),
    "binary": ("KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"),
    "gnu": "KMGTPEZY",
}  # type: Dict[str,Iterable[str]]


def naturalsize(value: Union[int, float, str], binary: bool = False, gnu: bool = False, format: str = "%.1f") -> str:
    """Format a number of bytes like a human readable filesize (e.g. 10 kB).

    By default, decimal suffixes (kB, MB) are used.

    Non-GNU modes are compatible with jinja2's `filesizeformat` filter.

    Examples:
    ```python
    >>> naturalsize(3000000)
    '3.0 MB'
    >>> naturalsize(300, False, True)
    '300B'
    >>> naturalsize(3000, False, True)
    '2.9K'
    >>> naturalsize(3000, False, True, "%.3f")
    '2.930K'
    >>> naturalsize(3000, True)
    '2.9 KiB'
    ```

    Args:
        value (int, float, str): Integer to convert.
        binary (bool): If `True`, uses binary suffixes (KiB, MiB) with base
            2<sup>10</sup> instead of 10<sup>3</sup>.
        gnu (bool): If `True`, the binary argument is ignored and GNU-style
            (`ls -sh` style) prefixes are used (K, M) with the 2**10 definition.
        format (str): Custom formatter.

    Returns:
        str: Human readable representation of a filesize.
    """

    if gnu:
        suffix = suffixes["gnu"]
    elif binary:
        suffix = suffixes["binary"]
    else:
        suffix = suffixes["decimal"]

    base = 1024 if (gnu or binary) else 1000
    bytes = float(value)
    abs_bytes = abs(bytes)

    if abs_bytes == 1 and not gnu:
        return "%d Byte" % bytes
    elif abs_bytes < base and not gnu:
        return "%d Bytes" % bytes
    elif abs_bytes < base and gnu:
        return "%dB" % bytes

    unit = 1
    s = ""
    for i, s in enumerate(suffix):
        unit = base ** (i + 2)
        if abs_bytes < unit and not gnu:
            return f"{format} %s" % ((base * bytes / unit), s)
        elif abs_bytes < unit and gnu:
            return f"{format}%s" % ((base * bytes / unit), s)

    if gnu:
        return f"{format}%s" % ((base * bytes / unit), s)

    return f"{format} %s" % ((base * bytes / unit), s)

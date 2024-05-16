try:
    import pandas as pd
except ImportError:
    pd = None


class DvcxError(Exception):
    def __init__(self, message):
        super().__init__(message)


def row_to_pandas(args, params):
    data = dict(zip([i.name for i in params], args))
    return pd.Series(data, name=data.get("name"))


def row_list_to_pandas(args, params):
    return pd.DataFrame(args, columns=[i.name for i in params])


def bin_to_array(data):
    return [
        int.from_bytes(data[i : i + 4], byteorder="big") for i in range(0, len(data), 4)
    ]


def array_to_bin(integers):
    return b"".join(int.to_bytes(i, length=4, byteorder="big") for i in integers)


def union_dicts(*dicts):
    """Union dictionaries.
    Equivalent to `d1 | d2 | d3` in Python3.9+ but works in older versions.
    """
    result = None
    for d in dicts:
        if not isinstance(d, dict):
            raise TypeError("All arguments must be dictionaries.")
        if not result:
            result = d.copy()
        else:
            result.update(d)
    return result

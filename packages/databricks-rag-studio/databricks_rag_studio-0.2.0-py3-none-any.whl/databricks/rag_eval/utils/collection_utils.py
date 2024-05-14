"""Utilities for manipulating collections."""

from typing import Mapping, Any, List


def omit_keys(d: Mapping[str, Any], keys: List[str]) -> Mapping[str, Any]:
    """
    Omit keys from a dictionary.
    :param d:
    :param keys:
    :return: A new dictionary with the keys removed.
    """
    return {k: v for k, v in d.items() if k not in keys}

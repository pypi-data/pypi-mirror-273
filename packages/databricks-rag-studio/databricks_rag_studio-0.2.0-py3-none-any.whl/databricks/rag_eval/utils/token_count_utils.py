"""Utilities for computing token count."""

import functools
import os
from typing import Optional


def compute_token_count(s: Optional[str]) -> Optional[int]:
    """
    Compute the token count of the input string using tiktoken.

    Returns None if the input string is None or not a string.

    :param s: The input string
    :return: The token count of the input string
    """
    if s is None:
        return None
    if not isinstance(s, str):
        return None

    return len(_cached_tiktoken_encoding().encode(s))


@functools.lru_cache(maxsize=8)
def _cached_tiktoken_encoding():
    """
    Load the tiktoken encoding and cache it.
    """
    import tiktoken

    # ref: https://github.com/openai/tiktoken/issues/75
    os.environ["TIKTOKEN_CACHE_DIR"] = ""
    return tiktoken.get_encoding("cl100k_base")

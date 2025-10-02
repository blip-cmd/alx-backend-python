#!/usr/bin/env python3
"""
utils module
"""
import requests
from functools import wraps
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Access nested map with key path.
    
    Args:
        nested_map: A nested map
        path: A sequence of key representing a path to the value
    
    Returns:
        The value at the specified path in the nested map
        
    Raises:
        KeyError: If the path doesn't exist in the nested map
    """
    for key in path:
        try:
            nested_map = nested_map[key]
        except (KeyError, TypeError):
            raise KeyError(key)
    return nested_map


def get_json(url: str) -> Dict:
    """
    Get JSON from remote url.
    
    Args:
        url: The URL to fetch JSON from
        
    Returns:
        The JSON response as a dictionary
    """
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> Callable:
    """
    Decorator to memoize a method.
    
    Args:
        fn: The function to memoize
        
    Returns:
        The memoized function
    """
    attr_name = "_{}".format(fn.__name__)

    @wraps(fn)
    def memoized(self):
        """"memoized wraps"""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)
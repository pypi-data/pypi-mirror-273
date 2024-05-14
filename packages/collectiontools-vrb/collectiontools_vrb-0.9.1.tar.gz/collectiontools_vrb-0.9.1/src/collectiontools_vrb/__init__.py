"""
# collectiontools_vrb

Various tools to handle collection I/O and transformations.

  - On PyPI: https://pypi.org/project/collectiontools-vrb/
  - On GitHub: https://github.com/v-r-b/collectiontools_vrb 

## \_\_init__.py

```function update_dict_from_url()```

Read collection data from the given URL. 

```function update_dict_from_key_value_file()```

Read collection data from the given file. 

```function dict_contains_path()```

Tests if a given path is a valid key inside the given dict.

```function update_dict_from_json_file()```
  
Read collection data from config file. Check for mandatory keys.

## collectiontranslator.py

```class CollectionTranslator```

Search strings, lists or dicts for placeholders using a 
regular expression provided by the user. Replace the matches 
with a value provided by a translator function, which is 
as well provided by the user.
"""

from __future__ import annotations
    
import asyncio
from types import FrameType
import aiohttp
import json
import traceback
import sys, inspect
from typing import Any as Any

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from _typeshed import SupportsWrite

from collectiontools_vrb.collectiontranslator import *

async def _update_dict_from_url(d: dict, url: str, sep: str, strip: bool) -> aiohttp.ClientResponse:
    """Internal method using asyncio to carry out
    the task of updateFromURL.
    See: updateDictFromURL(d, url, sep)
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.ok:
                text: str = await response.text()
            else:
                raise Exception(
                    f"Unable to read from URL {url}. Status {response.status}")
            for l in text.splitlines():
                parts = l.split(sep, 1)
                if len(parts) == 2:
                    if strip:
                        d[parts[0].strip()] = parts[1].strip()
                    else:
                        d[parts[0]] = parts[1]
    return response
    
def update_dict_from_url(d: dict, url: str, *,
            sep: str = "=", strip: bool = True,
            reraise_exc: bool = False, 
            print_errors_to: SupportsWrite[str]|None = None) -> bool:
    """Read collection data from the given URL. 

    The data must consist of lines of key-value-pairs
    separated by the given sep string. Sample line:
    If sep == "=", NAME=Miller results to a key-value-pair "NAME":"Miller".

    Args:
        d (dict): dictionary to be updated
        url (str): URL to read from
        sep (str, optional): String to separate key from value. Defaults to "=".
        strip (bool, optional): Strip trailing and leading whitespace from keys and values? Defaults to True.
        reraise_exc (bool, optional): reraise caught exceptions if True, otherwise
            print exception info if print_errors == True. Defaults to False.
        print_errors_to (SupportsWrite[str], optional): stream to print error information to, 
            i.e. missing mandatory keys, error on opening file etc. Defaults to None.
            If not None, print_errors_to will be passed to the print function as "file=" argument.

    Raises:
        Exception: if URL can not be read properly (only if reraise_exc == True)

    Returns:
        True, if HTTP status code of get(url) operation is less than 400, False otherwise
    """
    try:
        response = asyncio.run(_update_dict_from_url(d, url, sep, strip))
    except Exception as exc:
        # reraise exception if raiseExc == True
        if reraise_exc:
            raise
        # else print error if requested to do so
        elif print_errors_to:
            print(traceback.format_exc(), file=print_errors_to)
        return False
    return response.ok

def update_dict_from_key_value_file(d: dict, path: str, *,
            sep: str = "=", strip: bool = True,
            reraise_exc: bool = False, 
            print_errors_to: SupportsWrite[str]|None = None) -> bool:
    """Read collection data from the given file. 

    The data must consist of lines of key-value-pairs
    separated by the given sep string. Sample line:
    If sep == "=", NAME=Miller results to a key-value-pair "NAME":"Miller".

    Reraise an exception (e.g. FileNotFound) only if argument == True, 
    otherwise print exception information only.

    Args:
        d (dict): dictionary to be updated
        path (str): file descriptor or path to open
        sep (str, optional): String to separate key from value. Defaults to "=".
        strip (bool, optional): Strip trailing and leading whitespace from keys and values? Defaults to True.
        reraise_exc (bool, optional): reraise caught exceptions if True, otherwise
            print exception info if print_errors == True. Defaults to False.
        print_errors_to (SupportsWrite[str], optional): stream to print error information to, 
            i.e. missing mandatory keys, error on opening file etc. Defaults to None.
            If not None, print_errors_to will be passed to the print function as "file=" argument.

    Returns:
        bool: True on success, False otherwise

    Raises:
        Exception: FileNotFound (only if reraise_exc == True)
    """
    try:
        with open(path) as f:
            text: list[str] = f.read().splitlines()
        for l in text:
            parts = l.split(sep, 1)
            if len(parts) == 2:
                if strip:
                    d[parts[0].strip()] = parts[1].strip()
                else:
                    d[parts[0]] = parts[1]
        return True
    except Exception as exc:
        # reraise exception if raiseExc == True
        if reraise_exc:
            raise
        # else print error if requested to do so
        elif print_errors_to:
            print(traceback.format_exc(), file=print_errors_to)
        return False

def dict_contains_path(nested_dict: dict, keypath: str, *, sep: str = ".") -> bool:
    """ Tests if a given path is a valid key inside the given dict.
    It is assumed, that the key path elements are seperated by ".".
    To change this, use argument sep=...

    Args:
        nested_dict (dict): (nested) dictionary to search in
        keypath (str): key to be found (elements separated by sep)
        sep (str, optional): key element separator to be used. Defaults to ".".

    Returns:
        bool: True if the key could be found, False otherwise
    """
    # Split key path in first elements and all the rest
    key_parts = keypath.split(sep, 1)
    num_key_parts = len(key_parts)
    if num_key_parts == 1:
        # found single key. Test if it is in the dict:
        return key_parts[0] in nested_dict
    else:
        # test for first key element. 
        if key_parts[0] in nested_dict:
            # if found, go one level deeper with the nested dict
            # found at [key_parts[0]] und the rest of the key
            dict_part = nested_dict[key_parts[0]]
            return dict_contains_path(dict_part, key_parts[1], sep=sep)
        else:
            # if not found, there's no need to process
            # the rest of the key
            return False

def update_dict_from_json_file(d: dict, file: str, *,
                               mandatory_keys: list[str] = [], 
                               reraise_exc: bool = False,
                               print_errors_to: SupportsWrite[str]|None = None) -> bool:
    """ Read collection data from config file. Check for mandatory keys.
    Reraise an exception (e.g. FileNotFound) only if reraise_exc == True, 
    otherwise print exception information only if print_errors_to is not None.

    Args:
        d (dict): dictionary to be updated
        file (str): file descriptor or path to open
        mandatory_keys (list[str], optional): check for these keys in the dict
            If not found, return false and don't update dict. Defaults to [].
        reraise_exc (bool, optional): reraise caught exceptions if True, otherwise
            print exception info if print_errors == True. Defaults to False.
        print_errors_to (SupportsWrite[str], optional): stream to print error information to, 
            i.e. missing mandatory keys, error on opening file etc. Defaults to None.
            If not None, print_errors_to will be passed to the print function as "file=" argument.

    Returns:
        bool: True on success, False otherwise
    """

    result = None
    try:
        # read config file:
        with open(file) as fp:
            result = json.load(fp)

        # check for mandatory keys:
        for key in mandatory_keys:
            if not dict_contains_path(result, key, sep="."):
                if print_errors_to:
                    cf = inspect.currentframe()
                    if isinstance(cf, FrameType):
                        print(cf.f_code.co_name,
                              f": missing key '{key}' in file '{file}'", 
                              file=print_errors_to)
                return False

        # update d only in case all mandatory keys could be found
        d.update(result)
        return True
    except Exception as exc:
        # reraise exception if raiseExc == True
        if reraise_exc:
            raise
        # else print error if requested to do so
        elif print_errors_to:
            print(traceback.format_exc(), file=print_errors_to)
        return False

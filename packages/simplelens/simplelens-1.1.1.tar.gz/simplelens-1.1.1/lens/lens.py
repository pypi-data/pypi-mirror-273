# Copyright 2023 Nathan Menge - nathan.menge@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This module is included as it is useful to this project and I wasn't ready to open source it, but hopefully I will do
# that soon.  At which point I will remove this and pull it as a dependency through pip.

from collections.abc import Iterable, Mapping
from functools import partial, reduce
from typing import Any, cast, Optional, Sequence


def lens(collection: Iterable,
         keys: Sequence,
         always_flatten: Optional[bool] = None) -> Any:
    """
    This function implements the "lens" functional pattern that is used to extract data from within complex
    data structures.
    A specific feature of this implementation that is perhaps atyipical, is that it only pulls values from Mappings and
    Objects.  When it encounters something List-like, it maps the current key across the list and pulls the values from
    the list elements up to the list.  It does not flatten the lists.
    :param collection: The collection to extract data from
    :type collection: Iterable
    :param keys: Keys used for extraction
    :type keys: List[Union[int, str, tuple[int, str, dict]]
    :param always_flatten: Flag to set flattening behavior across the entire function call
    :type always_flatten: bool
    :return: Returns data found within the data structure
    :rtype: Any
    """
    if always_flatten is None:
        always_flatten = True
    reducer = partial(_reducer, always_flatten=always_flatten)
    try:
        return reduce(reducer, keys, collection)
    except AttributeError as ae:
        msg = f"{ae}.\nAttempting to focus lens across key set {keys}"
        raise FocusingError(msg) from None
    except IndexError:
        raise FocusingError(f"Collection emptied while attempting to focus across key set: {keys}") from None
    except KeyError as ke:
        collection = cast(Mapping, collection)
        collection_key_list = list(collection.keys())
        joined_keys = ', '.join(collection_key_list)
        msg = (f"Could not find key {ke} in collection with keys '{joined_keys}'.\nAttempting to focus lens "
               f"across key set {keys}")
        raise FocusingError(msg) from None


def _reducer(acc: Mapping | Sequence, i: int | str | tuple, always_flatten: bool) -> Any:
    """
    This is the reducer function for the lens.
    :param acc: The collection to reduce
    :type acc: Any
    :param i: The key to reduce the collection by, which in this case is to pull a value from the collection
    based on this value
    :type i: Union[dict, int, str, tuple]
    :return: Returns the focused result set, which can be almost anything
    :rtype: Any
    """
    j, args = unpack_element(i)
    force_map = args.get('force_map', False)
    flatten = force_map or args.get('flatten', always_flatten)
    if isinstance(acc, Mapping):
        # It is a Mapping which implies dict-like behavior
        return acc[j]
    if isinstance(acc, Sequence) and not isinstance(acc, str):
        # It is a Sequence, which implies List-like behavior, but we keep out strings, which are also list-like
        if isinstance(j, int) and not force_map:
            return acc[j]
        mapped_list = list(map(lambda x: _reducer(x, j, always_flatten), acc))  # type: ignore
        if flatten:
            mapped_list = _flatten(mapped_list)
        return mapped_list
    else:
        # It is neither a Mapping or Sequence, which only really leaves it as an attribute
        try:
            return getattr(acc, str(i))
        except AttributeError:
            raise AttributeError(f"Object with value '{acc}' has no attribute '{i}'") from None


def unpack_element(element: int | str | tuple[int | str, dict]) -> tuple[int | str, dict]:
    if isinstance(element, str):
        return element, {}
    if isinstance(element, int):
        return element, {}
    if isinstance(element, tuple):
        return unpack_tuple(element)
    raise ValueError(f"Element {element} is not a str, int, or tuple[2] and is not supported")


def unpack_tuple(element: tuple[int | str, dict]) -> tuple[int | str, dict]:
    tuple_length = len(element)
    if tuple_length == 2:
        return element
    if tuple_length == 1:
        return element[0], {}
    if tuple_length < 1:
        raise ValueError('Element is an empty tuple')
    raise ValueError(f"Unpacking a tuple: {element} that has more than 2 elements")


def _flatten(tall_list: list[list]) -> list:
    """
    This method is used to flatten a single level of nested list.
    :param tall_list: List to flatten
    :return: List
    """
    return_val = []
    for el in tall_list:
        if isinstance(el, Sequence) and not isinstance(el, str):
            return_val.extend(el)
        else:
            return_val.append(el)
    return return_val


class FocusingError(Exception):
    pass

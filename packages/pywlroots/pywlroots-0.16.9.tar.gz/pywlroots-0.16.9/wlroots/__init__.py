# Copyright (c) Sean Vig 2018

from __future__ import annotations

import weakref
from typing import Any, Callable, TypeVar

from ._ffi import ffi, lib
from .version import version as _version

__wlroots_version__ = (
    f"{lib.WLR_VERSION_MAJOR}.{lib.WLR_VERSION_MINOR}.{lib.WLR_VERSION_MICRO}"
)

__version__ = _version

_weakkeydict: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()

T = TypeVar("T")


class Ptr:
    """Add equality checks for objects holding the same cdata

    Objects that reference the same cdata objects will be treated as equal.
    Note that these objects will still have a different hash such that they
    should not collide in a set or dictionary.
    """

    _ptr: ffi.CData

    def __eq__(self, other) -> bool:
        """Return true if the other object holds the same cdata"""
        return hasattr(other, "_ptr") and self._ptr == other._ptr

    def __hash__(self) -> int:
        """Use the hash from `object`, which is unique per object"""
        return super().__hash__()


class PtrHasData(Ptr):
    """
    Add methods to get and set the void *data member on the wrapped struct. The value
    stored can be of any Python type.
    """

    @property
    def data(self) -> Any | None:
        """Return any data that has been stored on the object"""
        if self._ptr.data == ffi.NULL:
            return None
        return ffi.from_handle(self._ptr.data)

    @data.setter
    def data(self, data: Any) -> None:
        """Store the given data on the current object"""
        if data is None:
            # Clear the data reference.
            if self.data in _weakkeydict:
                del _weakkeydict[self.data]
            self._ptr.data = ffi.NULL
            return

        # We adding a new data reference.
        if isinstance(data, ffi.CData):
            # We were already provided with a handle. The allows users of this code to
            # handle memory themselves.
            handle = data
        else:
            # We need to make a new handle. This keeps the data alive.
            handle = ffi.new_handle(data)
            _weakkeydict[data] = handle
        self._ptr.data = handle


def str_or_none(member: ffi.CData) -> str | None:
    """
    Helper function to check struct members for ffi.NULL, returning None, or a char
    array, returning a string.
    """
    if member:
        return ffi.string(member).decode(errors="backslashreplace")
    return None


def ptr_or_null(obj: Ptr | None) -> ffi.CData:
    """
    Helper function to check if the object is None, returning ffi.NULL,
    otherwise the _ptr attribute of the object
    """
    return obj._ptr if obj is not None else ffi.NULL


def instance_or_none(cls: Callable[[ffi.CData], T], ptr: ffi.CData) -> T | None:
    """
    A factory function which returns eiher an instance of T or None.

    The result depends on ``ptr`` if it is ffi.NULL, None will be returned,
    otherwise the result of T(ptr)
    """
    return cls(ptr) if ptr != ffi.NULL else None

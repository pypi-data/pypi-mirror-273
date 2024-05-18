# -*- coding: utf-8 -*-

import pyfrpc

from collections.abc import Mapping, Sequence, ByteString
from conftest import *


def _reencode(value):
    encoded = pyfrpc.encode(pyfrpc.FrpcResponse(value), 0x0201)
    decoded = pyfrpc.decode(encoded)
    return decoded.data


def test_subclass_dict():
    class C(Mapping):
        def __init__(self, data):
            self.data = data

        def __getitem__(self, key):
            return self.data[key]

        def __iter__(self):
            return iter(self.data)

        def __len__(self):
            return len(self.data)

    value = {"hello": "world"}
    value_reencoded = _reencode(C(value))

    assert(value == value_reencoded)


def test_subclass_list():
    class C(Sequence):
        def __init__(self, data):
            self.data = data

        def __getitem__(self, index):
            return self.data[index]

        def __len__(self):
            return len(self.data)

    value = ["hello", "world", 3.14]
    value_reencoded = _reencode(C(value))

    assert(value == value_reencoded)


def test_subclass_bytes():
    class C(ByteString):
        def __init__(self, data):
            self.data = data

        def __getitem__(self, index):
            return self.data[index]

        def __len__(self):
            return len(self.data)

    value = b"hello world"
    value_reencoded = _reencode(C(value))

    assert(value == value_reencoded)

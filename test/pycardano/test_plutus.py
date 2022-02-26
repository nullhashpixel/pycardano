from dataclasses import dataclass
from test.pycardano.util import check_two_way_cbor
from typing import Union

from pycardano.plutus import PlutusData


@dataclass
class MyTest(PlutusData):
    CONSTR_ID = 130

    a: int
    b: bytes


@dataclass
class BigTest(PlutusData):
    CONSTR_ID = 8

    test: MyTest


@dataclass
class LargestTest(PlutusData):
    CONSTR_ID = 9


@dataclass
class VestingParam(PlutusData):
    CONSTR_ID = 1

    beneficiary: bytes
    deadline: int
    testa: Union[BigTest, LargestTest]
    testb: Union[BigTest, LargestTest]


def test_plutus_data():
    key_hash = bytes.fromhex("c2ff616e11299d9094ce0a7eb5b7284b705147a822f4ffbd471f971a")
    deadline = 1643235300000
    testa = BigTest(MyTest(123, b"1234"))
    testb = LargestTest()

    my_vesting = VestingParam(
        beneficiary=key_hash, deadline=deadline, testa=testa, testb=testb
    )
    assert (
        my_vesting.to_cbor()
        == "d87a9f581cc2ff616e11299d9094ce0a7eb5b7284b705147a822f4ffbd471f971a1b0000017e9874d2a0d905019fd8668218829f187b4431323334ffffd9050280ff"
    )
    check_two_way_cbor(my_vesting)
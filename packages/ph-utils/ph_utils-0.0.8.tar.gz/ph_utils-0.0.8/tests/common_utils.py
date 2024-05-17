from decimal import Decimal
from ph_utils.common import is_empty, is_blank, mask_phone, random, json_dumps


def test_is_empty():
    print(is_empty())
    print(is_empty(None))
    print(is_empty(""))
    print(is_empty(" "))
    print(is_empty(" a "))


def test_is_blank():
    print(is_blank())
    print(is_blank(None))
    print(is_blank(""))
    print(is_blank(" "))
    print(is_blank(" a "))


def test_random():
    print(random())
    print(random(only_num=True))
    print(random(only_num=True, first_zero=False))


def test_json_dumps():
    print(json_dumps({"name": "中文", "price": Decimal("0.0001")}, format=True))


def test_mask_phone():
    print(mask_phone("14523456"))


test_mask_phone()

from ph_utils.crypto import b64encode, b64decode


def test_base64_encode():
    print(b64encode("123456"))


def test_base64_decode():
    print(b64decode(b64encode("123456")))


test_base64_decode()

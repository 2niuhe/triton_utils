_DEFAUTL_DEVICE = "cuda"


def set_device(device: str):
    # device such as cuda mlu
    global _DEFAUTL_DEVICE
    _DEFAUTL_DEVICE = device
    print(f"set device type to {_DEFAUTL_DEVICE}")


def get_device():
    return _DEFAUTL_DEVICE

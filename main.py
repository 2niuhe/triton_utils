from triton_utils import create_input, set_device

set_device("cpu")


def main():
    result = create_input((3, 2))
    print("结果:", result)


if __name__ == "__main__":
    main()

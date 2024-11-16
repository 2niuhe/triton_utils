import sys

from src.carlton_template.mod import add_three


def main():
    if len(sys.argv) < 2:
        print("请提供一个数字作为命令行参数")
        return

    try:
        num = float(sys.argv[1])
    except ValueError:
        print("无法将输入转换为数字")
        return

    result = add_three(num)

    print("结果:", result)


if __name__ == "__main__":
    main()

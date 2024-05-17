import sys


def um2dpi(um):
    return 25400 / um


def cli():
    if len(sys.argv) < 2:
        print("Usage: um2dpi <\u03bcm> [<\u03bcm> ...]")
        sys.exit(1)
    ums = [float(um) for um in sys.argv[1:]]
    for um in ums:
        print(f"{um} \u03bcm: {um2dpi(um):.2f} dpi")


if __name__ == "__main__":
    cli()

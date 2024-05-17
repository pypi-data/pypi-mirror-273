import sys


def um2dpi(um):
    return 25400 / um


def dpi2um(dpi):
    return 25400 / dpi


def cli():
    if len(sys.argv) < 2:
        print("Usage: um2dpi [-r] <value> [value ...]")
        print("Convert from um to dpi or vice versa")
        print("Options:")
        print("\t-r: reverse conversion (from dpi to um)")
        sys.exit(1)

    if sys.argv[1] == "-r":
        dpis = [float(dpi) for dpi in sys.argv[2:]]
        ums = [dpi2um(dpi) for dpi in dpis]
        for dpi, um in zip(dpis, ums):
            print(f"{dpi:.1f} dpi: {um:.2f} \u03bcm")
    else:
        ums = [float(um) for um in sys.argv[1:]]
        dpis = [um2dpi(um) for um in ums]
        for um, dpi in zip(ums, dpis):
            print(f"{um:.1f} \u03bcm: {dpi:.2f} dpi")


if __name__ == "__main__":
    cli()

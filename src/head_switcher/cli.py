import argparse
import sys

from head_switcher.core import build_pack


def cli(cli_args):
    parser = argparse.ArgumentParser(
        prog='head-switcher',
        description='',
        epilog='')

    parser.add_argument('folder', help="Path to frontend build folder.")
    parser.add_argument('-o', '--out', help='path to output path', default='./out.frontend')
    args = parser.parse_args(cli_args)
    build_pack(args.folder, args.out)


def run():  # pragma: no cover
    cli(sys.argv[1:])


if __name__ == '__main__':  # pragma: no cover
    run()

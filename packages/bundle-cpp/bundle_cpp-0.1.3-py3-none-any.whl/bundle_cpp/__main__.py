import argparse
import dataclasses
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Optional as Opt

from . import bundle

WD = Path(os.getcwd())


@dataclass
class CLIParam:
    src: Path
    include_paths: List[Path] = dataclasses.field(
        default_factory=list
    )
    dst: Opt[Path] = None
    add_line: bool = False


def cli():
    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-I",
        type=str,
        action="append",
        metavar="include_path",
        default=[WD],
        dest="include_paths",
        help="can be set multiple times.",
    )
    parser.add_argument(
        "-o",
        type=str,
        metavar="out_file",
        # default="generated.cpp",
        dest="dst",
        help="e.g. main_generated.cpp. not set, print stdout.",
    )
    parser.add_argument(
        "-l",
        "--add-line",
        action="store_true",
        help='add #line <__LINE__> "<__FILE__>"',
    )
    g = parser.add_argument_group("required positional")
    g.add_argument(
        "src_file",
        type=str,
        help="e.g. main.cpp",
    )

    args = parser.parse_args()
    include_paths = [
        Path(p).resolve() for p in args.include_paths
    ]
    dst = None if args.dst is None else Path(args.dst).resolve()
    args = CLIParam(
        Path(args.src_file).resolve(),
        include_paths,
        dst,
        add_line=args.add_line,
    )
    res = bundle(
        args.src,
        args.include_paths,
        args.add_line,
    )[:-1]
    if args.dst is None:
        print(res)
        return
    with args.dst.open("w") as f:
        f.write(res)


if __name__ == "__main__":
    cli()

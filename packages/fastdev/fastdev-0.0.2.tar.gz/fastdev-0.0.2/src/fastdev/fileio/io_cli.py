import argparse
import warnings
from typing import IO, cast

import fsspec
from upath import UPath

from fastdev.fileio.io import ucopy

AVAILABLE_COMMANDS = ["cp", "ls", "rm", "cat"]
warnings.filterwarnings("ignore", module="upath")


def main():
    parser = argparse.ArgumentParser(description="UIO CLI")
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("args", nargs="*", help="Arguments for the command")
    args = parser.parse_args()

    if args.command not in AVAILABLE_COMMANDS:
        print(f"Command '{args.command}' not supported")
        return

    if args.command == "ls":
        urlpath = args.args[0] if args.args else "."
        fs = UPath(urlpath).fs
        for item in fs.ls(urlpath):
            if isinstance(item, dict):
                print(item["name"])
            else:
                print(item)

    if args.command == "cat":
        urlpath = args.args[0]
        with fsspec.open(urlpath, "r") as f:
            print(cast(IO, f).read())

    if args.command == "rm":
        urlpath = args.args[0]
        fs = UPath(urlpath).fs
        fs.rm(urlpath, recursive=True)

    if args.command == "cp":
        src_path, dst_path = args.args
        ucopy(src_path, dst_path)

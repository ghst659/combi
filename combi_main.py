#!/usr/bin/env python3

import argparse
from collections.abc import Sequence
import concurrent.futures
import enum
import logging
import pathlib
import subprocess
import sys

import combi

DEFAULT_SEP = ","

class Channel(enum.StrEnum):
    """Enum of possible I/O channels."""
    STDIN = enum.auto()
    STDOUT = enum.auto()
    STDERR = enum.auto()

def main(argv: Sequence[str]) -> int:
    """Combi generator CLI."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("--separator", metavar="SEPARATOR",
                        dest="separator", default=DEFAULT_SEP,
                        help="Intra-segment separator.")
    parser.add_argument("--segment", metavar="SEGMENT",
                        type=lambda s: [i.strip() for i in s.split(DEFAULT_SEP)],
                        dest="patterns", action="append", default=[],
                        help="Segment to be added to the pattern.")
    parser.add_argument("--segment_file", metavar="SEGMENT_FILE",
                        dest="segment_file", type=pathlib.Path, default=None,
                        help="File from which to read segments.")
    parser.add_argument("--concurrency", metavar="CONCURRENCY",
                        type=int, default=4,
                        help="Max level of concurrency.")
    parser.add_argument("--null", metavar="CHANNEL", type=Channel,
                        dest="null", action="append", default=[],
                        help="Null out these channels")
    parser.add_argument("-v","--verbose",
                        dest="verbose", action="store_true",
                        help="run verbosely")
    parser.add_argument("command", nargs="*")
    args = parser.parse_args(args=argv[1:])
    if args.verbose:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s %(asctime)s %(filename)s:%(lineno)d %(message)s")
    subprocess_kwargs = {}
    for c in args.null:
        subprocess_kwargs[c.value] = subprocess.DEVNULL
    logging.info("kwargs: %s", subprocess_kwargs)

    logging.info("template: '%s'", " ".join(args.command))

    patterns = []
    if args.segment_file:
        for raw_line in args.segment_file.read_text().split("\n"):
            if line := raw_line.strip():
                patterns.append(line.split(args.separator))
    patterns.extend(args.patterns)
    logging.info("patterns: %s", patterns)

    key_items = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        results = {}
        for item in combi.genit(patterns):
            command = [w.replace("{}", item) for w in args.command]
            logging.info("command: %s", command)
            avenir = pool.submit(subprocess.run, command, **subprocess_kwargs)
            results[avenir] = item
        for avenir in concurrent.futures.as_completed(results):
            item = results[avenir]
            if avenir.result().returncode == 0:
                key_items.append(item)
                logging.info("%s: PASS", item)
            else:
                logging.info("%s: fail", item)
    logging.info("key_items: %s", key_items)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

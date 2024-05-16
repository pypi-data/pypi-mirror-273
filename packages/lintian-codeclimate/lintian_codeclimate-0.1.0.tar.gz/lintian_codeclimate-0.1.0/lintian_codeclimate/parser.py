# Copyright: 2024 Cardiff University
# SPDX-License-Idenfitifer: MIT

"""Parser for Lintian.
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import argparse
import hashlib
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_DIR = Path(os.getenv('PROJECT_DIR', "."))
CHECK_REGEX = re.compile(
    r"Check: (?P<checkpath>debian\/[\w-]+)",
)
LINE_REGEX = re.compile(
    r"\A(?P<type>[A-Z]):\s+"
    r"(?P<package>[\w-]+):\s+"
    r"(?P<tag>[\w-]+)(\s+)?"
    r"(?P<desc>.*)?"
)
NOTES_REGEX = re.compile(
    r"\AN:(\s+)?(?P<content>.*)",
)
SEVERITY = {
    "I": "info",
    "P": "info",
    "W": "minor",
    "E": "major",
}


def parse_stream(stream):
    issues = []
    current = None
    notes = defaultdict(list)
    for line in stream:
        if match := NOTES_REGEX.match(line):
            content = match.groupdict().get("content", "")
            if current:
                notes[current["tag"]].append(content)
        elif match := LINE_REGEX.match(line):
            params = match.groupdict()
            fingerprint = hashlib.sha1(
                "".join(map(str, params.values())).encode("utf-8"),
            ).hexdigest()
            issues.append({
                "categories": ["Style"],
                "check_name": params["tag"],
                "description": f"{params['tag']} {params['desc']}",
                "fingerprint": fingerprint,
                "severity": SEVERITY.get(params["type"], "info"),
                "type": "issue",
            })
            # record for notes parsing
            current = params
    for tag in notes:
        notes[tag] = os.linesep.join(notes[tag]).strip()
    for issue in issues:
        tag = issue.get("check_name")
        if tag in notes:
            issue["content"] = {
                "body": notes[tag],
            }
            if match := CHECK_REGEX.search(notes[tag]):
                path = f"{PROJECT_DIR / match.groupdict()['checkpath']}"
            else:
                path = f"{PROJECT_DIR / 'debian' / 'control'}"
        else:
            path = f"{PROJECT_DIR / 'debian' / 'control'}"
        issue["location"] = {
            "path": path,
            "lines": {"begin": 1, "end": 1},
        }
    return issues


def parse(source):
    if isinstance(source, (str, os.PathLike)):
        with open(source, "r") as file:
            return parse(file)

    return parse_stream(source)


def write_json(data, target):
    if isinstance(target, (str, os.PathLike)):
        with open(target, "w") as file:
            return write_json(data, file)
    return json.dump(data, target)


# -- command-line interface

def create_parser():
    """Create an `argparse.ArgumentParser` for this tool.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "source",
        nargs="?",
        help="Path of lintian report to parse (defaults to stdin stream)",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        help="Path in which to write output JSON report.",
    )
    return parser


def main(args=None):
    parser = create_parser()
    opts = parser.parse_args(args=args)
    lint = parse(opts.source or sys.stdin)
    write_json(
        lint,
        opts.output_file or sys.stdout,
    )

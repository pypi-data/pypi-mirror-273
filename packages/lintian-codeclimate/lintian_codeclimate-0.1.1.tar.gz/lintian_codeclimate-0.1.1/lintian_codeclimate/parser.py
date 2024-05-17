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

CWD = Path(os.curdir)

CHECK_REGEX = re.compile(
    r"Check: (?P<path>debian\/[\w-]+)?(/)?(field(s)?/(?P<field>[\w-]+))?",
)
LINE_REGEX = re.compile(
    r"\A(?P<type>[A-Z]):\s+"
    r"(?P<package>[\w-]+( source)?):\s+"
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
TAG_MAP = {
    "copyright-refers-to-symlink-license": {
        "block": "license",
        "pattern": "{desc}",
    },
    "insecure-copyright-format-uri": {
        "field": "format",
    },
    "newer-standards-version": {
        "field": "standards-version",
    },
    "pypi-homepage": {
        "field": "homepage",
    },
    "python-package-missing-depends-on-python": {
        "field": "depends",
    },
    "python3-script-but-no-python3-dep": {
        "field": "depends",
    },
    "uses-debhelper-compat-file": {
        "path": "debian/compat",
    },
}
DESC_INCLUDES_LINE_NUMBER = [
    "debian-changelog-line-too-long",
    "debian-changelog-has-wrong-day-of-week",
]


def _get_location_debian(
    stream,
    default=1,
    field=None,
    pattern=None,
    block=None,
):
    """Identify a line range in a stream matching a given field or pattern
    inside a block.
    """
    start = 0
    inblock = block is None
    # if block given, but not field or pattern, match the start of the block
    if block and not (field or pattern):
        pattern = block
    for i, line in enumerate(stream, start=1):
        if line.lower().startswith(block.lower()):
            inblock = True
        if not inblock:  # keep looking
            continue
        if pattern and re.search(pattern, line, re.I):
            return (i, i)
        if field and line.lower().startswith(field):
            start = i
        elif start and not line.startswith(" "):
            break
    if start:
        return (start, i - 1)
    return (default, default)


def get_location(path, default=1, **kwargs):
    """Attempt to identify a codeclimate 'location' for a given field.
    """
    def _loc(begin, end):
        return {
            "path": str(path),
            "lines": {
                "begin": begin,
                "end": end,
            }
        }

    if not any(kwargs.values()):
        return _loc(default, default)

    path = Path(path)
    try:
        with open(path, "r") as file:
            return _loc(*_get_location_debian(file, default=default, **kwargs))
    except OSError:
        pass

    # fallback
    return _loc(default, default)


def format_issue(params):
    tag = str(params["tag"])
    nicetag = tag.capitalize().replace("-", " ")
    description = f"{nicetag} {params['desc']}"

    fingerprint = hashlib.sha1(
        "".join(map(str, params.values())).encode("utf-8"),
    ).hexdigest()

    # construct basic codeclimate issue
    return {
        "categories": ["Style"],
        "check_name": tag,
        "description": description,
        "fingerprint": fingerprint,
        "severity": SEVERITY.get(params["type"], "info"),
        "type": "issue",
        # include parsed information to assist in updated issues later
        "parsed": params,
    }


def update_issue(issue, project_dir=CWD, note=None):
    package = issue["parsed"]["package"]
    tag = issue["check_name"]

    # find the detailed note (if parsed) and use that fill out
    # the body content, and the location
    loc_params = {
        "path": "debian/control",
    }
    if package and not package.endswith(" source"):
        loc_params["block"] = f"package: {package}"
    loc_params.update(TAG_MAP.get(tag, {}))
    if loc_params.get("pattern"):
        loc_params["pattern"] = loc_params["pattern"].format(**issue["parsed"])
    if note:
        issue["content"] = {"body": note}
        if match := CHECK_REGEX.search(note):
            for key, value in match.groupdict().items():
                if value:
                    loc_params[key] = value

    if tag in DESC_INCLUDES_LINE_NUMBER:
        loc_params["default"] = int(issue["parsed"]["desc"][-2])

    # make path relative to project_dir
    loc_params["path"] = project_dir / loc_params["path"]

    # find location
    issue["location"] = get_location(**loc_params)

    # remove parsed info
    issue.pop("parsed", None)

    return issue


def parse_stream(stream, project_dir=CWD):
    issues = []
    notes = defaultdict(list)
    currentnote = []
    for line in stream:
        # parse notes
        while match := NOTES_REGEX.match(line):
            content = match.groupdict().get("content", "")
            currentnote.append(content)
            try:
                line = next(stream)
            except StopIteration:  # end of file
                break
        if note := os.linesep.join(currentnote).strip():
            latest = issues[-1]
            # record this note in the list of notes
            # (since lintian only shows each note once)
            notes[latest["check_name"]] = note
            # reset for the next note
            currentnote = []
        if match := LINE_REGEX.match(line):
            params = match.groupdict()
            issues.append(format_issue(params))

    # now that we've parsed everything, update issues based on the parsed notes
    for issue in issues:
        update_issue(issue, project_dir, notes.get(issue["check_name"]))

    return issues


def parse(source, *args, **kwargs):
    if isinstance(source, (str, os.PathLike)):
        with open(source, "r") as file:
            return parse(file, *args, **kwargs)

    return parse_stream(source, *args, **kwargs)


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
    parser.add_argument(
        "-d",
        "--project-dir",
        default=CWD,
        type=Path,
        help=(
            "Path containing source files for project "
            "(including the debian/ tree)"
        ),
    )
    return parser


def main(args=None):
    parser = create_parser()
    opts = parser.parse_args(args=args)
    lint = parse(
        opts.source or sys.stdin,
        project_dir=opts.project_dir,
    )
    write_json(
        lint,
        opts.output_file or sys.stdout,
    )

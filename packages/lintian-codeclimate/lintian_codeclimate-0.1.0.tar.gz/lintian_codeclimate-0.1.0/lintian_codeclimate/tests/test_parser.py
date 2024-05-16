# Copyright: 2024 Cardiff University
# SPDX-License-Idenfitifer: MIT

"""Tests for lintian_codeclimate.parser
"""

__author__ = "Duncan Macleod <macleoddm@cardiff.ac.uk>"

import io

import pytest

from lintian_codeclimate import parser


LINTIAN_SIMPLE = """
W: package-name: initial-upload-closes-no-bugs [usr/share/doc/package-name/changelog.Debian.gz:1]
"""  # noqa

LINTIAN_INFO = """
N:
W: package-name: initial-upload-closes-no-bugs [usr/share/doc/package-name/changelog.Debian.gz:1]
N:
N:   This package appears to be the first packaging of a new upstream software package (there is only
N:   one changelog entry and the Debian revision is 1), but it does not close any bugs. The initial
N:   upload of a new package should close the corresponding ITP bug for that package.
N:
N:   This warning can be ignored if the package is not intended for Debian or if it is a split of an
N:   existing Debian package.
N:
N:   Please refer to New packages (Section 5.1) in the Debian Developer's Reference for details.
N:
N:   Visibility: warning
N:   Show-Always: no
N:   Check: debian/changelog
N:   Renamed from: new-package-should-close-itp-bug
N:
"""  # noqa


@pytest.fixture
def lintian_stream():
    stream = io.StringIO()
    stream.write(LINTIAN_SIMPLE)
    stream.seek(0)
    return stream


@pytest.fixture
def lintian_path(tmp_path):
    name = tmp_path / "lintian.out"
    name.write_text(LINTIAN_INFO)
    return name


def test_parse_simple(lintian_stream):
    lint, = parser.parse(lintian_stream)
    assert lint["categories"] == ["Style"]
    assert lint["check_name"] == "initial-upload-closes-no-bugs"
    assert lint["severity"] == "minor"


def test_parse_info(lintian_path):
    lint, = parser.parse(lintian_path)
    assert lint["categories"] == ["Style"]
    assert lint["check_name"] == "initial-upload-closes-no-bugs"
    assert lint["content"]["body"].startswith(
        "This package appears to be the first",
    )
    assert lint["severity"] == "minor"
    assert lint["location"] == {
        "path": "debian/changelog",
        "lines": {
            "begin": 1,
            "end": 1,
        },
    }

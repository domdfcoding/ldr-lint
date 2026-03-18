#!/usr/bin/env python3
#
#  __init__.py
"""
Linter for LDraw .ldr files.
"""
#
#  Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from typing import List

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

# this package
from ldr_lint.lines import LDrawElement, lookup_line
from ldr_lint.utils import split_ws

__all__ = ["parse_file", "write_to_file"]

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2026 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"


def parse_file(filename: PathLike) -> List[LDrawElement]:
	"""
	Parse LDraw data from the given file.

	:param filename:
	"""

	lines = []
	for line in PathPlus(filename).read_lines():
		line = line.strip()
		if not line:
			continue

		type_str, raw_text = split_ws(line)
		line_type = int(type_str)

		lines.append(lookup_line(line_type).parse(raw_text))

	return lines


def write_to_file(ldraw_data: List[LDrawElement], filename: PathLike) -> None:
	"""
	Write the given LDraw lines to the given file.

	:param ldraw_data:
	:param filename:
	"""

	PathPlus(filename).write_lines(line.ldraw_string() for line in ldraw_data)

#!/usr/bin/env python3
#
#  utils.py
"""
General utilities.
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
import re
from typing import Sequence, Union

__all__ = ["format_value", "join_values", "round_float", "split_ws"]

_split_ws_re = re.compile(r"\s+")


def split_ws(string: str, maxsplit: int = 1) -> Sequence[str]:
	return _split_ws_re.split(string, maxsplit=maxsplit)


def join_values(*values: Union[str, float]):

	return ' '.join(map(format_value, values))


def round_float(value: float, atol=0.001) -> float:
	"""
	Round floats that are close to their integer equivalent.
	"""

	rounded = round(value)
	delta = abs(value - rounded)
	if delta <= atol:
		return rounded

	return value


def format_value(value: Union[str, float]) -> str:
	if isinstance(value, str):
		return value

	elif isinstance(value, int):
		return str(value)

	else:
		return str(round_float(value))

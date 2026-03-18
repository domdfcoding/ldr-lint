#!/usr/bin/env python3
#
#  lines.py
"""
LDraw line types.
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
import abc
import re
from typing import Type, Union

# 3rd party
import attrs
from typing_extensions import Self

# this package
from ldr_lint.utils import join_values, split_ws

__all__ = ["Comment", "LDrawElement", "Line", "OptionalLine", "Quad", "SubFileReference", "Triangle"]

# TODO: hexadecimal colours


@attrs.define
class LDrawElement(abc.ABC):
	raw_text: str

	@property
	@abc.abstractmethod
	def type_number(self) -> int:
		raise NotImplementedError

	@classmethod
	@abc.abstractmethod
	def parse(cls: Type[Self], raw_text: str) -> Self:
		raise NotImplementedError

	# @abc.abstractmethod
	def ldraw_string(self) -> str:
		# raise NotImplementedError
		values = [self.type_number]
		for attr in self.__attrs_attrs__[1:]:
			values.append(getattr(self, attr.name))

		return join_values(*values)


@attrs.define
class Comment(LDrawElement):

	# TODO: property for whether comment or META

	comment: str

	@property
	def type_number(self) -> int:
		return 0

	@classmethod
	def parse(cls: Type[Self], raw_text: str) -> Self:
		return cls(raw_text, raw_text)


@attrs.define
class SubFileReference(LDrawElement):

	colour: int
	x: float
	y: float
	z: float
	a: float
	b: float
	c: float
	d: float
	e: float
	f: float
	g: float
	h: float
	i: float
	file: str

	@property
	def type_number(self) -> int:
		return 1

	@classmethod
	def parse(cls: Type[Self], raw_text: str) -> Self:
		numbers_string, file = raw_text.rsplit(' ', 1)
		# file, *numbers = reversed(re.split(r"\s+", raw_text))
		# colour, x, y, z, a, b, c, d, e, f, g, h, i = reversed(map(float, numbers))
		# colour = int(colour)
		colour_str, *numbers = split_ws(numbers_string, 12)
		colour = int(colour_str)
		x, y, z, a, b, c, d, e, f, g, h, i = map(float, numbers)
		assert colour != 24
		return cls(
				raw_text,
				colour=colour,
				x=x,
				y=y,
				z=z,
				a=a,
				b=b,
				c=c,
				d=d,
				e=e,
				f=f,
				g=g,
				h=h,
				i=i,
				file=file,
				)


@attrs.define
class Line(LDrawElement):

	colour: int
	x1: float
	y1: float
	z1: float
	x2: float
	y2: float
	z2: float

	@property
	def type_number(self) -> int:
		return 2

	@classmethod
	def parse(cls: Type[Self], raw_text: str) -> Self:
		# colour, *numbers = map(float, re.split(r"\s+", raw_text))
		# colour = int(colour)
		colour_string, numbers_string = split_ws(raw_text)
		colour = int(colour_string)
		numbers = map(float, split_ws(numbers_string, 5))
		return cls(
				raw_text,
				colour,
				*numbers,
				)


@attrs.define
class Triangle(Line):

	x3: float
	y3: float
	z3: float

	@property
	def type_number(self) -> int:
		return 3

	@classmethod
	def parse(cls: Type[Self], raw_text: str) -> Self:
		# colour, *numbers = map(float, re.split(r"\s+", raw_text))
		# colour = int(colour)
		colour_string, numbers_string = split_ws(raw_text)
		colour = int(colour_string)
		numbers = map(float, split_ws(numbers_string, 8))
		return cls(
				raw_text,
				colour,
				*numbers,
				)


@attrs.define
class Quad(Triangle):

	x4: float
	y4: float
	z4: float

	@property
	def type_number(self) -> int:
		return 4

	@classmethod
	def parse(cls: Type[Self], raw_text: str) -> Self:
		# colour, *numbers = map(float, re.split(r"\s+", raw_text))
		# colour = int(colour)
		colour_string, numbers_string = split_ws(raw_text)
		colour = int(colour_string)
		numbers = map(float, split_ws(numbers_string, 11))
		return cls(
				raw_text,
				colour,
				*numbers,
				)


@attrs.define
class OptionalLine(Quad):

	@property
	def type_number(self) -> int:
		return 5


def lookup_line(line_type: Union[str, int]) -> Type[LDrawElement]:
	line_type = int(line_type)

	if line_type == 0:
		return Comment
	elif line_type == 1:
		return SubFileReference
	elif line_type == 2:
		return Line
	elif line_type == 3:
		return Triangle
	elif line_type == 4:
		return Quad
	elif line_type == 5:
		return OptionalLine
	else:
		raise NotImplementedError(line_type)

from __future__ import annotations
from decimal import Decimal
from typing import Literal, Optional, TypedDict, Union

Number = Union[Decimal, int, float]
Operator = Literal[
	"equal_to",
	"greater_than_or_equal_to",
	"greater_than",
	"less_than_or_equal_to",
	"less_than",
	"in",
]


class Action(TypedDict):
	set: Optional[Union[Number, str]]


class Condition(TypedDict):
	constant: Optional[str]
	operator: Operator
	value: Optional[Union[Number, list[Number], str, list[str]]]
	variable: Optional[str]


class Conditional(TypedDict):
	all: Optional[list[Union[Conditional, Condition]]]
	any: Optional[list[Union[Conditional, Condition]]]


class Rule(TypedDict):
	actions: dict[str, Action]
	conditions: Conditional

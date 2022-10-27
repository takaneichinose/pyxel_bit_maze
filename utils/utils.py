from enum import Enum
from dataclasses import dataclass

@dataclass
class Margin:
	top: int = 0
	bottom: int = 0
	left: int = 0
	right: int = 0

class FadeType(Enum):
	fade_in: int = 0
	fade_out: int = 1

class Direction(Enum):
	up: int = 0
	down: int = 1
	left: int = 2
	right: int = 3

import pandas as pd
from datetime import date
from dataclasses import dataclass
from typing import List


@dataclass
class Position:
    name: str
    cusip: int
    value: int
    shares: int
    date: str

empty_position = Position(None, None, 0, 0, None)


@dataclass
class DomainConfig:
    start_year: int
    cik: int


@dataclass
class PositionSummary:
    date: date
    positions: List[Position]
    dataframe: pd.DataFrame


@dataclass
class PositionChange:
    value: int
    shares: int
    value_delta: int
    shares_delta: int

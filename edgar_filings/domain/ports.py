from typing import List

import pandas as pd
from abc import ABCMeta, abstractmethod

from .types import Position


class IndexLoader(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, start_year: int):
        pass


class PositionLoader(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, filing: pd.Series) -> List[Position]:
        pass

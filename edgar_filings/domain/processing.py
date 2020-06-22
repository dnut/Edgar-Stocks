from collections import defaultdict
from dataclasses import fields, asdict
from functools import reduce
from typing import List

import pandas as pd

from .types import Position, PositionSummary, PositionChange, empty_position


def positions_to_dataframe(positions: List[Position], date: str) -> pd.DataFrame:
    df = pd.DataFrame([asdict(pos) for pos in positions],
                      columns=[field.name for field in fields(Position)])
    newdf = df.set_index('cusip', drop=True)
    newdf['date'] = date
    return newdf


def fun(history: List[PositionSummary]):
    a = pd.concat([i.dataframe for i in history])
    print(a.groupby('cusip'))


def process_history_objects(history: List[PositionSummary]):
    instruments = defaultdict(dict)
    dates = []
    cusips = {}
    for summary in history:
        dates.append(summary.date)
        for position in summary.positions:
            instruments[summary.date][position.cusip] = position
            cusips[position.cusip] = position.name
    last_date = None
    datetat = defaultdict(dict)
    datetat2 = defaultdict(dict)
    for date in dates:
        if last_date is not None:
            for cusip, name in cusips.items():
                position = instruments[date].get(cusip, empty_position)
                last_position = instruments[last_date].get(cusip, empty_position)
                change = PositionChange(position.value, position.shares,
                                        position.value - last_position.value,
                                        position.shares - last_position.shares)
                datetat[date][cusip] = change
                datetat2[f'{date}-value'][name] = change.value
                datetat2[f'{date}-shares'][name] = change.shares
                datetat2[f'{date}-value_delta'][name] = change.value_delta
                datetat2[f'{date}-shares_delta'][name] = change.shares_delta
        # instruments[summary.date].get(position.cusip, None)
        last_date = date
    return pd.DataFrame(datetat2)


def join_dataframes(history: List[PositionSummary]):
    xx = reduce(lambda x, y: x.join(y.dataframe, how='outer', rsuffix=y.date), history,
                pd.DataFrame())
    print(xx)

from dataclasses import dataclass

import pandas as pd

from .processing import process_history_objects, positions_to_dataframe, fun
from .types import DomainConfig, PositionSummary
from ..domain.ports import IndexLoader, PositionLoader


@dataclass
class Dependencies:
    config: DomainConfig
    load_index: IndexLoader
    get_positions: PositionLoader
    FORM_TYPE = '13F-HR'


def run(deps: Dependencies):
    history = _load_history(deps)
    fun(history)
    # df = process_history_objects(history)
    # df.to_csv('first-manhattan.csv')


def _load_history(deps: Dependencies):
    index = deps.load_index(deps.config.start_year)
    filtered = index.loc[index['cik'] == deps.config.cik].loc[index['form'] == deps.FORM_TYPE]
    return [_get_position_summary(deps, filing) for filing in filtered.iloc]


def _get_position_summary(deps: Dependencies, filing: pd.Series):
    positions = deps.get_positions(filing)
    df = positions_to_dataframe(positions, filing['date'])
    return PositionSummary(filing['date'], positions, df)

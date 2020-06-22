import logging
import os
import re
from dataclasses import dataclass
from typing import Union

import edgar
import pandas as pd

from .edgar_config import EdgarConfig
from edgar_filings.func import curry


@dataclass
class _IndexFile:
    path: str
    year: int
    quarter: int


@curry
def load_index(config: EdgarConfig, start_year: int):
    return _load_index(config.data_dir, config.use_cache, start_year)


def _load_index(data_dir: str, use_cache: bool, start_year: int):
    cache_path = os.path.join(data_dir, 'full_index.pkl')
    if use_cache and os.path.isfile(cache_path):
        logging.info('Loading index from cache (may not include'
                     ' filings from the desired date range)')
        return pd.read_pickle(os.path.join(data_dir, 'full_index.pkl'))
    logging.info('Downloading index')
    index = _download_index_to_pd(data_dir, start_year)
    logging.info('Storing index in cache')
    index.to_pickle(os.path.join(data_dir, 'full_index.pkl'))
    return index


def _download_index_to_pd(data_dir: str, start_year: int):
    index_files = _download_index(os.path.join(data_dir, 'index'), start_year)
    indices = [_parse_index(index_file.path) for index_file in index_files]
    return pd.concat(indices, ignore_index=True)


def _download_index(directory, start_year):
    edgar.download_index(directory, start_year, skip_all_present_except_last=True)
    return [index_file for fn in sorted(os.listdir(directory))
            if (index_file := _get_index_file(directory, fn)) is not None
            and index_file.year >= start_year]


def _get_index_file(directory: str, filename: str) -> Union[_IndexFile, None]:
    result = re.match(r'([0-9]{4})-QTR([0-4]).tsv$', filename)
    if not result:
        logging.error(f'This file has an invalid filename and will'
                      f' not be included in the index: {filename}')
        return None
    return _IndexFile(os.path.join(directory, filename),
                      int(result.groups()[0]),
                      int(result.groups()[1]))

def _parse_index(path):
    logging.info(f'Parsing {path}')
    return pd.read_csv(path, '|', names=['cik', 'company', 'form', 'date', 'file', 'file2'])

import logging
import logging.config
import os
import urllib.request
from typing import Union, Dict, List

import pandas as pd

from .edgar_config import EdgarConfig
from .parse_positions import parse_positions
from ...domain.types import Position
from edgar_filings.func import curry
from ...domain.ports import PositionLoader


# class EdgarPositionLoader(PositionLoader):
#     def __init__(self, config: EdgarConfig):
#         self._config = config
#
#     def __call__(self, filing: pd.Series) -> List[Position]:
#         return _get_positions(self._config.data_dir, self._config.base_url, self._config.xml_namespace, filing)
#

@curry
def get_positions(config: EdgarConfig, filing: pd.Series) -> PositionLoader:
    return _get_positions(config.data_dir, config.base_url, config.xml_namespace, filing)


def _get_positions(data_dir: str, base_url: str, namespace: Dict[str, str], filing: pd.Series) -> List[Position]:
    url = base_url + _txt_path_to_form_13_xml(filing['file'])
    date = filing['date']
    local_path = _download_form_13_xml(data_dir, url, date)
    if local_path is None:
        return []
    return parse_positions(local_path, namespace, date)


def _txt_path_to_form_13_xml(txt_path: str) -> str:
    return txt_path.replace('-', '').rstrip('.txt') + '/form13fInfoTable.xml'


def _download_form_13_xml(data_dir: str, url: str, name: str) -> Union[str, None]:
    local_path = os.path.join(data_dir, 'forms', name)
    if os.path.isfile(local_path):
        logging.info(f'{local_path} is already downloaded from a previous session.')
        return local_path
    logging.info(f'Downloading form13fInfoTable.xml for {name} filing')
    try:
        urllib.request.urlretrieve(url, local_path)
    except:
        logging.warning(f'Could not get form13fInfoTable.xml for {name} filing.')
        return None
    else:
        return local_path

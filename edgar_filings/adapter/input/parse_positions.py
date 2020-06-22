from typing import Dict, List
from xml.etree.ElementTree import parse, Element

from edgar_filings.domain.types import Position
from edgar_filings.func import curry


def parse_positions(file_name, ns, date) -> List[Position]:
    root = parse(file_name).getroot()
    return [_convert_info_table(_get_text(ns)(it), date) for it in root.findall('infoTable', ns)]


def _convert_info_table(get, date):
    return Position(get('nameOfIssuer'),
                    get('cusip'),
                    int(get('value')),
                    int(get('.//shrsOrPrnAmt/sshPrnamt')),
                    date)


@curry
def _get_text(namespace: Dict[str, str], node: Element, tag: str):
    it = node.findall(tag, namespace)
    if len(it) != 1:
        raise KeyError(f'Expected 1 of {tag}, but found {len(it)}: {node.text}')
    return it[0].text

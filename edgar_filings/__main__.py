from edgar_filings.domain.types import DomainConfig
from .adapter.input import get_positions
from .adapter.input import load_index, EdgarConfig
from .config import load_config
from .domain.service import Dependencies, run


def main():
    config = load_config()
    edgar_config = config[EdgarConfig]
    domain_config = config[DomainConfig]
    index_loader = load_index(edgar_config)
    info_table_loader = get_positions(edgar_config)
    run(Dependencies(domain_config, index_loader, info_table_loader))


if __name__ == '__main__':
    main()

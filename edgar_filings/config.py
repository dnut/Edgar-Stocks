import logging.config
import pandas as pd
import yaml

from .adapter.input import EdgarConfig
from .domain.types import DomainConfig


def load_config():
    set_global_state()
    with open('config.yml') as f:
        conf = yaml.safe_load(f)
    return {
        EdgarConfig: EdgarConfig(**conf['edgar']),
        DomainConfig: DomainConfig(**conf['domain'])
    }



def set_global_state():
    LOG_LEVEL = logging.DEBUG

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'f': {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}
        },
        'handlers': {
            'h': {'class': 'logging.StreamHandler',
                  'formatter': 'f',
                  'level': LOG_LEVEL}
        },
        'root': {
            'handlers': ['h'],
            'level': LOG_LEVEL,
        },
    })

    pd.options.display.width = 0

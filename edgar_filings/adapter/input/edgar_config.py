from dataclasses import dataclass
from typing import Dict


@dataclass
class EdgarConfig:
    base_url: str
    xml_namespace: Dict[str, str]
    data_dir: str
    use_cache: bool

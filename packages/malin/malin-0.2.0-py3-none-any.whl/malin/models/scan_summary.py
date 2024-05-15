from typing import List
from dataclasses import dataclass

@dataclass
class ScanSummary:
    engine: str
    message: str
    detected: bool
    malware: List[str]

    #is_file_infected: bool
    #virus_type: str
    #engine_version: str

    
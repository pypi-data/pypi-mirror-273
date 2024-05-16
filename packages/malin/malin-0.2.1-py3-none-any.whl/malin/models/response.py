from typing import List
from dataclasses import dataclass

@dataclass
class ScanSummary:
    engine: str
    message: str
    detected: bool
    malware: List[str]

@dataclass
class UpdateSummary:
    pass    
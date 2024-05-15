from dataclasses import dataclass

@dataclass
class ScanSummary:
    is_file_infected: bool
    virus_type: str
    engine_version: str
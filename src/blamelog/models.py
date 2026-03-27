from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class BlameEntry:
    commit_sha: str
    author: str
    timestamp: datetime
    line_number: int
    line_content: str

@dataclass
class FileReport:
    path: str
    entries: list[BlameEntry] = field(default_factory=list)
    # add more fields as the design evolves
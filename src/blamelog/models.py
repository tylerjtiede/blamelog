from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Commit:
    sha: str
    author: str
    email: str
    timestamp: datetime
    message: str

@dataclass
class BlameEntry:
    line_number: int
    line_content: str
    commit: Commit

@dataclass
class FileReport:
    path: str
    entries: list[BlameEntry] = field(default_factory=list)

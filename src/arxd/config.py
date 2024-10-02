from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    prefix: str
    auto_del: bool
    ignore_pattern: str
    dry_run: bool
    verbosity: bool

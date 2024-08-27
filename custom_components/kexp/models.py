"""Models for KEXP API response."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Show:
    """A partial show result."""

    name: str
    start_time: str
    hosts: list[str]
    thumbnail: str

    @property
    def title(self) -> str:
        """The display string for the particular episode of the show."""
        local_date = (
            datetime.fromisoformat(self.start_time).astimezone().strftime("%a %b %d")
        )

        return f'{local_date}: {self.name} w/ {", ".join(self.hosts)}'

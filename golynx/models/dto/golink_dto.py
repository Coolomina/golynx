from dataclasses import dataclass
from ..domain.golink import Golink


@dataclass
class GolinkDTO:
    link: str
    redirection: str

    def toGolink(self, created_by: str):
        return Golink(
            link=self.link, redirection=self.redirection, created_by=created_by
        )

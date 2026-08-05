from typing import Protocol

from domain.build.model.build import Build


class BuildServicePort(Protocol):
    def parse_pob_code(self, *, pob_code: str) -> Build: ...

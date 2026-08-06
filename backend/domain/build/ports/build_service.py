from typing import Protocol

from domain.build.model.build import Build


class BuildServicePort(Protocol):

    def get_builds(self, *, build_id: str | None = None) -> list[Build]: ...

    def save_build(self, *, build: Build) -> str: ...

    def parse_pob_code(self, *, pob_code: str, build_set_id: str) -> Build: ...

    def get_build_sets_from_pob_code(self, *, pob_code: str) -> dict[str, str]: ...

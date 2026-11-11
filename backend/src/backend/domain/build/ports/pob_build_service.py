import uuid
from typing import Protocol

from src.backend.domain.build.model.build import Build


class PoBBuildServicePort(Protocol):
    def parse_pob_code(
        self, *, pob_code: str, build_set_id: str, owner_id: uuid.UUID
    ) -> Build: ...

    def get_build_sets_from_pob_code(self, *, pob_code: str) -> dict[str, str]: ...

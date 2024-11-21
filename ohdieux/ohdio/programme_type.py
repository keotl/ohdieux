from typing import Literal, Optional

from ohdieux.model.programme import Programme

ProgrammeType = Optional[Literal["balado", "emissionpremiere", "grandesseries"]]


def infer_programme_type(programme: Programme) -> ProgrammeType:
    if "premiere/emission" in programme.programme.link:
        return "emissionpremiere"
    if "balado" in programme.programme.link:
        return "balado"
    if "grandes-series" in programme.programme.link:
        return "grandesseries"

    return None

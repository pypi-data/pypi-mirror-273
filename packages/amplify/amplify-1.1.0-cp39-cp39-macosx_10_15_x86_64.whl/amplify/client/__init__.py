from __future__ import annotations

import warnings
from typing import NoReturn

from typing_extensions import deprecated

from .. import DWaveSamplerClient as _DWaveSamplerClient
from .. import FixstarsClient as _FixstarsClient
from .. import FujitsuDA4Client
from .. import NECVA2Client
from .. import GurobiClient as _GurobiClient
from .. import LeapHybridSamplerClient as _LeapHybridSamplerClient
from .. import ToshibaSQBM2Client as _ToshibaSQBM2Client
from .._backward import _deprecation_warnings_msg, _NotImplemented, _obsolete_warnings_msg

warnings.warn(_deprecation_warnings_msg(f"{__name__} module"), DeprecationWarning, stacklevel=2)

__all__ = [
    "FixstarsClient",
    "DWaveSamplerClient",
    "LeapHybridSamplerClient",
    "FujitsuDASolverClient",
    "FujitsuDASolverExpertClient",
    "FujitsuDAPTSolverClient",
    "FujitsuDAMixedModeSolverClient",
    "FujitsuDA2SolverClient",
    "FujitsuDA2SolverExpertClient",
    "FujitsuDA2PTSolverClient",
    "FujitsuDA2MixedModeSolverClient",
    "FujitsuDA3SolverClient",
    "FujitsuDA4SolverClient",
    "ToshibaClient",
    "ToshibaSQBM2Client",
    "HitachiClient",
    "ABSClient",
    "GurobiClient",
    "QiskitClient",
    "QulacsClient",
    "NECClient",
]


class _FutureRelease:
    def __init__(self, *args, **kwargs) -> NoReturn:
        raise NotImplementedError(
            f"{type(self).__name__} (or its alternative) will be implemented in the future release."
        )


@deprecated(_deprecation_warnings_msg("amplify.client.FixstarsClient", "amplify.FixstarsClient"))
class FixstarsClient(_FixstarsClient):
    pass


@deprecated(_deprecation_warnings_msg("amplify.client.DWaveSamplerClient", "amplify.DWaveSamplerClient"))
class DWaveSamplerClient(_DWaveSamplerClient):
    pass


@deprecated(_deprecation_warnings_msg("amplify.client.LeapHybridSamplerClient", "amplify.LeapHybridSamplerClient"))
class LeapHybridSamplerClient(_LeapHybridSamplerClient):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.FujitsuDASolverClient"))
class FujitsuDASolverClient(_NotImplemented):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.FujitsuDASolverExpertClient"))
class FujitsuDASolverExpertClient(_NotImplemented):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.FujitsuDAPTSolverClient"))
class FujitsuDAPTSolverClient(_NotImplemented):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.FujitsuDAMixedModeSolverClient"))
class FujitsuDAMixedModeSolverClient(_NotImplemented):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.FujitsuDA2SolverClient"))
class FujitsuDA2SolverClient(_NotImplemented):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.FujitsuDA2SolverExpertClient"))
class FujitsuDA2SolverExpertClient(_NotImplemented):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.FujitsuDA2PTSolverClient"))
class FujitsuDA2PTSolverClient(_NotImplemented):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.FujitsuDA2MixedModeSolverClient"))
class FujitsuDA2MixedModeSolverClient(_NotImplemented):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.FujitsuDA3SolverClient"))
class FujitsuDA3SolverClient(_NotImplemented):
    pass


@deprecated(_deprecation_warnings_msg("amplify.client.FujitsuDA4SolverClient", "amplify.FujitsuDA4Client"))
class FujitsuDA4SolverClient(FujitsuDA4Client):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.ToshibaClient"))
class ToshibaClient(_NotImplemented):
    pass


@deprecated(_deprecation_warnings_msg("amplify.client.ToshibaSQBM2Client", "amplify.ToshibaSQBM2Client"))
class ToshibaSQBM2Client(_ToshibaSQBM2Client):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.HitachiClient"))
class HitachiClient(_FutureRelease):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.ABSClient"))
class ABSClient(_FutureRelease):
    pass


@deprecated(_deprecation_warnings_msg("amplify.client.GurobiClient", "amplify.GurobiClient"))
class GurobiClient(_GurobiClient):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.QiskitClient"))
class QiskitClient(_FutureRelease):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.QulacsClient"))
class QulacsClient(_FutureRelease):
    pass


@deprecated(_obsolete_warnings_msg("amplify.client.NECClient", "amplify.NECVA2Client"))
class NECClient(NECVA2Client):
    pass

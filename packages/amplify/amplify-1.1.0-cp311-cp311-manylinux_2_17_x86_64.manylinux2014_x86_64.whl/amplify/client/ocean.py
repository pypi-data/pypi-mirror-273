from __future__ import annotations

from typing_extensions import deprecated

from .. import DWaveSamplerClient as _DWaveSamplerClient
from .. import LeapHybridSamplerClient as _LeapHybridSamplerClient
from .._backward import _deprecation_warnings_msg

__all__ = [
    "DWaveSamplerClient",
    "LeapHybridSamplerClient",
]


@deprecated(_deprecation_warnings_msg("amplify.client.DWaveSamplerClient", "amplify.DWaveSamplerClient"))
class DWaveSamplerClient(_DWaveSamplerClient):
    pass


@deprecated(_deprecation_warnings_msg("amplify.client.LeapHybridSamplerClient", "amplify.LeapHybridSamplerClient"))
class LeapHybridSamplerClient(_LeapHybridSamplerClient):
    pass

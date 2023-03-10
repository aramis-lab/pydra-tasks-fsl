"""Pydra tasks for FSL.

>>> from pydra.tasks import fsl
"""

from .bet import BET
from .convert_xfm import ConvertXFM
from .flirt import FLIRT
from .fnirt import FNIRT
from .fslmerge import FSLMerge

__all__ = [
    "BET",
    "ConvertXFM",
    "FLIRT",
    "FNIRT",
    "FSLMerge",
]

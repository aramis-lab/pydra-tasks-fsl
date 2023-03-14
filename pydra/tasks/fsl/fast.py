"""
FAST
====
"""
import os
import typing as ty

import attrs

import pydra

__all__ = ["FAST"]


class FASTSpec(pydra.specs.ShellSpec):
    """Specifications for FAST."""

    # Input parameters.
    input_image: os.PathLike = attrs.field(
        metadata={
            "help_string": "input image (single-channel mode)",
            "mandatory": True,
            "argstr": "",
            "position": -1,
            "xor": {"input_images"},
        }
    )

    input_images: ty.Iterable[os.PathLike] = attrs.field(
        metadata={
            "help_string": "input images (multi-channel mode)",
            "mandatory": True,
            "argstr": "...",
            "position": -1,
            "xor": {"input_image"},
        }
    )

    num_channels: int = attrs.field(
        metadata={
            "help_string": "number of channels",
            "requires": {"input_images"},
            "readonly": True,
            "formatter": lambda input_images: f"-S {len(input_images)}",
        }
    )

    image_type: int = attrs.field(
        default=1,
        metadata={
            "help_string": "type of input image(s) (1: T1, 2: T2, 3: PD)",
            "argstr": "-t",
            "allowed_values": {1, 2, 3},
        },
    )

    # Output parameters.
    output_basename: str = attrs.field(
        metadata={
            "help_string": "basename used for output files",
            "argstr": "-o",
        },
    )

    num_classes: int = attrs.field(
        default=3,
        metadata={
            "help_string": "number of tissue-type classes",
            "argstr": "-n",
        },
    )

    save_bias_field_image: bool = attrs.field(
        metadata={
            "help_string": "save estimated bias field",
            "argstr": "-b",
        }
    )

    save_restored_input_image: bool = attrs.field(
        metadata={
            "help_string": "save estimated restored image after bias field correction",
            "argstr": "-B",
        }
    )

    save_segmentation_masks: bool = attrs.field(
        metadata={
            "help_string": "save segmentation mask for each class",
            "argstr": "-g",
        }
    )

    # Advanced parameters.
    main_mrf_parameter: float = attrs.field(
        default=0.1,
        metadata={
            "help_string": "",
            "argstr": "-H",
        },
    )

    bias_field_iterations: int = attrs.field(
        default=4,
        metadata={
            "help_string": "number of iterations for bias field removal",
            "argstr": "-I",
        },
    )

    bias_field_smoothing: float = attrs.field(
        default=20,
        metadata={
            "help_string": "bias field smoothing (FWHM in millimeters)",
            "argstr": "-l",
        },
    )

    no_partial_volume_estimation: bool = attrs.field(
        metadata={
            "help_string": "do not perform partial volume estimation",
            "argstr": "--nopve",
        }
    )


class FASTOutSpec(pydra.specs.ShellOutSpec):
    """Ouput specifications for FAST."""

    segmentation_image: str = attrs.field(
        metadata={
            "help_string": "segmentation image with each voxel assigned a class",
            "mandatory": True,
        }
    )

    segmentation_masks: ty.List[str] = attrs.field(
        metadata={
            "help_string": (
                "segmentation mask per class, with each voxel assigned a value of "
                "1 if belonging to the class 0 otherwise."
            ),
            "requires": {"save_segmentation_masks"},
        }
    )

    bias_field_image: str = attrs.field(
        metadata={
            "help_string": "estimated bias field",
            "requires": {"save_bias_field_image"},
        }
    )

    restored_input_image: str = attrs.field(
        metadata={
            "help_string": "restored input image after bias field correction",
            "requires": {"save_restored_input_image"},
        }
    )


class FAST(pydra.engine.ShellCommandTask):
    """Task definition for FAST."""

    input_spec = pydra.specs.SpecInfo(name="FASTInput", bases=(FASTSpec,))

    output_spec = pydra.specs.SpecInfo(name="FASTOuput", bases=(FASTOutSpec,))

    executable = "fast"

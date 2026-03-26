"""Shared test fixtures for gemmology-plugin tests."""

import argparse  # noqa: I001

import pytest


# Common CDL strings for testing
VALID_CDL_STRINGS = [
    "cubic[m3m]:{111}",
    "cubic[m3m]:{111}@1.0 + {100}@1.3",
    "cubic[m3m]:{110}@1.0 + {211}@0.6",
    "trigonal[-3m]:{10-10}@1.0 + {10-11}@0.8",
    "hexagonal[6/mmm]:{10-10}@1.0 + {0001}@1.5",
]

PRESET_NAMES = [
    "diamond",
    "ruby",
    "sapphire",
    "emerald",
    "quartz",
    "garnet",
    "topaz",
    "spinel",
    "tourmaline",
    "zircon",
]


@pytest.fixture
def valid_cdl_strings():
    """Return a list of valid CDL strings for parametrised tests."""
    return VALID_CDL_STRINGS


@pytest.fixture
def preset_names():
    """Return a list of common preset names for testing."""
    return PRESET_NAMES


@pytest.fixture
def tmp_output_dir(tmp_path):
    """Provide a temporary directory for test output files."""
    output_dir = tmp_path / "crystal_output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def svg_args_factory():
    """Factory fixture to create argparse Namespace objects for SVG commands."""

    def _make_args(**overrides):
        defaults = {
            "cdl": "cubic[m3m]:{111}",
            "preset": None,
            "twin": None,
            "output": None,
            "format": "svg",
            "width": 600,
            "height": 600,
            "elev": 30.0,
            "azim": -45.0,
            "no_axes": False,
            "no_grid": False,
            "info_fga": False,
        }
        defaults.update(overrides)
        return argparse.Namespace(**defaults)

    return _make_args

"""
CLI execution tests for gemmology-plugin.

Tests actual command execution using capsys for stdout/stderr capture.
These tests verify the CLI commands work correctly after bug fixes.
"""

import argparse
import json
import sys

import pytest


# =============================================================================
# Test Data
# =============================================================================

# Valid presets for testing
VALID_PRESETS = ["diamond", "ruby", "emerald", "quartz"]

# Valid CDL test cases
VALID_CDL_CASES = [
    pytest.param("cubic[m3m]:{111}", id="octahedron"),
    pytest.param("cubic[m3m]:{100}", id="cube"),
    pytest.param("cubic[m3m]:{111}@1.0 + {100}@1.3", id="truncated-octahedron"),
]


# =============================================================================
# TestListCommand - Tests for list-presets command
# =============================================================================


class TestListCommand:
    """Test list-presets command execution."""

    def test_list_categories(self, capsys):
        """List command without args shows categories."""
        from gemmology_plugin.cli import _handle_list_command

        args = argparse.Namespace(search=None, category=None)
        _handle_list_command(args)

        captured = capsys.readouterr()
        assert "Available categories:" in captured.out
        assert "cubic" in captured.out.lower()

    def test_list_by_category(self, capsys):
        """List command with category shows presets in that category."""
        from gemmology_plugin.cli import _handle_list_command

        args = argparse.Namespace(search=None, category="cubic")
        _handle_list_command(args)

        captured = capsys.readouterr()
        assert "Found" in captured.out
        assert "presets" in captured.out

    def test_list_search(self, capsys):
        """List command with search shows matching presets."""
        from gemmology_plugin.cli import _handle_list_command

        args = argparse.Namespace(search="diamond", category=None)
        _handle_list_command(args)

        captured = capsys.readouterr()
        # May find presets or not depending on search
        assert "Found" in captured.out or "No presets" in captured.out

    def test_list_no_results(self, capsys):
        """List command with no matches shows appropriate message."""
        from gemmology_plugin.cli import _handle_list_command

        args = argparse.Namespace(search="xyznonexistent123abc", category=None)
        _handle_list_command(args)

        captured = capsys.readouterr()
        assert "No presets found" in captured.out


# =============================================================================
# TestInfoCommand - Tests for info command
# =============================================================================


class TestInfoCommand:
    """Test info command execution."""

    @pytest.mark.parametrize("preset", VALID_PRESETS)
    def test_info_valid_preset(self, capsys, preset):
        """Info command with valid preset shows details."""
        from gemmology_plugin.cli import _handle_info_command

        args = argparse.Namespace(preset=preset)
        _handle_info_command(args)

        captured = capsys.readouterr()
        assert "Name:" in captured.out
        assert "CDL:" in captured.out

    def test_info_invalid_preset(self, capsys):
        """Info command with invalid preset exits with error."""
        from gemmology_plugin.cli import _handle_info_command

        args = argparse.Namespace(preset="nonexistent_xyz_abc")

        with pytest.raises(SystemExit) as exc_info:
            _handle_info_command(args)

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "Unknown preset" in captured.err

    def test_info_shows_crystal_system(self, capsys):
        """Info command shows crystal system for presets that have it."""
        from gemmology_plugin.cli import _handle_info_command

        args = argparse.Namespace(preset="diamond")
        _handle_info_command(args)

        captured = capsys.readouterr()
        assert "Crystal System:" in captured.out


# =============================================================================
# TestSvgCommand - Tests for crystal-svg command
# =============================================================================


class TestSvgCommand:
    """Test crystal-svg command execution."""

    def _make_svg_args(self, **kwargs):
        """Create argparse Namespace with default SVG arguments."""
        defaults = {
            "cdl": None,
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
        defaults.update(kwargs)
        return argparse.Namespace(**defaults)

    @pytest.mark.parametrize("cdl", VALID_CDL_CASES)
    def test_svg_from_cdl(self, capsys, cdl):
        """SVG command with CDL produces SVG output."""
        from gemmology_plugin.cli import _handle_svg_command

        args = self._make_svg_args(cdl=cdl)
        _handle_svg_command(args)

        captured = capsys.readouterr()
        assert "</svg>" in captured.out

    @pytest.mark.parametrize("preset", VALID_PRESETS)
    def test_svg_from_preset(self, capsys, preset):
        """SVG command with preset produces SVG output."""
        from gemmology_plugin.cli import _handle_svg_command

        args = self._make_svg_args(preset=preset)
        _handle_svg_command(args)

        captured = capsys.readouterr()
        assert "</svg>" in captured.out

    def test_svg_to_file(self, capsys, tmp_path):
        """SVG command with output file writes to file."""
        from gemmology_plugin.cli import _handle_svg_command

        output_file = tmp_path / "test.svg"
        args = self._make_svg_args(cdl="cubic[m3m]:{111}", output=str(output_file))
        _handle_svg_command(args)

        assert output_file.exists()
        content = output_file.read_text()
        assert "</svg>" in content

        captured = capsys.readouterr()
        assert "Written to" in captured.out

    def test_svg_invalid_preset(self, capsys):
        """SVG command with invalid preset exits with error."""
        from gemmology_plugin.cli import _handle_svg_command

        args = self._make_svg_args(preset="nonexistent_xyz_abc")

        with pytest.raises(SystemExit) as exc_info:
            _handle_svg_command(args)

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err


# =============================================================================
# TestStlOutput - Tests for STL output format
# =============================================================================


class TestStlOutput:
    """Test STL output format."""

    def test_stl_binary_output(self, tmp_path):
        """STL format produces binary output to file."""
        from gemmology_plugin.cli import _handle_svg_command

        output_file = tmp_path / "test.stl"
        args = argparse.Namespace(
            cdl="cubic[m3m]:{111}",
            preset=None,
            twin=None,
            output=str(output_file),
            format="stl",
            width=600,
            height=600,
            elev=30.0,
            azim=-45.0,
            no_axes=False,
            no_grid=False,
            info_fga=False,
        )
        _handle_svg_command(args)

        assert output_file.exists()
        content = output_file.read_bytes()
        # Binary STL: 80-byte header + 4-byte facet count + facet data
        assert len(content) >= 84


# =============================================================================
# TestGltfOutput - Tests for glTF output format
# =============================================================================


class TestGltfOutput:
    """Test glTF output format."""

    def test_gltf_output(self, tmp_path):
        """glTF format produces valid JSON output to file."""
        from gemmology_plugin.cli import _handle_svg_command

        output_file = tmp_path / "test.gltf"
        args = argparse.Namespace(
            cdl="cubic[m3m]:{111}",
            preset=None,
            twin=None,
            output=str(output_file),
            format="gltf",
            width=600,
            height=600,
            elev=30.0,
            azim=-45.0,
            no_axes=False,
            no_grid=False,
            info_fga=False,
        )
        _handle_svg_command(args)

        assert output_file.exists()
        content = json.loads(output_file.read_text())
        assert "asset" in content
        assert "meshes" in content


# =============================================================================
# TestErrorHandling - Tests for error cases
# =============================================================================


class TestErrorHandling:
    """Test error handling paths."""

    def test_invalid_cdl_error(self, capsys):
        """Invalid CDL produces error message."""
        from gemmology_plugin.cli import _handle_svg_command

        args = argparse.Namespace(
            cdl="invalid[xxx]:{999}",
            preset=None,
            twin=None,
            output=None,
            format="svg",
            width=600,
            height=600,
            elev=30.0,
            azim=-45.0,
            no_axes=False,
            no_grid=False,
            info_fga=False,
        )

        with pytest.raises(SystemExit) as exc_info:
            _handle_svg_command(args)

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error:" in captured.err


# =============================================================================
# TestMainEntryPoint - Tests for main() function
# =============================================================================


class TestMainEntryPoint:
    """Test main() entry point."""

    def test_version_command(self, capsys):
        """Main with version command shows version."""
        from gemmology_plugin import __version__
        from gemmology_plugin.cli import main

        old_argv = sys.argv
        try:
            sys.argv = ["gemmology", "version"]
            main()
            captured = capsys.readouterr()
            assert __version__ in captured.out
        finally:
            sys.argv = old_argv

    def test_no_command_exits_with_error(self, capsys):
        """Main with no command exits with code 1."""
        from gemmology_plugin.cli import main

        old_argv = sys.argv
        try:
            sys.argv = ["gemmology"]
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
        finally:
            sys.argv = old_argv


# =============================================================================
# TestCrystalSvgEntryPoint - Tests for crystal-svg entry point
# =============================================================================


class TestCrystalSvgEntryPoint:
    """Test crystal_svg() entry point function."""

    def test_crystal_svg_entry_point(self, capsys, monkeypatch):
        """crystal_svg entry point works with CDL argument."""
        from gemmology_plugin.cli import crystal_svg

        monkeypatch.setattr(
            sys, "argv", ["crystal-svg", "--cdl", "cubic[m3m]:{111}"]
        )
        crystal_svg()

        captured = capsys.readouterr()
        assert "</svg>" in captured.out

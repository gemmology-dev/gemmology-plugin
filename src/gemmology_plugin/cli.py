"""
Gemmology Plugin CLI - Command-line interface for crystal visualization.

This module provides the command-line interface for the gemmology plugin,
wrapping functionality from the component packages.
"""

import argparse
import sys


def create_argument_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="gemmology",
        description="Gemmology plugin for crystal visualization and gemstone expertise",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # crystal-svg command
    svg_parser = subparsers.add_parser(
        "crystal-svg",
        aliases=["svg"],
        help="Generate SVG visualization of crystal structure",
    )
    _add_svg_arguments(svg_parser)

    # list-presets command
    list_parser = subparsers.add_parser(
        "list-presets",
        aliases=["list"],
        help="List available mineral presets",
    )
    list_parser.add_argument(
        "--category",
        "-c",
        help="Filter by category",
    )
    list_parser.add_argument(
        "--search",
        "-s",
        help="Search for presets by name",
    )
    list_parser.add_argument(
        "--origin",
        choices=["natural", "synthetic", "simulant"],
        help="Filter presets by origin (natural, synthetic, simulant)",
    )

    # info command
    info_parser = subparsers.add_parser(
        "info",
        help="Show information about a preset",
    )
    info_parser.add_argument(
        "preset",
        help="Preset name (e.g., diamond, ruby, emerald)",
    )

    # version command
    subparsers.add_parser("version", help="Show version information")

    return parser


def _add_svg_arguments(parser: argparse.ArgumentParser) -> None:
    """Add SVG-related arguments to a parser."""
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--cdl",
        help="Crystal Description Language string",
    )
    group.add_argument(
        "--preset",
        "-p",
        help="Use a mineral preset (e.g., diamond, ruby)",
    )
    group.add_argument(
        "--twin",
        "-t",
        help="Twin law name (e.g., spinel, japan)",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["svg", "png", "stl", "gltf"],
        default="svg",
        help="Output format (default: svg)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=600,
        help="Output width in pixels (default: 600)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=600,
        help="Output height in pixels (default: 600)",
    )
    parser.add_argument(
        "--elev",
        type=float,
        default=30.0,
        help="View elevation angle in degrees (default: 30)",
    )
    parser.add_argument(
        "--azim",
        type=float,
        default=-45.0,
        help="View azimuth angle in degrees (default: -45)",
    )
    parser.add_argument(
        "--no-axes",
        action="store_true",
        help="Hide crystallographic axes",
    )
    parser.add_argument(
        "--no-grid",
        action="store_true",
        help="Hide background grid",
    )
    parser.add_argument(
        "--info-fga",
        action="store_true",
        help="Include FGA info panel",
    )


def crystal_svg() -> None:
    """Entry point for crystal-svg command."""
    parser = argparse.ArgumentParser(
        prog="crystal-svg",
        description="Generate SVG visualization of crystal structure",
    )
    _add_svg_arguments(parser)
    args = parser.parse_args()
    _handle_svg_command(args)


def _handle_svg_command(args: argparse.Namespace) -> None:
    """Handle the crystal-svg command."""
    import os
    import tempfile

    from cdl_parser import parse_cdl
    from crystal_geometry import cdl_to_geometry
    from crystal_renderer import generate_cdl_svg, geometry_to_gltf, geometry_to_stl
    from mineral_database import get_preset

    # Determine CDL string
    cdl: str | None = None
    info_properties = None

    if args.cdl:
        cdl = args.cdl
    elif args.preset:
        preset = get_preset(args.preset)
        if preset is None:
            print(f"Error: Unknown preset '{args.preset}'", file=sys.stderr)
            sys.exit(1)
        cdl = preset["cdl"]
        # Build info properties from preset if FGA info panel requested
        if args.info_fga:
            info_properties = {
                "name": preset.get("name"),
                "chemistry": preset.get("chemistry"),
                "system": preset.get("system"),
                "hardness": preset.get("hardness"),
                "ri": preset.get("ri"),
                "sg": preset.get("sg"),
            }
            # Remove None values
            info_properties = {k: v for k, v in info_properties.items() if v is not None}
    elif args.twin:
        # For twins, construct the CDL with twin modifier
        cdl = f"cubic[m3m]:octahedron|twin({args.twin})"

    if cdl is None:
        print("Error: No CDL string provided", file=sys.stderr)
        sys.exit(1)

    try:
        if args.format == "svg":
            # generate_cdl_svg writes to file and returns Path
            # Use temp file if output not specified
            if args.output:
                output_path = args.output
            else:
                fd, output_path = tempfile.mkstemp(suffix=".svg")
                os.close(fd)

            # Convert pixel dimensions to figsize in inches (at 100 dpi)
            figsize = (args.width / 100, args.height / 100)

            generate_cdl_svg(
                cdl,
                output_path,
                show_axes=not args.no_axes,
                elev=args.elev,
                azim=args.azim,
                show_grid=not args.no_grid,
                info_properties=info_properties,
                figsize=figsize,
            )

            if args.output:
                print(f"Written to {args.output}")
            else:
                # Read and print temp file, then clean up
                with open(output_path) as f:
                    print(f.read())
                os.unlink(output_path)

        elif args.format in ("stl", "gltf"):
            import json

            desc = parse_cdl(cdl)
            geom = cdl_to_geometry(desc)
            if args.format == "stl":
                output = geometry_to_stl(geom.vertices, geom.faces, binary=True)
                is_binary = True
            else:
                gltf_dict = geometry_to_gltf(geom.vertices, geom.faces)
                output = json.dumps(gltf_dict, indent=2)
                is_binary = False

            # Output binary/text data
            if args.output:
                mode = "wb" if is_binary else "w"
                with open(args.output, mode) as f:
                    f.write(output)
                print(f"Written to {args.output}")
            else:
                if is_binary:
                    sys.stdout.buffer.write(output)
                else:
                    print(output)
        else:
            print(f"Error: Unsupported format '{args.format}'", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _handle_list_command(args: argparse.Namespace) -> None:
    """Handle the list-presets command."""
    from mineral_database import (
        get_preset,
        list_by_origin,
        list_preset_categories,
        list_presets,
        search_presets,
    )

    if args.search:
        preset_names = search_presets(args.search)
    elif args.category:
        preset_names = list_presets(args.category)
    elif args.origin:
        preset_names = list_by_origin(args.origin)
    else:
        # List all categories and counts
        categories = list_preset_categories()
        print("Available categories:")
        for cat in sorted(categories):
            presets_in_cat = list_presets(cat)
            print(f"  {cat}: {len(presets_in_cat)} presets")
        return

    if not preset_names:
        print("No presets found.")
        return

    print(f"Found {len(preset_names)} presets:")
    for name in sorted(preset_names):
        preset = get_preset(name)
        if preset:
            system = preset.get("system", "unknown")
            display_name = preset.get("name", name)
            origin = preset.get("origin", "natural")
            origin_badge = ""
            if origin == "synthetic":
                origin_badge = " [synthetic]"
            elif origin == "simulant":
                origin_badge = " [simulant]"
            print(f"  {display_name:20} ({system}){origin_badge}")


def _handle_info_command(args: argparse.Namespace) -> None:
    """Handle the info command."""
    from mineral_database import get_family, get_preset

    preset = get_preset(args.preset)
    if preset is None:
        print(f"Error: Unknown preset '{args.preset}'", file=sys.stderr)
        sys.exit(1)

    print(f"Name: {preset.get('name')}")
    print(f"CDL: {preset.get('cdl')}")
    if preset.get("system"):
        print(f"Crystal System: {preset.get('system')}")
    if preset.get("chemistry"):
        print(f"Chemistry: {preset.get('chemistry')}")
    if preset.get("hardness"):
        print(f"Hardness: {preset.get('hardness')}")
    if preset.get("sg"):
        print(f"Specific Gravity: {preset.get('sg')}")
    if preset.get("ri"):
        print(f"Refractive Index: {preset.get('ri')}")
    if preset.get("birefringence"):
        print(f"Birefringence: {preset.get('birefringence')}")
    if preset.get("optical_character"):
        print(f"Optical Character: {preset.get('optical_character')}")

    # Origin and synthetic/simulant fields
    origin = preset.get("origin")
    if origin and origin != "natural":
        print(f"Origin: {origin}")
    if preset.get("growth_method"):
        print(f"Growth Method: {preset.get('growth_method')}")
    if preset.get("natural_counterpart_id"):
        print(f"Natural Counterpart: {preset.get('natural_counterpart_id')}")
    if preset.get("manufacturer"):
        print(f"Manufacturer: {preset.get('manufacturer')}")
    if preset.get("year_first_produced"):
        print(f"Year First Produced: {preset.get('year_first_produced')}")
    if preset.get("diagnostic_synthetic_features"):
        features = preset["diagnostic_synthetic_features"]
        if isinstance(features, list):
            print("Diagnostic Synthetic Features:")
            for feature in features:
                print(f"  - {feature}")
        else:
            print(f"Diagnostic Synthetic Features: {features}")

    # Family-level information
    family = get_family(args.preset)
    if family:
        print(f"\nFamily: {family.get('name', '')}")
        if family.get("description"):
            print(f"Family Description: {family.get('description')}")


def main() -> None:
    """Main entry point for the gemmology CLI."""
    parser = create_argument_parser()
    args = parser.parse_args()

    if args.command in ("crystal-svg", "svg"):
        _handle_svg_command(args)
    elif args.command in ("list-presets", "list"):
        _handle_list_command(args)
    elif args.command == "info":
        _handle_info_command(args)
    elif args.command == "version":
        from gemmology_plugin import __version__

        print(f"gemmology-plugin {__version__}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

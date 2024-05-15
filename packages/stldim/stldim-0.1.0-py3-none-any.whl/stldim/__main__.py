#!/usr/bin/env python3
"""
    stldim - Get dimensions of an STL file
    Usage:
        stldim.py [options] <stlfile>

    Options:
        -h --help       Show this screen.
        --version       Show version.
        --name=<name>   Name of the object [defaults to the filename with non alpha-numeric characters replaced with underscores].
"""

import argparse
import os
import sys

import stldim.version as version
from stldim import get_varname, get_stl_dimensions

def main():
    parser = argparse.ArgumentParser(prog="stldim",
                                     description="Get dimensions of an STL file")

    parser.add_argument("stlfile", type=str, help="Path to the STL file")
    parser.add_argument("--version", action="version",
                        help="Show version", version=version.__str__)
    parser.add_argument("--name", type=str, default=None,
                        help="Name of the object (defaults to filename with special characters replaced by underscores")

    args = parser.parse_args()

    if not os.path.exists(args.stlfile):
        sys.exit(f'ERROR: file args.stlfile was not found!')
    varname = get_varname(args.stlfile, args.name)

    stl_dimensions = get_stl_dimensions(args.stlfile)


# the logic is easy from there

    print("// File:", args.stlfile)
    lst = ['obj =("', args.stlfile, '");']
    obj = ['\t\timport("', args.stlfile, '");']

    print("// X size:", stl_dimensions['xsize'])
    print(f"{varname}_xsize = {stl_dimensions['xsize']};")
    print("// Y size:", stl_dimensions['ysize'])
    print(f"{varname}_ysize = {stl_dimensions['ysize']};")
    print("// Z size:", stl_dimensions['zsize'])
    print(f"{varname}_zsize = {stl_dimensions['zsize']};")
    print("// X position:", stl_dimensions['minx'])
    print(f"{varname}_xposition = {stl_dimensions['minx']};")
    print("// Y position:", stl_dimensions['miny'])
    print(f"{varname}_yposition = {stl_dimensions['miny']};")
    print("// Z position:", stl_dimensions['minz'])
    print(f"{varname}_zposition = {stl_dimensions['minz']};")

    # --------------------
    print("NE=1; NW=2; SW=3; SE=4; CTR=5; CTRXY=6;")

    print(f"module {varname}_obj2origin (where) {{")
    print("\tif (where == NE) {")
    print(f"\t\t{varname}_objNE ();")
    print("\t}")
    print("")

    print("\tif (where == NW) {")
    print("\t\ttranslate([", -stl_dimensions['xsize'], ",", 0, ",", 0, "])")
    print(f"\t\t{varname}_objNE ();")
    print("\t}")
    print("")

    print("\tif (where == SW) {")
    print("\t\ttranslate([", -stl_dimensions['xsize'],
          ",", -stl_dimensions['ysize'], ",", 0, "])")
    print(f"\t\t{varname}_objNE ();")
    print("\t}")
    print("")

    print("\tif (where == SE) {")
    print(
        "\t\ttranslate([", 0, ",", -stl_dimensions['ysize'], ",", 0, ",", "])")
    print(f"\t\t{varname}_objNE ();")
    print("\t}")
    print("")

    print("\tif (where == CTR) {")
    print("\ttranslate([", -stl_dimensions['midx'], ",", -
          stl_dimensions['midy'], ",", -stl_dimensions['midz'], "])")
    print(f"\t\t{varname}_objNE ();")
    print("\t}")
    print("")

    print("\tif (where == CTRXY) {")
    print("\ttranslate([", -stl_dimensions['midx'],
          ",", -stl_dimensions['midy'], ",", 0, "])")
    print(f"\t\t{varname}_objNE ();")
    print("\t}")
    print("}")
    print("")

    print(f"module {varname}_objNE () {{")
    print("\ttranslate([", -stl_dimensions['minx'], ",", -
          stl_dimensions['miny'], ",", -stl_dimensions['minz'], "])")
    print("".join(obj))
    print("}")


if __name__ == '__main__':
    main()

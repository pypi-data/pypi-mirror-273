# stldim

A tool for mesuring the dimensions of an STL file.

## Description

This is a python library which measures the dimmensions and coordinates of an STL file. It can be used as a library where you can use the measurements in your code, or it can be used as a command line tool which prints out the measurements as OpenSCAD code, so you can use it as a library in your OpenSCAD designs.

## Acknowledgements

It is an enhanced version of <https://github.com/lar3ry/OpenSCAD---Move-STL-to-origin> which in turn is based on `stldim.py`, by Jamie Bainbridge. Their version can be found at:
  <https://www.reddit.com/r/3Dprinting/comments/7ehlfc/python_script_to_find_stl_dimensions/>

## CLI

If called from the command line, a library is printed to the terminal which can be used in OpenSCAD.

The script will create an OpenSCAD library which will allow you to place an STL file to 6 different positions in relation to the origin:

CTR put's the center of the STL to the origin of the OpenSCAD coordinate system.
CTRXY puts the center of the STL to the origin of the OpenSCAD coordinate system, but only in the XY plane.
NE, NW, SW, SE put the STL to the origin of the OpenSCAD coordinate system, but only in the XY plane, and in the direction of the compass point.

In the generated library, a module `<name>_obj2origin()` is created which you can use to place the object.
Name is derived from the basename of the STL file, with all non-alphanumeric characters replaced by underscores (e.g. `My Object.stl` becomes `My_Object_stl`).

The script will also define variables for the x-, y-, and z-size and -position of the object which can be used for other calculations in your code.

### Usage

```shell
stldim 3DBenchy.stl --name=object >benchy.scad
```

This will create an OpenSCAD library file `benchy.scad` which you can include in your OpenSCAD code:

```OpenSCAD
include<benchy.scad>; // Include the generated library

bin_obj2origin(NE); // put the object in the North-East corner of the XY plane
```

Other options for obj2origin() are:

- `CTR` - Center the object on the origin
- `CTRXY` - Center the object on the origin, but only in the XY plane
- `NE` - Put the object in the North-East corner of the XY plane
- `NW` - Put the object in the North-West corner of the XY plane
- `SW` - Put the object in the South-West corner of the XY plane
- `SE` - Put the object in the South-East corner of the XY plane

## Library

You can also import stldim in your python project and use the provided methods to get the dimensions of an STL file.

Be aware though, that this library is in a very early stage of development and the API might change significantly in the future.


## Prerequisites

You will have to install `stl`, `numpy`, and `numpy-stl` Python packages in case you don't have those already.

```shell
pip3 install stl
pip3 install numpy
pip3 install numpy-stl
```

## Installation

```shell
pip3 install stldim
```

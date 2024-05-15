# stldim

Makes a library tailored to an existing STL file. Move it to the origin in OpenSCAD.

It is an enhanced version of <https://github.com/lar3ry/OpenSCAD---Move-STL-to-origin> which in turn is based on `stldim.py`, by Jamie Bainbridge. Their version can be found at:
  <https://www.reddit.com/r/3Dprinting/comments/7ehlfc/python_script_to_find_stl_dimensions/>

The script will create an OpenSCAD library which will allow you to place an STL file to 6 different positions in relation to the origin:

CTR put's the center of the STL to the origin of the OpenSCAD coordinate system.
CTRXY puts the center of the STL to the origin of the OpenSCAD coordinate system, but only in the XY plane.
NE, NW, SW, SE put the STL to the origin of the OpenSCAD coordinate system, but only in the XY plane, and in the direction of the compass point.

In the generated library, a module `<name>_obj2origin()` is created which you can use to place the object.
Name is derived from the basename of the STL file, with all non-alphanumeric characters replaced by underscores (e.g. `My Object.stl` becomes `My_Object_stl`).

The script will also define variables for the x-, y-, and z-size and -position of the object which can be used for other calculations in your code.

## Prerequisites

You will have to install `stl`, `numpy`, and `numpy-stl` Python packages in case you don't have those already.

```shell
pip3 install stl
pip3 install numpy
pip3 install numpy-stl
```

## Usage

Place the `stldim.py` file where you keep your Python executable scripts. Its usage is like this:

```shell
stldim [stl file]                # prints the result in stdout
stldim [stl file] > [scad file]  # writes the result into a .scad file
```

On a command line, CD to the directory containing the STL you wish to move, and run the script, giving it the name of the STL file as an argument. If you wish, you can redirect the output to a library file as well (see the example below).

## Acknowledgements

This project is based on <https://github.com/lar3ry/OpenSCAD---Move-STL-to-origin> and enhances it with additional features.

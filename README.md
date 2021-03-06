README
======

This file provides basic explanations regarding the PyFauxFur project.
It contains a simple descriptions of its features, system requirements,
installation and usage instructions. For more information, please refer to the
report, available in the report/ folder.

FEATURES
--------

PyFauxFur implements the Turing Morphogenesis model [Turing52], as
described by Turk [Turk91]. It features real time display of the simulation
results, and the calculations are done in a separate thread. It uses Qt for
its graphical user interface, OpenGL for the image rendering, and Blitz++
(via SciPy) for its numerical calculations.

REQUIREMENTS
------------

This program has been tested with python 2.5. It requires PyQt4, NumPy,
SciPy and PyOpenGL >= 3.0. It has been tested with PyQt4 4.4.4, NumPy 1.2.1,
SciPy 0.7.0 and PyOpenGL 3.0.0.

	apt-get install python-qt4 python-numpy python-scipy \
	 python-opengl python-qt4-gl python-dev

INSTALLATION
------------

Apart from the dependencies, no installation should be necessary.

If Ui_MainWindow.py has not been generated, you can do so by running

	./gen.sh

COMMON PROBLEMS
---------------

	ImportError: No module named Ui_MainWindow

Please refer to the INSTALLATION section : you need to generate the necessary
UI files for the Qt-based interface to be correctly displayed. These files may
be generated automatically in a future release.

USAGE
-----

Simply run

	python PyFauxFur.py

For additional usage information, you can run

	python PyFauxFur.py --help

You can also generate a batch of sample images after 1000 iterations with

	./test_images.sh

SOME PATTERNS
-------------

The default parameters (which you can see with the --help option) are a good
starting point for interesting textures. Running the program for 1000 or so
iterations with parameters within [0.5, 2] * default values will produce
interesting results. Changing ß_i is not recommended.

To get stripes, use D_a > 10 * D_b, the width of stripes will decrease when
D_s increases. To obtain dots, use 5 * D_b > D_a > 3 * D_b. To obtain blobs
and lines, use D_a >> D_b. The spots will be less intense as the number of
iterations and D_s increase.

REFERENCES
----------

[Turk1991] Greg Turk, "Generating Textures on Arbitrary Surfaces Using
Reaction-Diffusion," Computer Graphics, Vol. 25, No. 4, (SIGGRAPH 91), July
1991, pp. 289-298.

[Turing1952] Alan Turing, "The Chemical Basis of Morphogenesis," Philosophical
Transactions of the Royal Society B, Vol. 237, pp. 37-72 (August 14, 1952).

CODE INSPIRATION
----------------

Reaction-Diffusion Textures, Orion Sky Lawlor,
http://charm.cs.uiuc.edu/users/olawlor/projects/2003/rd/

Turing's Reaction-Diffusion Model of Morphogenesis, Christopher G. Jennings,
http://www.sfu.ca/~cjenning/toybox/turingmorph/

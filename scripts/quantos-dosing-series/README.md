#Quantos dosing scripts

This directory contains scripts for generating a set of input masses for a given binary mixture and number of mole fractions.

Currently, the script is run with:
`python binary_mixture.py input.yaml`

It then writes out a file containing the list of mass pairs to interpolate between 100% compound 1 and 100% compound 2. The output filename is given in the yaml.

An example yaml is provided in this directory and can be used as a template. The output filename is optional, and the script will print the name of the file
containing the output after running.  

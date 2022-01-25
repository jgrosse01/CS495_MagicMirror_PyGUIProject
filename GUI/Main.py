"""
Created on 22 January 2022
Name: Main.py
Author: Jake Grosse
Description: A Python file which initializes and runs the GUI Mirror. Very simple.
"""

# import the mirror class so we can make it
from Mirror import Mirror

# here we initialize and run the mirror (in the main method... waow...)
if __name__ == '__main__':
    # didn't need to consult anything for this one line
    # it just makes a mirror with the title as passed by parameter
    # please note the empty spaces on the sides of the camera image are a design choice
    mirror = Mirror("Mirror mirror on the wall...")

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 12:53:24 2019

@author: Xavier Tanguay
"""



# =============================================================================
#                   Generating the basics of the project 
# =============================================================================



# Setting up the project file :

def bw2_launch(name) :
    bw.projects.set_current(name) 
    bw.projects.current

# Getting the biosphere matrix :
    
    bw.bw2setup()  # This will take some time 
               # This will also generate the LCIA methods
    biosphere = bw.Database('biosphere3') # This will generate a variable that will hold the database itself.

    print('The biosphere database is a square matrix of',len(biosphere),'datasets.')
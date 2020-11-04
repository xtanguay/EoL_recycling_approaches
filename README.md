# EoL_recycling_approaches

This repository provides access to the inventory (both in table formats and Brightway2 compatible) used in the modelling of wood cascades and the scripts to perform the LCA calculations (from setting up the biosphere, loading the background databases (ecoinvent 3.5), loading the foreground and applying the equations presented in the paper).

Detailed content of the repository : 

00_Main_file script : Contains the project, performs LCA calculations and calls imbedded functions from files 01 to 04. Make sure to fix file paths as requested in the file.

01_Initializing : Handles project creation/assignment and biosphere database creation.

02_Ecoinvent_import : Imports ecoinvent to the project (if not already done). Attention should be paid to file paths.

03_Inventory_converter : This file was developed by Massimo Pizzol in the Brightway2 for beginners (see https://github.com/massimopizzol/B4B) and allows to convert excel spreadsheets to python dictionaries, which are later converted to a database. 

04_Cascade_parameterization : Parameterizes the inventories in accordance to equations shown in the paper and values from the supplementary information.

Inventory tables : Provides access, in simplified tables, to the processes modelled and quantities for the cascade system and virgin materials (assuming Q = 1 and d =1). 

Inventory_model/Modified attributional datasets/Modified consequential datasets : The foreground and the modified background datasets are available in this ready to use format for the python script. 

Notes :

The content of this repository isn't guaranteed to work right-away. The scripts and spreadsheets presented are edited versions of the case study. Some scripts require to be modified by the user to enter his/her own file path. The ecoinvent 3.5 databases (cut-off/apos/consequential) are NOT included. It is the user's responsibility to check that everything works correctly. A working version of Brightway2 (or any of the other libraries called in the scripts) are required. On a final note, I am not a professional programmer. The scripts presented could be made more "pythonic" and better organized, but it is left to potential users to optimize their own scripts.




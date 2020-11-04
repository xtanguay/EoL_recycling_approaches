# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 12:12:24 2019

@author: Xavier Tanguay
"""

#%% 


# =============================================================================
#                """Files to be used along with this script : """
# =============================================================================

 
exec(open('01_Initializing.py').read())
exec(open('02_Ecoinvent_import.py').read())
exec(open('03_Inventory_converter.py').read())
exec(open('04_Cascade_parameterization.py').read())

# Note : 
        # To have the files working, the sub-files have to be executed 1st. To do so, launch each sub-file 
        # and run them seperately. This will activate the functions within each of them. Then, run this cell
        # to activate them. 


#%%

# =============================================================================
#                       """Setting up the infrastructure : """
# =============================================================================

        
import brightway2 as bw
import pandas as pd
import numpy as np
import seaborn as sns
from brightway2 import * 
from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter, Group  
from bw2analyzer import ContributionAnalysis
from bw2data import Database, get_activity
from bw2calc import GraphTraversal

#%%

# =============================================================================
#                """ Launching the basic imports of brightway2 : """
# =============================================================================

project_name = 'Wood_cascade'         # Will set up the project under this name.

bw2_launch(project_name)                # Obtained from the Initializing file - will generate LCIA & biosphere matrix.
#print(bw.databases)                   # Used to seek how many databases are in the actual project already.  

#%%

# =============================================================================
#                 """ Importing the ecoinvent databases : """
# =============================================================================

# Databases names : 

eco_35_CO = 'ecoinvent 3_5 cut_off'              # Name of the 1st ecoinvent database desired.
eco_35_con = 'ecoinvent 3_5 consequential'       # Name of the 2nd ecoinvent database desired.
eco_35_APOS = 'ecoinvent 3_5 apos'               # Name of the 3rd ecoinvent database desired.


# Getting the technosphere matrix (ecoinvent) : 
ei_CO_35 = get_ei_db(eco_35_CO)                    # Cut-off 3_5 database
ei_con_35 = get_ei_db(eco_35_con)                  # Consquential 3_5 database
ei_APOS_35 = get_ei_db(eco_35_APOS)                # Allocation at point of substitution 3_5 database


# The lenght is printed in the end to validate if the import worked correctly. Usual ecoinvent databases hold about 15k datasets (roughly). 
print('')

#%%
# ==================================================================================
# """ Generating the modified datasets and exchanges - consequential datasets : """
# ==================================================================================

# Enter the name of the new database :  

Db_name = "Modified consequential datasets"

        # Note : This has to be the same name as the one in the excel spreadsheet. 

"""
# =============================================================================
#       Make sure to use the correct filepath to your own CSV file here :
# =============================================================================
"""

fpCSV = r'C:\Users\User\Brightway2\Spyder files\Modified consequential datasets.csv' 
mydb = pd.read_csv(fpCSV, header = 0, sep = ",") # if using csv file
mydb['Exchange uncertainty type'] = mydb['Exchange uncertainty type'].fillna(0).astype(int)


""""
# =============================================================================
# 
# =============================================================================
""""


bw2_db = lci_to_bw2(mydb)   # The excel file is now in the form of a dictionnary.
#print(bw2_db)              # To help visualize the dictionnary.
print(bw.databases)


if Db_name in bw.databases :
    del bw.databases[Db_name] 
print(bw.databases)

# Creating a new database : 

t_db = Database(Db_name)



# Acquiring the data from the dictionnary : 

t_db.write(bw2_db)

# Important note :
                # Should the program return "Database is locked" as an error at this point, restarting the kernel and running everything
                # at once should fix this. 
                # If an error "list index out of range" occurs, one explanation may be there is still data in some of the excel cells,
                # for instance a space " ". Use "print(mydb)" as a command to see if the excel file is longuer than expected. 

                # Sometimes, errors spurr out of miss-naming processes (creating twice the name, but 2 codes or vice-versa)
                # This will throw errors such as "Technosphere matrix isn't square" and will prevent LCIA calculations.
                # The message will quote a number of rows and lines being uneven. To find the processes :
"""               
                for ds in Database("Consequential inventory"):
                    for prod_exc in ds.production():
                        if ((prod_exc['input'][1]) != ds['code']):
                            print((ds['name'],ds['code'],prod_exc['input']))
                            
"""      
print('')

#%%
# =======================================================================================
#       """ Generating the modified datasets and exchanges - attributional datasets : """
# ========================================================================================

# Enter the name of the new database :  

Db_name = "Modified dataset"

        # Note : This has to be the same name as the one in the excel spreadsheet. 

"""
# =============================================================================
#       Make sure to use the correct filepath to your own CSV file here :
# =============================================================================
"""

fpCSV = r'C:\Users\User\Brightway2\Spyder files\Modified attributional datasets.csv' 
mydb = pd.read_csv(fpCSV, header = 0, sep = ",") # if using csv file
mydb['Exchange uncertainty type'] = mydb['Exchange uncertainty type'].fillna(0).astype(int)

"""
# =============================================================================
# 
# =============================================================================
"""

bw2_db = lci_to_bw2(mydb)   # The excel file is now in the form of a dictionnary.
#print(bw2_db)              # To help visualize the dictionnary.
print(bw.databases)


if Db_name in bw.databases :
    del bw.databases[Db_name] 
print(bw.databases)

# Creating a new database : 

t_db = Database(Db_name)



# Acquiring the data from the dictionnary : 

t_db.write(bw2_db)

# Important note :
                # Should the program return "Database is locked" as an error at this point, restarting the kernel and running everything
                # at once should fix this. 
                # If an error "list index out of range" occurs, one explanation may be there is still data in some of the excel cells,
                # for instance a space " ". Use "print(mydb)" as a command to see if the excel file is longuer than expected. 

                # Sometimes, errors spurr out of miss-naming processes (creating twice the name, but 2 codes or vice-versa)
                # This will throw errors such as "Technosphere matrix isn't square" and will prevent LCIA calculations.
                # The message will quote a number of rows and lines being uneven. To find the processes :
"""               
                for ds in Database("Consequential inventory"):
                    for prod_exc in ds.production():
                        if ((prod_exc['input'][1]) != ds['code']):
                            print((ds['name'],ds['code'],prod_exc['input']))
                            
"""  

print('')

#%%

# ===========================================================================================
#       """ Generating the demand vector's activities and exchanges - foreground system : """
# ===========================================================================================

# Enter the name of the new database :  

Db_name = "Demand vector"

        # Note : This has to be the same name as the one in the excel spreadsheet. 

"""
# =============================================================================
#       Make sure to use the correct filepath to your own CSV file here :
# =============================================================================
"""

fpCSV = r'C:\Users\User\Brightway2\Spyder files\Inventory_model_MSC_PSR_2.csv' #make sure to reach the right filepath in your own comp.
mydb = pd.read_csv(fpCSV, header = 0, sep = ",") # if using csv file
mydb['Exchange uncertainty type'] = mydb['Exchange uncertainty type'].fillna(0).astype(int)

"""
# =============================================================================
# 
# =============================================================================
"""

bw2_db = lci_to_bw2(mydb)   # The excel file is now in the form of a dictionnary.
#print(bw2_db)              # To help visualize the dictionnary.
print(bw.databases)


if Db_name in bw.databases :
    del bw.databases[Db_name] 
print(bw.databases)

# Creating a new database : 

t_db = Database(Db_name)

# Acquiring the data from the dictionnary : 

t_db.write(bw2_db)

# Important note :
                # Should the program return "Database is locked" as an error at this point, restarting the kernel and running everything
                # at once should fix this. 
                # If an error "list index out of range" occurs, one explanation may be there is still data in some of the excel cells,
                # for instance a space " ". Use "print(mydb)" as a command to see if the excel file is longuer than expected. 

                # Sometimes, errors spurr out of miss-naming processes (creating twice the name, but 2 codes or vice-versa)
                # This will throw errors such as "Technosphere matrix isn't square" and will prevent LCIA calculations.
                # The message will quote a number of rows and lines being uneven. To find the processes :

            
"""             
for ds in Database("Demand vector"):
    for prod_exc in ds.production():
        if ((prod_exc['input'][1]) != ds['code']):
            print((ds['name'],ds['code'],prod_exc['input']))
                            
"""

print('')

#%% 

# =============================================================================
#                """ Parmaterization of the demand vector : """ 
# =============================================================================

# i) Select the recycling allocation method : 
#--------------------------------------------------------------------------------------------------
Partitioning_method_A = 'Cut off'
Partitioning_method_B = 'Open loop'
Partitioning_method_F = 'Open loop S2017'
Partitioning_method_G = 'Open loop VL'
Partitioning_method_H = 'Open loop VL S2017'

# ii) Define the parameters accordingly : 
#--------------------------------------------------------------------------------------------------

# List of parameters : 
RC = 0.0             #          # Usualy RC < 1
RRE = 0.53            #         # Usualy RRE < 1
C_RRE = 1         #             # Usualy 1 < C_RRE
CR_CRRE = 1         # Open-loops - multi and single.   
CR_CRRE_1st = 1
F_n_1 = 1        #    
F = 1            #     Open-loop
n = 1           #  Open-loop UL                # Supposed amount of previous cycles.
Q = 1

#--------------------------------------------------------------
# To model the wood cascade, some paramaters are defined aside here : 
# RC in this project is always 100% for the recycled content. Therefore : 
RCFPI = 1

# RRE Glued-lam : 
RREGL = 0.9

# RRE OSB : 
RREOSB = 0.9

# RRE PB : 
RREPB = 1

# RRE COGEN : 
RRECOGEN = 0

# iii) Acquire the LCI from the database: 
#--------------------------------------------------------------------------------------------------

# Enter the "Activity Code" field of the desired process : 

"""
#---------------------------------------------------------
#                    CUT-OFF DATABASE : 
#---------------------------------------------------------
"""

# CUT OFF ALLOCATIONS : 

#####################################
LCI1 = t_db.get("PVCOBCO_Etot_1_LCI")
LCI2 = t_db.get("PVCOBCO_Etot_2_LCI")
LCI3 = t_db.get("PVCOBCO_Etot_3_LCI")
LCI4 = t_db.get("PVCOBCO_Etot_4_LCI")
LCI5 = t_db.get("PVCOBCO_Etot_5_LCI")
#############
LCI6 = t_db.get("FPICOBCO_Etot_1_LCI")
LCI7 = t_db.get("FPICOBCO_Etot_2_LCI")
LCI8 = t_db.get("FPICOBCO_Etot_3_LCI")
LCI9 = t_db.get("FPICOBCO_Etot_4_LCI")
LCI10 = t_db.get("FPICOBCO_Etot_5_LCI")
#####################################

# SCHRIJVERS 2017 ALLOCATIONS :

######################################
LCI11 = t_db.get("PVOLSBCO_Etot_1_LCI")
LCI12 = t_db.get("PVOLSBCO_Etot_2_LCI")
LCI13 = t_db.get("PVOLSBCO_Etot_3_LCI")
LCI14 = t_db.get("PVOLSBCO_Etot_4_LCI")
LCI15 = t_db.get("PVOLSBCO_Etot_5_LCI")
#############
LCI16 = t_db.get("FPIOLSBCO_Etot_1_LCI")
LCI17 = t_db.get("FPIOLSBCO_Etot_2_LCI")
LCI18 = t_db.get("FPIOLSBCO_Etot_3_LCI")
LCI19 = t_db.get("FPIOLSBCO_Etot_4_LCI")
LCI20 = t_db.get("FPIOLSBCO_Etot_5_LCI")
#####################################

# PROPOSED ALLOCATIONS : 

######################################
LCI21 = t_db.get("PVOLPBCO_Etot_1_LCI")
LCI22 = t_db.get("PVOLPBCO_Etot_2_LCI")
LCI23 = t_db.get("PVOLPBCO_Etot_3_LCI")
LCI24 = t_db.get("PVOLPBCO_Etot_4_LCI")
LCI25 = t_db.get("PVOLPBCO_Etot_5_LCI")
##############
LCI26 = t_db.get("FPIOLPBCO_Etot_1_LCI")
LCI27 = t_db.get("FPIOLPBCO_Etot_2_LCI")
LCI28 = t_db.get("FPIOLPBCO_Etot_3_LCI")
LCI29 = t_db.get("FPIOLPBCO_Etot_4_LCI")
LCI30 = t_db.get("FPIOLPBCO_Etot_5_LCI")
#######################################


"""
#---------------------------------------------------------
#      ALLOCATION AT POINT OF SUBSTITUTION DATABASE : 
#---------------------------------------------------------
"""

# CUT OFF ALLOCATIONS : 

#####################################
LCI31 = t_db.get("PVCOBAPOS_Etot_1_LCI")
LCI32 = t_db.get("PVCOBAPOS_Etot_2_LCI")
LCI33 = t_db.get("PVCOBAPOS_Etot_3_LCI")
LCI34 = t_db.get("PVCOBAPOS_Etot_4_LCI")
LCI35 = t_db.get("PVCOBAPOS_Etot_5_LCI")
#############
LCI36 = t_db.get("FPICOBAPOS_Etot_1_LCI")
LCI37 = t_db.get("FPICOBAPOS_Etot_2_LCI")
LCI38 = t_db.get("FPICOBAPOS_Etot_3_LCI")
LCI39 = t_db.get("FPICOBAPOS_Etot_4_LCI")
LCI40 = t_db.get("FPICOBAPOS_Etot_5_LCI")
#####################################

# SCHRIJVERS 2017 ALLOCATIONS :

######################################
LCI41 = t_db.get("PVOLSBAPOS_Etot_1_LCI")
LCI42 = t_db.get("PVOLSBAPOS_Etot_2_LCI")
LCI43 = t_db.get("PVOLSBAPOS_Etot_3_LCI")
LCI44 = t_db.get("PVOLSBAPOS_Etot_4_LCI")
LCI45 = t_db.get("PVOLSBAPOS_Etot_5_LCI")
#############
LCI46 = t_db.get("FPIOLSBAPOS_Etot_1_LCI")
LCI47 = t_db.get("FPIOLSBAPOS_Etot_2_LCI")
LCI48 = t_db.get("FPIOLSBAPOS_Etot_3_LCI")
LCI49 = t_db.get("FPIOLSBAPOS_Etot_4_LCI")
LCI50 = t_db.get("FPIOLSBAPOS_Etot_5_LCI")
#####################################

# PROPOSED ALLOCATIONS : 

######################################
LCI51 = t_db.get("PVOLPBAPOS_Etot_1_LCI")
LCI52 = t_db.get("PVOLPBAPOS_Etot_2_LCI")
LCI53 = t_db.get("PVOLPBAPOS_Etot_3_LCI")
LCI54 = t_db.get("PVOLPBAPOS_Etot_4_LCI")
LCI55 = t_db.get("PVOLPBAPOS_Etot_5_LCI")
##############
LCI56 = t_db.get("FPIOLPBAPOS_Etot_1_LCI")
LCI57 = t_db.get("FPIOLPBAPOS_Etot_2_LCI")
LCI58 = t_db.get("FPIOLPBAPOS_Etot_3_LCI")
LCI59 = t_db.get("FPIOLPBAPOS_Etot_4_LCI")
LCI60 = t_db.get("FPIOLPBAPOS_Etot_5_LCI")
#######################################

"""
#---------------------------------------------------------
#      CONSEQUENTIAL MODELLING : 
#---------------------------------------------------------
"""

# CUT-OFF DATABASE : 

LCI61 = t_db.get("FPICQBCO_Etot_5_LCI")

# CONSEQUENTIAL DATABASE : 

LCI62 = t_db.get("FPICQBCQ_Etot_5_LCI")


# iv) Calculate the new flows: 
#--------------------------------------------------------------------------------------------------

# First, wipe out the existing groups of parametrized flows : 
for groups in Group :   
    Group.delete_by_id(groups)
    
# Then, generate the new ones : 


"""
#---------------------------------------------------------
#                    CUT-OFF DATABASE : 
#---------------------------------------------------------
"""

# CUT OFF PARAMETRIZATION :     
    
Recycling_allocation(Partitioning_method_A,LCI1,Db_name,RC,RRE)
Recycling_allocation(Partitioning_method_A,LCI2,Db_name,RC,RRE)
Recycling_allocation(Partitioning_method_A,LCI3,Db_name,RC,RRE)
Recycling_allocation(Partitioning_method_A,LCI4,Db_name,RC,RRE)
Recycling_allocation(Partitioning_method_A,LCI5,Db_name,RC,0)
#--------------------------------------------------------------------
Recycling_allocation(Partitioning_method_A,LCI6,Db_name,RC,RRE)
Recycling_allocation(Partitioning_method_A,LCI7,Db_name,RCFPI,RREGL)
Recycling_allocation(Partitioning_method_A,LCI8,Db_name,RCFPI,RREOSB)
Recycling_allocation(Partitioning_method_A,LCI9,Db_name,RCFPI,RREPB)
Recycling_allocation(Partitioning_method_A,LCI10,Db_name,RCFPI,RRECOGEN)
#--------------------------------------------------------------------

# SCHRIJVERS 2017 PARAMETRIZATION : 

#Recycling_allocation(Partitioning_method_F,LCI11,Db_name,RRE,1)
#Recycling_allocation(Partitioning_method_F,LCI12,Db_name,RRE,2)
#Recycling_allocation(Partitioning_method_F,LCI13,Db_name,RRE,3)
#Recycling_allocation(Partitioning_method_F,LCI14,Db_name,RRE,4)
#Recycling_allocation(Partitioning_method_F,LCI15,Db_name,0,5)
#--------------------------------------------------------------------
#Recycling_allocation(Partitioning_method_H,LCI16,Db_name,1)
#Recycling_allocation(Partitioning_method_H,LCI17,Db_name,2)
#Recycling_allocation(Partitioning_method_H,LCI18,Db_name,3)
#Recycling_allocation(Partitioning_method_H,LCI19,Db_name,4)
#Recycling_allocation(Partitioning_method_H,LCI20,Db_name,5)
#--------------------------------------------------------------------

# PROPOSED METHOD PARAMETRIZATION :

#Recycling_allocation(Partitioning_method_B,LCI21,Db_name,RRE,Q,1)
#Recycling_allocation(Partitioning_method_B,LCI22,Db_name,RRE,Q,2)
#Recycling_allocation(Partitioning_method_B,LCI23,Db_name,RRE,Q,3)
#Recycling_allocation(Partitioning_method_B,LCI24,Db_name,RRE,Q,4)
#Recycling_allocation(Partitioning_method_B,LCI25,Db_name,0,Q,5)
#--------------------------------------------------------------------
#Recycling_allocation(Partitioning_method_G,LCI26,Db_name,1)
#Recycling_allocation(Partitioning_method_G,LCI27,Db_name,2)
#Recycling_allocation(Partitioning_method_G,LCI28,Db_name,3)
#Recycling_allocation(Partitioning_method_G,LCI29,Db_name,4)
#Recycling_allocation(Partitioning_method_G,LCI30,Db_name,5)

"""
#---------------------------------------------------------
#      ALLOCATION AT POINT OF SUBSTITUTION DATABASE : 
#---------------------------------------------------------
"""

# CUT OFF PARAMETRIZATION :     
    
#Recycling_allocation(Partitioning_method_A,LCI31,Db_name,RC,RRE)
#Recycling_allocation(Partitioning_method_A,LCI32,Db_name,RC,RRE)
#Recycling_allocation(Partitioning_method_A,LCI33,Db_name,RC,RRE)
#Recycling_allocation(Partitioning_method_A,LCI34,Db_name,RC,RRE)
#Recycling_allocation(Partitioning_method_A,LCI35,Db_name,RC,0)
#--------------------------------------------------------------------
#Recycling_allocation(Partitioning_method_A,LCI36,Db_name,RC,RRE)
#Recycling_allocation(Partitioning_method_A,LCI37,Db_name,RCFPI,RREGL)
#Recycling_allocation(Partitioning_method_A,LCI38,Db_name,RCFPI,RREOSB)
#Recycling_allocation(Partitioning_method_A,LCI39,Db_name,RCFPI,RREPB)
#Recycling_allocation(Partitioning_method_A,LCI40,Db_name,RCFPI,RRECOGEN)
#--------------------------------------------------------------------

# SCHRIJVERS 2017 PARAMETRIZATION : 

#Recycling_allocation(Partitioning_method_F,LCI41,Db_name,RRE,1)
#Recycling_allocation(Partitioning_method_F,LCI42,Db_name,RRE,2)
#Recycling_allocation(Partitioning_method_F,LCI43,Db_name,RRE,3)
#Recycling_allocation(Partitioning_method_F,LCI44,Db_name,RRE,4)
#Recycling_allocation(Partitioning_method_F,LCI45,Db_name,0,5)
#--------------------------------------------------------------------
#Recycling_allocation(Partitioning_method_H,LCI46,Db_name,1)
#Recycling_allocation(Partitioning_method_H,LCI47,Db_name,2)
#Recycling_allocation(Partitioning_method_H,LCI48,Db_name,3)
#Recycling_allocation(Partitioning_method_H,LCI49,Db_name,4)
#Recycling_allocation(Partitioning_method_H,LCI50,Db_name,5)
#--------------------------------------------------------------------

# PROPOSED METHOD PARAMETRIZATION :

#Recycling_allocation(Partitioning_method_B,LCI51,Db_name,RRE,Q,1)
#Recycling_allocation(Partitioning_method_B,LCI52,Db_name,RRE,Q,2)
#Recycling_allocation(Partitioning_method_B,LCI53,Db_name,RRE,Q,3)
#Recycling_allocation(Partitioning_method_B,LCI54,Db_name,RRE,Q,4)
#Recycling_allocation(Partitioning_method_B,LCI55,Db_name,0,Q,5)
#--------------------------------------------------------------------
#Recycling_allocation(Partitioning_method_G,LCI56,Db_name,1)
#Recycling_allocation(Partitioning_method_G,LCI57,Db_name,2)
#Recycling_allocation(Partitioning_method_G,LCI58,Db_name,3)
#Recycling_allocation(Partitioning_method_G,LCI59,Db_name,4)
#Recycling_allocation(Partitioning_method_G,LCI60,Db_name,5)

"""
#---------------------------------------------------------
#                CONSEQUENTIAL MODELLING : 
#---------------------------------------------------------
"""

# CUT-OFF DATABASE : 

#Recycling_allocation('Consequential cascading',LCI61,Db_name,5)

# CONSEQUENTIAL DATABASE : 

#Recycling_allocation('Consequential cascading',LCI62,Db_name,5)


#%%

# =============================================================================
#                        """ LCIA of the system : """
# =============================================================================

# i) Generate the functional unit : 
#---------------------------------------------------------------------------------------------------

# Products of interest in this LCA : 
# Fill the list of codes (coming from the inventory_model file) : 
# Then, assign an amount to the functional unit : 

List_of_codes = ("FPICOBCO_Etot_2_LCI",
                 ) 

List_of_quantities = {
        
'rate_A' : 1,}


# Extracting the functionnal unit's amounts in the program : 
temp_list_A = []
for rate in List_of_quantities :
    temp_list_A.append(List_of_quantities.get(rate))
    
# Extracting codes according to variables : 
counter = 0
Compared_elements = []   # Note : Also used to generate the graphes (item count and hue)
temp_list = []
if len(List_of_quantities) == len(List_of_codes) : 
    for ele in List_of_quantities :
        ele1 = t_db.get(List_of_codes[counter])
        temp_list.append(ele1)
        Compared_elements.append(ele1['code'])
        counter = counter+1 
else : 
    print('Please fix the amount of variables names to match the amount of codes.')

   
# Number of compared processes 
Amount_compared = 0
for ele in Compared_elements:
    Amount_compared = Amount_compared+1


# A list of all the required elements by the functionnal unit : 
list_functional_units = []
counter = 0 
for element in temp_list : 
    list_functional_units.append({element.key:temp_list_A[counter]})  
    counter = counter + 1
 
    
    
# ii) Generate the list of methods to characterize the inventory : 
#---------------------------------------------------------------------------------------------------
# Make a list of all impact method names (tuples):
Method_counter = []


#---------------------------------------------------------------------------------------------------
# Including IMPACT 2002+ methods : 
Impact2002_total = [method for method in bw.methods if "IMPACT 2002+" in str(method) and "total" in str(method)]
print(Impact2002_total)
for method in Impact2002_total : 
    Method_counter.append(method)

#---------------------------------------------------------------------------------------------------
# Including TRACI methods : 
#TRACI = [method for method in bw.methods if "TRACI" in str(method) and "environmental impact" in str(method)]
#print(TRACI)
#for method in TRACI : 
#    Method_counter.append(method)

#---------------------------------------------------------------------------------------------------

# And the list of methods that is desired : 
list_methods = Method_counter

# Since methods have names using commas, to extract their common names : 
list_of_shorter_methods = []
for method in Method_counter :
    if "IMPACT 2002+" in str(method) :
        print(method[1])
        list_of_shorter_methods.append(method[1])
    if "TRACI" in str(method[0]) :
        print(method[2])
        list_of_shorter_methods.append(method[2])
   
print(list_of_shorter_methods)     
shorter_methods = tuple(list_of_shorter_methods)


# iii) Run the calculations : 
#---------------------------------------------------------------------------------------------------


# a) Single process (i.e. : Process contribution)
if len(list_functional_units) == 1 :

    # Contribution analysis options : 
    Contribution_of_processes_option = False
    Graph_traversal_option = False
    
    # Initializing required variables (all options included) :
    Score = np.array([])
    Contri_ana = ContributionAnalysis()
    Contributions_df = pd.DataFrame([])
    Graph_trav = GraphTraversal()
    Graph_traversal_df = pd.DataFrame([])
    
    # Performing the LCA calculation (per LCIA method) :
    
    single_activity = t_db.get(List_of_codes)
    SingleLCA = bw.LCA({single_activity:List_of_quantities.get(rate)}, list_methods[0]) # Do LCA with one impact category
    SingleLCA.lci()
    for category in list_methods:
        SingleLCA.switch_method(category)
        SingleLCA.lcia()
        Score = np.append(Score,SingleLCA.score)
        
    # Contribution of processes : 
        if Contribution_of_processes_option :
            Contributions = Contri_ana.annotated_top_processes(SingleLCA,names = True)
            dataframed_Contributions = pd.DataFrame(data = Contributions)
            dataframed_Contributions.drop(dataframed_Contributions.columns[1],axis=1,inplace = True)
            dataframed_Contributions[dataframed_Contributions.columns[0]]=dataframed_Contributions[dataframed_Contributions.columns[0]]/(SingleLCA.score)*100
            Contributions_df = pd.concat([Contributions_df,dataframed_Contributions.head(8)],axis = 1) 

    # Graph traversal : 
        if Graph_traversal_option :
            
            # 1st : Perform graph traversal and recover links for activity names : 
            Traversed_Graph = Graph_trav.calculate({single_activity:List_of_quantities.get(rate)},category,cutoff = 0.01,max_calc = 5000.0,skip_coproducts = False)
            Traversed_Graph_df2 = pd.DataFrame(data = Traversed_Graph['edges'])
            ra, rp, rb = SingleLCA.reverse_dict() 
            dfra = pd.DataFrame(data = ra)
            
            # 2nd : Change Edge ids for activities names and insert into a dataframe :
            
            i = 1
            j = 0
            Traversed_Graph_df3 = Traversed_Graph_df2.copy()
        
            for x in Traversed_Graph_df2['to'] :
                if x > 0 :        
                    Traversed_db = dfra.loc[0,x]
                    Traversed_code = dfra.loc[1,x]
                    Traversed_act_name =(Traversed_db,Traversed_code) 
                    a = get_activity(Traversed_act_name)
                    Traversed_Graph_df3.loc[i,'to'] = str(get_activity(Traversed_act_name))
                    i = i+1
        
            for x in Traversed_Graph_df2['from'] :      
                    Traversed_db = dfra.loc[0,x]
                    Traversed_code = dfra.loc[1,x]
                    Traversed_act_name =(Traversed_db,Traversed_code) 
                    a = get_activity(Traversed_act_name)
            
                    Traversed_Graph_df3.loc[j,'from'] = str(get_activity(Traversed_act_name))
                    j = j+1
    
            Traversed_Graph_df3.drop(Traversed_Graph_df3.columns[[2,3]],axis=1,inplace = True)
            Traversed_Graph_df3.drop([0],inplace = True)
            
            Graph_traversal_df = pd.concat([Graph_traversal_df,Traversed_Graph_df3.head(10)],axis = 1) 

    # Exporting everything into excel worksheets : 
"""
# ================================================================================
#       Make sure to fix the filepaths to match your expected output direction
# ================================================================================
"""


    if Graph_traversal_option :
        Graph_traversal_to_excel =  Graph_traversal_df.to_excel(r'C:\Users\User\Brightway2\Spyder files\Dataset profile\Traversed_Graph.xlsx',index = True, header = True)             
    if Contribution_of_processes_option :    
        Contributions_to_excel =  Contributions_df.to_excel(r'C:\Users\User\Brightway2\Spyder files\Dataset profile\Contribution_analysis.xlsx',index = True, header = True)            
    Score_TR = np.array([Score])
    Score_TR.T    
    Results = pd.DataFrame(columns=shorter_methods, index = Compared_elements, data=Score_TR)
    Results_to_excel = Results.to_excel(r'C:\Users\User\Brightway2\Spyder files\LCA_results.xlsx',index = True, header = True)
    print(Results)

else : 
 
# b) Multiple processes (Comparative LCA)
    
    bw.calculation_setups['Inventory modelling'] = {'inv':list_functional_units, 'ia':list_methods}
    # inv : inventory
    # ia : impact assessment
    lca = bw.MultiLCA('Inventory modelling') # Run LCA calculations with method
    lca.results
    Results = pd.DataFrame(columns=shorter_methods, index = Compared_elements, data=lca.results)
    Results_to_excel = Results.to_excel(r'C:\Users\User\Brightway2\Spyder files\LCA_results.xlsx',index = True, header = True)
    print(Results)
    print('')  # Free space to read in the post-processor
    
    
"""    
# =============================================================================
# 
# =============================================================================
"""



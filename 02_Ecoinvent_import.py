# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 13:26:14 2019

@author: Xavier Tanguay
"""




def get_ei_db(ei_name) :

    
# =============================================================================
#    # Modify to reach your own directory where all your ecospold files are stored.  
# =============================================================================
    
# Generating the file path : 
    b = "\\"
    Directory1 = "C:\\Users\\User\\Brightway2\\Projects\\Database"          
    Directory2 = '\\ecospold2\\datasets'
    fpeiXX = (Directory1+b+ei_name+Directory2)  # Generates the actual filepath, allowing to change its name if multiple databases are desired.
                                                
# =============================================================================
# 
# =============================================================================

# First, let's check if the database has already been imported into the computer (which would save quite alot
# of time for the computer not to have to work for all those thousands of entries). If not, then the computer will 
# load it using this command. 

    bw.databases
    if ei_name in bw.databases:
        print("Database has already been imported")
    else:
        eixx = bw.SingleOutputEcospold2Importer(fpeiXX, ei_name)
        eixx.apply_strategies()
        eixx.statistics()
        eixx.write_database() # This will take some time.

# This command will allow the computer to actualy access the content of the database.

# Note : eixx is only an importer. It is not the database itself. To handle data within the database : 

    eidb = bw.Database(ei_name)

    print('The',ei_name,'database is a square matrix of : ',len(eidb), ' datasets.')  # Making sure the import worked properly.
    return eidb


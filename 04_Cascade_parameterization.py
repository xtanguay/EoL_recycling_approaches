# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:51:18 2019

@author: Xavier Tanguay
"""

def Recycling_allocation(Rule,LCI,Db_name,*args) :

    from bw2data.parameters import ActivityParameter, DatabaseParameter, ProjectParameter, Group   
    amnt_args=0
    

    
# CUT OFF :
#------------------------------------------------------------------------------
    if Rule == 'Cut off' :
        for args_count in args:
            amnt_args = amnt_args+1
            
        if amnt_args == 2 :
            print('Using the Cut-off allocation, the following parameters have been applied to the exchanges of the inventory model : RC & RRE')

            a = args[0]
            b = args[1]
            
            #--------------------------------------------------------------------------------
            #Note : This was created to allow different parameterized datasets off the same function.
                        
            groupname = "Cut off group "
            gname =(groupname+LCI[1]) 
            
            group_list = []
            for groups in Group :
                if gname in groups.name : 
                    group_list.append(groups.name)

            if gname not in group_list : 
                Group.create(name=gname)
            
            #---------------------------------------------------------------------------------------
            
            project_data1 = [{
                    'name': 'RC',
                    'formula': a,
                    'database' : Db_name,
                    'code' : LCI,
                    }, {
                            'name': 'RRE',
                            'database' : Db_name,
                            'code' : LCI,
                            'amount': b,}]
    
            parameters.new_activity_parameters(project_data1,gname)

            for exc in LCI.exchanges():
                if 'Ev' in exc.input[1] :
                    exc['amount'] = 0
                    exc['formula'] = '(100-RC*100)/100'  # Note : This is to reduce IEEE standard floating point issues with decimals.
                    exc.save()

                if 'Erc' in exc.input[1] :
                    exc['amount'] = 0
                    exc['formula'] = 'RC'
                    exc.save()
                if 'Ed' in exc.input[1] :
                    exc['amount'] = 0
                    exc['formula'] = '(100-RRE*100)/100' # Note : This is to reduce IEEE standard floating point issues with decimals.
                    exc.save()
                if 'E_rre' in exc.input[1] :
                    exc['amount'] = 0
                    exc['formula'] = 'RRE'
                    exc.save()             
                if 'ASB' in exc.input[1] :
                    exc['amount'] = 0
                    exc['formula'] = '1'
                    exc.save()    
                if 'DSB' in exc.input[1] :
                    exc['amount'] = 0
                    exc['formula'] = '1'
                    exc.save()  


                       
            # Setting them active now : 
            parameters.add_exchanges_to_group(gname,LCI)   # Notify Brightway2 that there is actualy formulas embedded.
            ActivityParameter.recalculate_exchanges(gname)  # Have the calculations performed with the parameters'values. 


            # And now, the exchanges : 
            print('The resulting exchanges are now : ')
            for exc in LCI.exchanges():
                print(exc.amount, exc.input, exc.output)
            print('')
            
        else : 
            print('Wrong amount of arguments was used. To use the Cut off method, please enter 5 arguments with the following synthax :\n',
                  '"Recycling_allocation(Allocation_Rule , LCI , Database_name , RC , RRE )"')
  

# OPEN LOOP (According to Schrijvers 2017 - generalized case) :
#------------------------------------------------------------------------------    
    elif Rule == 'Open loop S2017' :
        for args_count in args:
            amnt_args = amnt_args+1
        if amnt_args == 2 :
            
            print('Using the Open loop S2017 allocation - 1st LCI only, the following parameters have been applied'
                  ' to the exchanges of the inventory model : RRE , n')
            
            a = args[0]
            n = args[1]

            #--------------------------------------------------------------------------------
            #Note : This was created to allow different parameterized datasets off the same function.
                        
            groupname = "Open loop S2017 group "
            gname =(groupname+LCI[1]) 
            
            group_list = []
            for groups in Group :
                if gname in groups.name : 
                    group_list.append(groups.name)

            if gname not in group_list : 
                Group.create(name=gname)
            
            #---------------------------------------------------------------------------------------

            project_data2 = [{
                    'name': 'RRE',
                    'formula': a,
                    'database' : Db_name,
                    'code' : LCI,}, {
                            'name': 'LCA_share',
                            'formula': '1/(1+RRE)',
                            'database' : Db_name,
                            'code' : LCI,}]
    
            parameters.new_activity_parameters(project_data2,gname)

            #---------------------------------------------------------------------------------------
            # Preparing the unique identifiers :

            validation_code = LCI[1]                           
            lci_code = 'Etot_'+str(n)    
            lci_full_code = lci_code+'_LCI'
                    
            # Ev 
            sub_lci_exc_code_v = 'Ev'+str(n)
            act_code_v = validation_code.replace(lci_full_code,sub_lci_exc_code_v)
       
            # Erc
            sub_lci_exc_code_rc = 'Erc'+str(n)
            act_code_rc = validation_code.replace(lci_full_code,sub_lci_exc_code_rc)                                     
                    
            # Ed
            sub_lci_exc_code_d = 'Ed'+str(n)
            act_code_d = validation_code.replace(lci_full_code,sub_lci_exc_code_d)                      
                    
            # Erre
            sub_lci_exc_code_rre = 'E_rre'+str(n)
            act_code_rre = validation_code.replace(lci_full_code,sub_lci_exc_code_rre)                                      
            
            # ASB
            sub_lci_exc_code_A = 'ASB'+str(n)
            act_code_A = validation_code.replace(lci_full_code,sub_lci_exc_code_A)                   
                   
            # DSB
            sub_lci_exc_code_D = 'DSB'+str(n)
            act_code_D = validation_code.replace(lci_full_code,sub_lci_exc_code_D) 


            for exc in LCI.exchanges():
                if exc.input[1] == act_code_v :
                    exc['amount'] = 0
                    exc['formula'] = '1*LCA_share'  
                    exc.save()
                if exc.input[1] == act_code_rc :
                    exc['amount'] = 0
                    exc['formula'] = '0'
                    exc.save()
                if exc.input[1] == act_code_d :
                    exc['amount'] = 0
                    exc['formula'] = 'LCA_share*(100-RRE*100)/100' # Note : This is to reduce IEEE standard floating point issues with decimals.
                    exc.save()
                if exc.input[1] == act_code_rre :
                    exc['amount'] = 0
                    exc['formula'] = 'RRE*LCA_share'
                    exc.save()
                if exc.input[1] == act_code_A :
                    exc['amount'] = 0
                    exc['formula'] = '1*LCA_share'
                    exc.save()    
                if exc.input[1] == act_code_D :
                    exc['amount'] = 0
                    exc['formula'] = '1*LCA_share'
                    exc.save() 

                
            # Setting them active now : 
            parameters.add_exchanges_to_group(gname,LCI)   # Notify Brightway2 that there is actualy formulas embedded.
            ActivityParameter.recalculate_exchanges(gname)  # Have the calculations performed with the parameters'values. 



            # And now, the exchanges : 
            print('The resulting exchanges are now : ')
            for exc in LCI.exchanges():
                print(exc.amount, exc.input, exc.output)          
            print('')
            
        else : 
            print('Wrong amount of arguments was used. To use the Open loop S2017 method, please enter 5 arguments with the following synthax :\n',
            '"Recycling_allocation(Allocation_Rule , LCI , Databse_name , RRE , n )"')  
            
# OPEN LOOP - Proposed version (1st LCI) :
#------------------------------------------------------------------------------  

    elif Rule == 'Open loop' :
        for args_count in args:
            amnt_args = amnt_args+1
        if amnt_args == 3 :
            
            print('Using the Open loop allocation for 1st LCI only, the following parameters have been applied to '
                  'the exchanges of the inventory model : RRE , Q , n ')
   

            a = args[0]
            b = args[1]
            n = args[2]

            #--------------------------------------------------------------------------------
            #Note : This was created to allow different parameterized datasets off the same function.
                        
            groupname = "Open loop group "
            gname =(groupname+LCI[1]) 
            
            group_list = []
            for groups in Group :
                if gname in groups.name : 
                    group_list.append(groups.name)

            if gname not in group_list : 
                Group.create(name=gname)
            
            #---------------------------------------------------------------------------------------
            # Generating the paramtrization parameters :

            project_data5 = [{
                            'name': 'RRE',
                            'formula': a,
                            'database' : Db_name,
                            'code' : LCI,},{
                            'name': 'Q',
                            'formula': b,
                            'database' : Db_name,
                            'code' : LCI,},{
                            'name': 'LCA_share',
                            'formula': '1/(1+RRE*Q)',
                            'database' : Db_name,
                            'code' : LCI,}]
    
            parameters.new_activity_parameters(project_data5,gname)

            #---------------------------------------------------------------------------------------
            # Preparing the unique identifiers :

            validation_code = LCI[1]                           
            lci_code = 'Etot_'+str(n)    
            lci_full_code = lci_code+'_LCI'
                    
            # Ev 
            sub_lci_exc_code_v = 'Ev'+str(n)
            act_code_v = validation_code.replace(lci_full_code,sub_lci_exc_code_v)
       
            # Erc
            sub_lci_exc_code_rc = 'Erc'+str(n)
            act_code_rc = validation_code.replace(lci_full_code,sub_lci_exc_code_rc)                                     
                    
            # Ed
            sub_lci_exc_code_d = 'Ed'+str(n)
            act_code_d = validation_code.replace(lci_full_code,sub_lci_exc_code_d)                      
                    
            # Erre
            sub_lci_exc_code_rre = 'E_rre'+str(n)
            act_code_rre = validation_code.replace(lci_full_code,sub_lci_exc_code_rre)                                      
            
            # ASB
            sub_lci_exc_code_A = 'ASB'+str(n)
            act_code_A = validation_code.replace(lci_full_code,sub_lci_exc_code_A)                   
                   
            # DSB
            sub_lci_exc_code_D = 'DSB'+str(n)
            act_code_D = validation_code.replace(lci_full_code,sub_lci_exc_code_D) 

            #---------------------------------------------------------------------------------------
            # Replacing the values : 

            for exc in LCI.exchanges():
                if exc.input[1] == act_code_v :
                    exc['amount'] = 0
                    exc['formula'] = '1*LCA_share' 
                    exc.save()
                if exc.input[1] == act_code_rc :
                    exc['amount'] = 0
                    exc['formula'] = '0'
                    exc.save()
                if exc.input[1] == act_code_d :
                    exc['amount'] = 0
                    exc['formula'] = 'LCA_share*(100-RRE*100)/100' # Note : This is to reduce IEEE standard floating point issues with decimals.
                    exc.save()
                if exc.input[1] == act_code_rre :
                    exc['amount'] = 0
                    exc['formula'] = 'RRE*LCA_share'
                    exc.save()
                if exc.input[1] == act_code_A :
                    exc['amount'] = 0
                    exc['formula'] = '1*LCA_share'
                    exc.save()    
                if exc.input[1] == act_code_D :
                    exc['amount'] = 0
                    exc['formula'] = '1*LCA_share'
                    exc.save() 

            #---------------------------------------------------------------------------------------                                  
            # Setting them active now : 
            parameters.add_exchanges_to_group(gname,LCI)   # Notify Brightway2 that there is actualy formulas embedded.
            ActivityParameter.recalculate_exchanges(gname)  # Have the calculations performed with the parameters'values. 

            #---------------------------------------------------------------------------------------
            # And now, the exchanges : 
            print('The resulting exchanges are now : ')
            for exc in LCI.exchanges():
                print(exc.amount, exc.input, exc.output)
            print('')
            #---------------------------------------------------------------------------------------            

        else : 
            print('Wrong amount of arguments was used. To use the Open loop method for the 1st LCI, please enter 6 arguments with the following synthax :\n',
            '"Recycling_allocation(Allocation_Rule , LCI , Database_name , RRE , Q , n "')  
            

# OPEN LOOP - Various life cycles :
#------------------------------------------------------------------------------  
    
    elif Rule == 'Open loop VL' :
        for args_count in args:
            amnt_args = amnt_args+1
        if amnt_args == 1 :
            



            #-----------------------------------------------------------------------------------------            
            # Initialization of the variables :
            
            n = args[0]     
            n_i = 1
            RRE_i = 0  
            RC = 0   # 1st life cycle doesn't contain any recycled content (or could always be fixed here)
            Q_i = 0    

            #-----------------------------------------------------------------------------------------            
            # Basic validation :       
 
            validation_code = LCI[1]
            print(validation_code)                
            lci_code = 'Etot_'+str(n)
                        
            try :
                validation_act = t_db.get(validation_code)

            #-----------------------------------------------------------------------------------------            
            # Introductory message :


                print('Using the Open loop VL allocation, the following parameters have to be defined iteratively : \n'
                  'RRE, RC , CR_CRRE and Q. Please fill them as they are requested in the IPython console.')          


            #-----------------------------------------------------------------------------------------            
            # Loop calculations :

                print('##########################################')

                while n_i < n+1 : 
                
                    # Updating to the new activity : 
                    
                    sub_lci_code = 'Etot_'+str(n_i)
                    activity_code = validation_code.replace(lci_code,sub_lci_code)

                    print('Evaluating the inventory for the life cycle of :',activity_code)             
                    activity = t_db.get(activity_code) 
                
                   #-----------------------------------------------------------------------------------------
                   # Acquiring the new parameters of the loop : 
                   
                   
                    # Retrieving RRE :               
                    #-----------------------------------------------------------------                   
                    print("Enter the RRE value for the life cycle number",n_i," :")
                    
                    while True : 
                        try :    
                            RRE = float(input())
                        
                    # Validates that RRE is inferior to 1 :                   
                            try :    
                                assert RRE <= 1 
                            except AssertionError :
                                    print('Invalid input. Please try again and enter a number between 0 and 1 for RRE in life cycle number',n_i)
                                    continue    
                            
                    # Validates that RRE is suprerior or equal to 0 : 
                            try : 
                                assert RRE >= 0
                            except AssertionError : 
                                    print('Invalid input. Please try again and enter a number between 0 and 1 for RRE in life cycle number',n_i)
                                    continue                        
                        
                   # Validates that it is indeed a number that was sent as an answer :      
                        except ValueError: 
                            print('Invalid input. Please try again and enter a number between 0 and 1 for RRE in life cycle number',n_i)
                            continue
                        else :
                            break
    
                     
                    # Retrieving RC :  
                    #-----------------------------------------------------------------                   
                    print("Enter the RC value for the life cycle number",n_i," :")
                    
                    while True : 
                        try :    
                            RC = float(input())
                        
                    # Validates that RC is inferior to 1 :                   
                            try :    
                                assert RC <= 1 
                            except AssertionError :
                                    print('Invalid input. Please try again and enter a number between 0 and 1 for RC in life cycle number',n_i)
                                    continue    
                            
                    # Validates that RC is suprerior or equal to 0 : 
                            try : 
                                assert RC >= 0
                            except AssertionError : 
                                    print('Invalid input. Please try again and enter a number between 0 and 1 for RC in life cycle number',n_i)
                                    continue                        
                        
                   # Validates that it is indeed a number that was sent as an answer :      
                        except ValueError: 
                            print('Invalid input. Please try again and enter a number between 0 and 1 for RC in life cycle number',n_i)
                            continue
                        else :
                            break
    
                    # Retrieving Q :       
                    #-----------------------------------------------------------------               
                    print("Enter the Q value for the life cycle number",n_i," :")
                    
                    while True : 
                        try :    
                            Q = float(input())
                        
                    # Validates that Q is inferior to 2 :                   
                            try :    
                                assert Q <= 2 
                            except AssertionError :
                                    print('Invalid input. Please try again and enter a number between 0 and 2 for Q in life cycle number',n_i)
                                    continue    
                            
                    # Validates that Q is suprerior or equal to 0 : 
                            try : 
                                assert Q >= 0
                            except AssertionError : 
                                    print('Invalid input. Please try again and enter a number between 0 and 2 for Q in life cycle number',n_i)
                                    continue                        
                        
                   # Validates that it is indeed a number that was sent as an answer :      
                        except ValueError: 
                            print('Invalid input. Please try again and enter a number between 0 and 2 for Q in life cycle number',n_i)
                            continue
                        else :
                            break
                        
                    # Retrieving CR_CRRE :       
                    #-----------------------------------------------------------------               
                    print("Enter the CR_CRRE value for the life cycle number",n_i," :")
                    
                    while True : 
                        try :    
                            CR_CRRE = float(input())
                          
                            
                    # Validates that Q is suprerior or equal to 0 : 
                            try : 
                                assert CR_CRRE >= 0
                            except AssertionError : 
                                    print('Invalid input. Please try again and enter a number higher than 0 for CR_CRRE in life cycle number',n_i)
                                    continue                        
                        
                   # Validates that it is indeed a number that was sent as an answer :      
                        except ValueError: 
                            print('Invalid input. Please try again and enter a number higher than 0 for CR_CRRE in life cycle number',n_i)
                            continue
                        else :
                            break
                             
                    
                    print("In the life cycle number",n_i,"\n The RRE value is :",RRE,"\n The RC value is :",RC,"\n The Q value is : ",Q,
                          "\n The CR_CRRE value is : ",CR_CRRE)  
                    
                    b_n_1 = 1/(1+RRE_i*Q_i)
                    b = 1/(1+RRE*Q)
                    
        
                    #-----------------------------------------------------------------------------------------
                    # Defining the new unique identifiers for the calculation : 
                    
                    lci_full_code = lci_code+'_LCI'
                                      
                    # Etot previous life cycle                  
                    sub_lci_exc_code_p = 'Etot_'+str(n_i-1)+'_LCI'
                    activity_code_p = validation_code.replace(lci_full_code,sub_lci_exc_code_p)
                    
                    # Ev 
                    sub_lci_exc_code_v = 'Ev'+str(n_i)
                    act_code_v = validation_code.replace(lci_full_code,sub_lci_exc_code_v)
                    
                    # Erc
                    sub_lci_exc_code_rc = 'Erc'+str(n_i)
                    act_code_rc = validation_code.replace(lci_full_code,sub_lci_exc_code_rc)                                     
                    
                    # Ed
                    sub_lci_exc_code_d = 'Ed'+str(n_i)
                    act_code_d = validation_code.replace(lci_full_code,sub_lci_exc_code_d)                      
                    
                    # Erre
                    sub_lci_exc_code_rre = 'E_rre'+str(n_i)
                    act_code_rre = validation_code.replace(lci_full_code,sub_lci_exc_code_rre)                                      
                    
                    # ASB
                    sub_lci_exc_code_A = 'ASB'+str(n_i)
                    act_code_A = validation_code.replace(lci_full_code,sub_lci_exc_code_A)                   
                   
                    # DSB
                    sub_lci_exc_code_D = 'DSB'+str(n_i)
                    act_code_D = validation_code.replace(lci_full_code,sub_lci_exc_code_D)                                      
                
                   #-----------------------------------------------------------------------------------------            
                   # Calculations for the current life cycle, using the previous life cycle's data.
                   # Here, Q_i and RRE_i are still the ones of the previous life cycle
                            
                    for exc in activity.exchanges() :
                        if exc.input[1] == activity_code_p :
                            exc['amount'] = (CR_CRRE*(1-b_n_1)/b_n_1)*b
                            exc.save() 
           
                #-----------------------------------------------------------------------------------------
                # Calculations for the current life cycle, using the actual life cycle's data.
    
            
                        if exc.input[1] == act_code_v :
                            exc['amount'] = ((100-RC*100)/100)*b  # Note : This is to reduce IEEE standard floating point issues with decimals.
                            exc.save()
                        
                        if exc.input[1] == act_code_rc :
                            exc['amount'] = RC*b  
                            exc.save()
                        
                        if exc.input[1] == act_code_d :
                            exc['amount'] = ((100-RRE*100)/100)*b  # Note : This is to reduce IEEE standard floating point issues with decimals.
                            exc.save()
                        
                        if exc.input[1] == act_code_rre :
                            exc['amount'] = RRE*b  
                            exc.save()
                            
                        if exc.input[1] == act_code_A :
                            exc['amount'] = b  
                            exc.save()
                            
                        if exc.input[1] == act_code_D :
                            exc['amount'] = b  
                            exc.save()
                    
    
                #-----------------------------------------------------------------------------------------
                    # Updating the variables to become the ones of the previous life-cycle.
                    Q_i = Q
                    RRE_i = RRE                           
                #-----------------------------------------------------------------------------------------
                # End of the while loop.  
                
                    n_i = n_i+1
                    print('##########################################') 
                #-----------------------------------------------------------------------------------------
                # Presenting the final exchanges, for the whole inventory involved : 
        
                n_i = 1  # Counter reset
                print('The resulting exchanges are now :')   
                                
                while n_i < n+1 : 
                    
                    sub_lci_code = 'Etot_'+str(n_i)
                    activity_code_display = validation_code.replace(lci_code,sub_lci_code)
                    activity_display = t_db.get(activity_code_display)   
                
                    print('\nThe exchanges of',activity_code_display,'are now given by :')
                    
                    for exc in activity_display.exchanges():
                        print(exc.amount, exc.input,'to', exc.output)               
                                    
                    n_i = n_i+1         
                         
                print('##########################################')
                print('')
                      
            #-----------------------------------------------------------------------------------------
            # End of the try scenario, preventing crashes in case the excel file doesn't hold enough modelled life cycles.                    
            except : 
                print("The amount of modelled life cycles in the Inventory_model.csv file doesn't correspond to the amount requested with n_VL")   
            #-----------------------------------------------------------------------------------------
                
        else : 
            print('Wrong amount of arguments used. To use the Open loop VL method , please enter '
                  '4 arguments with the following synthax :\n',
            '"Recycling_allocation(Allocation_Rule , LCI , Database_name , n )"')   

       
# OPEN LOOP - Various life cycles (According to Schrijvers 2017) :
#------------------------------------------------------------------------------  
    
    elif Rule == 'Open loop VL S2017' :
        for args_count in args:
            amnt_args = amnt_args+1
        if amnt_args == 1 :
            



            #-----------------------------------------------------------------------------------------            
            # Initialization of the variables :
            
            n = args[0]     
            n_i = 1 
            RC = 0   # 1st life cycle doesn't contain any recycled content (or could always be fixed here)
  

            #-----------------------------------------------------------------------------------------            
            # Basic validation :       

            validation_code = LCI[1]
            print(validation_code)                
            lci_code = 'Etot_'+str(n)

            try :
                validation_act = t_db.get(validation_code)



            #-----------------------------------------------------------------------------------------            
            # Introductory message :


                print('Using the Open loop VL S2017 allocation, the following parameters have to be defined iteratively : \n'
                  'RRE, RC . Please fill them as they are requested in the IPython console.')          


            #-----------------------------------------------------------------------------------------            
            # Loop calculations :

                print('##########################################')

                while n_i < n+1 : 
                
                    # Updating to the new activity : 
                    
                    sub_lci_code = 'Etot_'+str(n_i)
                    activity_code = validation_code.replace(lci_code,sub_lci_code)

                    print('Evaluating the inventory for the life cycle of :',activity_code)             
                    activity = t_db.get(activity_code)
             
                   #-----------------------------------------------------------------------------------------
                   # Acquiring the new parameters of the loop : 
                   
                   
                    # Retrieving RRE :               
                    #-----------------------------------------------------------------                   
                    print("Enter the RRE value for the life cycle number",n_i," :")
                    
                    while True : 
                        try :    
                            RRE = float(input())
                        
                    # Validates that RRE is inferior to 1 :                   
                            try :    
                                assert RRE <= 1 
                            except AssertionError :
                                    print('Invalid input. Please try again and enter a number between 0 and 1 for RRE in life cycle number',n_i)
                                    continue    
                            
                    # Validates that RRE is suprerior or equal to 0 : 
                            try : 
                                assert RRE >= 0
                            except AssertionError : 
                                    print('Invalid input. Please try again and enter a number between 0 and 1 for RRE in life cycle number',n_i)
                                    continue                        
                        
                   # Validates that it is indeed a number that was sent as an answer :      
                        except ValueError: 
                            print('Invalid input. Please try again and enter a number between 0 and 1 for RRE in life cycle number',n_i)
                            continue
                        else :
                            break
    
                     
                    # Retrieving RC :  
                    #-----------------------------------------------------------------                   
                    print("Enter the RC value for the life cycle number",n_i," :")
                    
                    while True : 
                        try :    
                            RC = float(input())
                        
                    # Validates that RC is inferior to 1 :                   
                            try :    
                                assert RC <= 1 
                            except AssertionError :
                                    print('Invalid input. Please try again and enter a number between 0 and 1 for RC in life cycle number',n_i)
                                    continue    
                            
                    # Validates that RC is suprerior or equal to 0 : 
                            try : 
                                assert RC >= 0
                            except AssertionError : 
                                    print('Invalid input. Please try again and enter a number between 0 and 1 for RC in life cycle number',n_i)
                                    continue                        
                        
                   # Validates that it is indeed a number that was sent as an answer :      
                        except ValueError: 
                            print('Invalid input. Please try again and enter a number between 0 and 1 for RC in life cycle number',n_i)
                            continue
                        else :
                            break
                    
                    print("In the life cycle number",n_i,"\n The RRE value is :",RRE)  
                    
                    
                    b = 1/(1+RRE)
                    
        
                    #-----------------------------------------------------------------------------------------
                    # Defining the new unique identifiers for the calculation : 
                    
                    lci_full_code = lci_code+'_LCI'
                                      
                    # Etot previous life cycle                  
                    sub_lci_exc_code_p = 'Etot_'+str(n_i-1)+'_LCI'
                    activity_code_p = validation_code.replace(lci_full_code,sub_lci_exc_code_p)
                    
                    # Ev 
                    sub_lci_exc_code_v = 'Ev'+str(n_i)
                    act_code_v = validation_code.replace(lci_full_code,sub_lci_exc_code_v)
                    
                    # Erc
                    sub_lci_exc_code_rc = 'Erc'+str(n_i)
                    act_code_rc = validation_code.replace(lci_full_code,sub_lci_exc_code_rc)                                     
                    
                    # Ed
                    sub_lci_exc_code_d = 'Ed'+str(n_i)
                    act_code_d = validation_code.replace(lci_full_code,sub_lci_exc_code_d)                      
                    
                    # Erre
                    sub_lci_exc_code_rre = 'E_rre'+str(n_i)
                    act_code_rre = validation_code.replace(lci_full_code,sub_lci_exc_code_rre)                                      
                    
                    # ASB
                    sub_lci_exc_code_A = 'ASB'+str(n_i)
                    act_code_A = validation_code.replace(lci_full_code,sub_lci_exc_code_A)                   
                   
                    # DSB
                    sub_lci_exc_code_D = 'DSB'+str(n_i)
                    act_code_D = validation_code.replace(lci_full_code,sub_lci_exc_code_D)                 
                
                   #-----------------------------------------------------------------------------------------            
                   # Calculations for the current life cycle, using the previous life cycle's data.
                   # Here, RRE_i is still the one of the previous life cycle
                            
                    for exc in activity.exchanges() :
                        if exc.input[1] == activity_code_p :
                            exc['amount'] = RC*b
                            exc.save() 
           
                #-----------------------------------------------------------------------------------------
                # Calculations for the current life cycle, using the actual life cycle's data.
    
            
                        if exc.input[1] == act_code_v :
                            exc['amount'] = ((100-RC*100)/100)*b  # Note : This is to reduce IEEE standard floating point issues with decimals.
                            exc.save()
                        
                        if exc.input[1] == act_code_rc :
                            exc['amount'] = RC*b  
                            exc.save()
                        
                        if exc.input[1] == act_code_d :
                            exc['amount'] = ((100-RRE*100)/100)*b  # Note : This is to reduce IEEE standard floating point issues with decimals.
                            exc.save()
                        
                        if exc.input[1] == act_code_rre :
                            exc['amount'] = RRE*b  
                            exc.save()
                            
                        if exc.input[1] == act_code_A :
                            exc['amount'] = b  
                            exc.save()
                            
                        if exc.input[1] == act_code_D :
                            exc['amount'] = b  
                            exc.save()
                                              
                #-----------------------------------------------------------------------------------------
                # End of the while loop.  
                
                    n_i = n_i+1
                    print('##########################################') 
                #-----------------------------------------------------------------------------------------
                # Presenting the final exchanges, for the whole inventory involved : 
        
                n_i = 1  # Counter reset
                print('The resulting exchanges are now :')   
                
                
                while n_i < n+1 : 
                    sub_lci_code = 'Etot_'+str(n_i)
                    activity_code_display = validation_code.replace(lci_code,sub_lci_code)
                    activity_display = t_db.get(activity_code_display)   
                
                    print('\nThe exchanges of',activity_code_display,'are now given by :')
                    
                    for exc in activity_display.exchanges():
                        print(exc.amount, exc.input,'to', exc.output)               
                                    
                    n_i = n_i+1  
                    
                print('##########################################')   
                print('')
                      
            #-----------------------------------------------------------------------------------------
            # End of the try scenario, preventing crashes in case the excel file doesn't hold enough modelled life cycles.                    
            except : 
                print("The amount of modelled life cycles in the Inventory_model.csv file doesn't correspond to the amount requested with n_VL")   
            #-----------------------------------------------------------------------------------------
                
        else : 
            print('Wrong amount of arguments used. To use the Open loop VL S2017 method , please enter '
                  '4 arguments with the following synthax :\n',
            '"Recycling_allocation(Allocation_Rule , LCI , Database_name , n )"')   
     

# Consequential approach :
#------------------------------------------------------------------------------  
    
    elif Rule == 'Consequential cascading' :
        for args_count in args:
            amnt_args = amnt_args+1
        if amnt_args == 1 :
            



            #-----------------------------------------------------------------------------------------            
            # Initialization of the variables :
            
            n = args[0]     
            n_i = 1
   
            #-----------------------------------------------------------------------------------------            
            # Basic validation :       
 
            validation_code = LCI[1]
            print(validation_code)                
            lci_code = 'Etot_'+str(n)
                        
            try :
                validation_act = t_db.get(validation_code)

            #-----------------------------------------------------------------------------------------            
            # Introductory message :


                print('Using the Consequential cascading approach, the following parameter have to be defined iteratively : \n'
                  'd. Please fill this parameter as it is requested in the IPython console.')          


            #-----------------------------------------------------------------------------------------            
            # Loop calculations :

                print('##########################################')

                while n_i < n+1 : 
                
                    # Updating to the new activity : 
                    
                    sub_lci_code = 'Etot_'+str(n_i)
                    activity_code = validation_code.replace(lci_code,sub_lci_code)

                    print('Evaluating the inventory for the life cycle of :',activity_code)             
                    activity = t_db.get(activity_code) 
                
                   #-----------------------------------------------------------------------------------------
                   # Acquiring the new substitution rate parameter (d) of the loop : 
                   
                    print("Enter the substitution rate value for the life cycle number",n_i," :")
                    
                    while True : 
                        try :    
                            d = float(input())
                        
                    # Validates that d is inferior to 2 :                   
                            try :    
                                assert d <= 2 
                            except AssertionError :
                                    print('Invalid input. Please try again and enter a number between 0 and 2 for life cycle number',n_i)
                                    continue    
                            
                    # Validates that d is suprerior or equal to 0 : 
                            try : 
                                assert d >= 0
                            except AssertionError : 
                                    print('Invalid input. Please try again and enter a number between 0 and 2 for life cycle number',n_i)
                                    continue                        
                        
                   # Validates that it is indeed a number that was sent as an answer :      
                        except ValueError: 
                            print('Invalid input. Please try again and enter a number between 0 and 2 for life cycle number',n_i)
                            continue
                        else :
                            break
    

                    #-----------------------------------------------------------------------------------------
                    # Defining the new unique identifiers for the calculation : 
                    
                    lci_full_code = lci_code+'_LCI'
                                      
                    # Ecascade 
                    sub_lci_exc_code_cascade = 'Ecascade'+str(n_i)
                    act_code_cascade = validation_code.replace(lci_full_code,sub_lci_exc_code_cascade)       

                    # Esub 
                    sub_lci_exc_code_subst = 'Esub'+str(n_i)
                    act_code_subst = validation_code.replace(lci_full_code,sub_lci_exc_code_subst)
                    
                    # Ealt 
                    sub_lci_exc_code_alt = 'Ealt'+str(n_i)
                    act_code_alt = validation_code.replace(lci_full_code,sub_lci_exc_code_alt)
                                                                         
                   #-----------------------------------------------------------------------------------------            
                   # Adjusting the substitution ratio :
                   
                   # Note : To adjust the Ealt quantities, hardcoding has been used. This should be
                   #        revisited if the case study is modified.

                    #Ecascade 
                    for exc in activity.exchanges() : 
                        if exc.input[1] == act_code_cascade :                       
                            cascade_prod = t_db.get(exc.input[1])                        
                        
                            for content in cascade_prod.exchanges() : 
                                # This is hardcoded to keep how database was created originaly : 
                                
                                if 'Recycled_WC_cogeneration_CO' in content.input[1] :
                                    Recyc_prod = content['amount']
                                    
                                if 'Recyc_WC_cogeneration_conseq' in content.input[1] :
                                    Recyc_prod = content['amount']

                    # Esub
                    for exc in activity.exchanges() :

                        # First, modify the substitution rate :
                        if exc.input[1] == act_code_subst :
                            exc['amount'] = 1*d
                            exc.save()
                            
                        # Second, since the alternative energy production isn't proportionaly linked : 
                            substitution_data = t_db.get(exc.input[1])
                            for content in substitution_data.exchanges():
                                
                                # This is hardcoded to keep how database was created originaly : 
                                if 'Recycled_WC_cogeneration_CO' in content.input[1] :
                                    Recyc_regular = content['amount']

                                if 'Recyc_WC_cogeneration_conseq' in content.input[1] :
                                    Recyc_regular = content['amount']

                    # Ealt
                    for exc in activity.exchanges() :
                        if exc.input[1] == act_code_alt : 
                            alt_energy = t_db.get(exc.input[1])
                            
                            for content in alt_energy.exchanges() :                         
                                    content['amount'] = (Recyc_regular*-1*d)-Recyc_prod
                                    content.save()
                                    
                          
                #-----------------------------------------------------------------------------------------
                # End of the while loop.  
                
                    n_i = n_i+1
                    print('##########################################') 
                #-----------------------------------------------------------------------------------------
                # Presenting the final exchanges, for the whole inventory involved : 
        
                n_i = 1  # Counter reset
                print('The resulting exchanges are now :')   
                                
                while n_i < n+1 : 
                    
                    sub_lci_code = 'Etot_'+str(n_i)
                    activity_code_display = validation_code.replace(lci_code,sub_lci_code)
                    activity_display = t_db.get(activity_code_display)   
                
                    print('\nThe exchanges of',activity_code_display,'are now given by :')
                    
                    for exc in activity_display.exchanges():
                        print(exc.amount, exc.input,'to', exc.output)               
                                    
                    n_i = n_i+1         
                         
                print('##########################################')
                print('')
                      
            #-----------------------------------------------------------------------------------------
            # End of the try scenario, preventing crashes in case the excel file doesn't hold enough modelled life cycles.                    
            except : 
                print("The amount of modelled life cycles in the Inventory_model.csv file doesn't correspond to the amount requested with n")   
            #-----------------------------------------------------------------------------------------
                
        else : 
            print('Wrong amount of arguments used. To use the Consequential cascading method , please enter '
                  '4 arguments with the following synthax :\n',
            '"Recycling_allocation(Allocation_Rule , LCI , Database_name , n )"')   

#  If none of the previous were selected : 
#------------------------------------------------------------------------------
    else : 
       print('Invalid input. Pick one of the following allocation rule as string inputs : "Cut off" , "Open loop", Open loop S2017 '
             ' , "Open loop VL S2017" or "Open loop VL". Alternatively,'
             'use the Consequential substitution parameterization with : "Consequential cascading".')


   

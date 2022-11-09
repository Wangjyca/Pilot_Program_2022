"""
Copyright by Jingyu Wang 9.30.2022 

"""
import csv
from SumTool import text2lines, lines2dict, trimDollarMark

dict_setting_budgetName2standardName = {} #Translating dict from budget name to standrad catergory
dict_setting_quickbookName2standardName = {} #Translating dict from actual cost catergories at Quick Book to standrad catergories

list_inhouse_task = [] #Designated which task is in house job



def budgetCost_setting(filename:str)->bool:
     """
     To open a CVS file at which the users set how the categories of the Budget translating to the standard categories then generate a translating dictionary,
     See page 7, 8 and Graph 5 at page 9 in the proposal. 
     
     """
     try: 
         with open(filename,'r') as fd:
             for line in fd:
                  line = line.strip()
               
                  if not line:
                      continue
               
                  line2list = line.split(",")
               
                  if line2list[1].strip() =='@':
                    
                       list_inhouse_task.append(line2list[2].strip())

                  dict_setting_budgetName2standardName[line2list[2].strip()] = line2list[3].strip()
                         
     except FileNotFoundError:
          return False
     return True
   
def actualCost_setting(filename:str)->bool:
     """
     To open a CVS file at which the users set how the categories of actual cost named QB Category translating to the standard categories then generate a translating dictionary,
     See page 7 and Graph 6 at page 10 in the proposal. 
     """
     try: 
         with open(filename,'r') as fd:
              for line in fd:
                   line = line.strip()
               
                   if not line:
                        continue
               
                   line2list = line.split(",")
                
                   dict_setting_quickbookName2standardName[line2list[1].strip()] = line2list[2].strip()
                   
     except FileNotFoundError:
          return False
     
     return True               
              

def budgetReport_lines2list(lines)->tuple:
     '''
     This function takes the lines and turns it into a list named list_budgets in the form of
          [('Abatement', 0.0, 0.0, 0.0, '', 'Sub Abatement'),
           ('Rough Carpentry/Framing', 0, 0, 1700.0, 'H', 'Materials'),
           ('Rough Carpentry/Framing', 0, 0, 4200.0, 'H', 'Wage')...]
     Note: (Budget Name, Materials cost, wage cost, Materials cost+ wage cost , In house task/Not, Standard Catergory name)
     '''

 
     list_MissingBudgetItems_inSettingDict =[] #If items in the proposal are not in the translating dict, record them to this list
     list_budgets = [] # Clean up the list first

     for line in lines:
         littlelist = line.split('\t')
          
         if len(littlelist) >= 8:
            
             # set the in house tasks with H 
             inhouse_mark = ""
             if  littlelist[4].strip() in list_inhouse_task:
                 #"H" means that is for in house task
                 inhouse_mark = "H"

             # Mark the standard catergory to each budget item
             standard_catergory = ""
             """IF NOT IN THE DICt, WE NEED A LIST OF THE MISSING CATEGORY """
             if littlelist[4].strip() in dict_setting_budgetName2standardName: #the item in the budget is in the translating dict
                  standard_catergory = dict_setting_budgetName2standardName[littlelist[4].strip()]
             else:
                  list_MissingBudgetItems_inSettingDict.append(littlelist[4].strip())
                  
                  
             # Create the tuple for each item
             the_tuple =(littlelist[4].strip(),
                         float(trimDollarMark(littlelist[5])),
                         float(trimDollarMark(littlelist[6])),
                         float(trimDollarMark(littlelist[8])),
                         inhouse_mark,standard_catergory)
             
             list_budgets.append(the_tuple)

     # Split element of the list of in house task item to two elements,  labor cost at one element and materials cost at another element
     for i in range(len(list_budgets) - 1 , 0, -1):
          if list_budgets[i][4] == "H":
               list_budgets.insert( i + 1, (list_budgets[i][0],0,0,list_budgets[i][2],"H","Wages"))
               list_budgets[i] =           (list_budgets[i][0],0,0,list_budgets[i][1],"H","Materials")
               
     return (list_budgets,list_MissingBudgetItems_inSettingDict)



def budgetReport_lines2dict(lines)->tuple:     
     '''

     '''
     tuple_budgets = budgetReport_lines2list(lines)
     
     list_budgets = tuple_budgets[0]
     list_missing = tuple_budgets[1]
     dict_Budgets_Report={}
     
     for list_budget in list_budgets:
          dict_Budgets_Report[list_budget[5]] = dict_Budgets_Report.get(list_budget[5],0.00) + float(list_budget[3])
     return (dict_Budgets_Report, list_missing)    

def actualCostReport_lines2dict(lines)->tuple:
     """

     """
     list_MissingActualCostItems_inSettingDict =[]
     dict_ActualCost_Report = {}
     d_transactions = dict()
     d_transactions = lines2dict(lines)
     
     for d_transaction in d_transactions:
          """IF NOT IN THE DICt, WE NEED A LIST OF THE MISSING CATEGORY """
          if d_transaction in dict_setting_quickbookName2standardName:
               keyofStandard_C = dict_setting_quickbookName2standardName[d_transaction]
               dict_ActualCost_Report[keyofStandard_C] = dict_ActualCost_Report.get(keyofStandard_C,0.00) + float(d_transactions[d_transaction])
          else:
              list_MissingActualCostItems_inSettingDict.append(d_transaction)
     return (dict_ActualCost_Report,list_MissingActualCostItems_inSettingDict)
     

def comparison_report_2strings2dict(budget_report_string:str,actualcost_report_string:str)->dict:
     """
     After getting the budget and the actual cost reports in string form, the function generates the comparison report.
     
     Example: 
     Category:      Budget:      Actual Cost:    Profit or Loss:
     Wages	    $27,837.80	 $29,200.05	 $-1,362.25
     Permits	    $3,193.48	 $1,615.35	 $1,578.13
     Materials	    $7,104.20	 $8,231.50	 $-1,127.30
     Indirect Cost  $0.00	 $6,401.50	 $-6,401.50
     (S)Flooring    $5,910.00    $0.00	         $5,910.00
     ...
     """
     comparison_report_dict = {}
     
     lines = text2lines(budget_report_string)
     budget_report_dict = lines2dict(lines)

     lines = text2lines(actualcost_report_string)
     actualcost_report_dict = lines2dict(lines)

     # To get the AND set for the categories from both reports
     key_list_budget = [d for d in budget_report_dict]
     key_list_actualcost = [d for d in actualcost_report_dict ]
     key_set = set(key_list_budget + key_list_actualcost)

     # If the cetagory of the budget side is not exsiting, set the amount as zero. On the other hand, do the same for the actual cost side
     for key in key_set:
         if key:
             comparison_report_dict[key] = (budget_report_dict.get(key,0.00),\
                                           actualcost_report_dict.get(key,0.00),\
                                           budget_report_dict.get(key,0.00)- actualcost_report_dict.get(key,0.00))

     return comparison_report_dict


if __name__ == '__main__':
    import doctest
    doctest.testmod()

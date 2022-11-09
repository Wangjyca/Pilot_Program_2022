"""
Copyright by Hugo and Jingyu Wang 9.30.2022 

"""
import csv
from SumTool import text2lines, lines2dict, trimDollarMark

dict_setting_budgetName2standardName = {} #Translating dict from budget name to standrad catergory
dict_setting_quickbookName2standardName = {} #Translating dict from actual cost catergories at Quick Book to standrad catergories

list_inhouse_task = [] #Designated which task is in house job
#list_budgets = [] #list of the budget for displaying at the datawindow on the interface
#list_MissingBudgetItems_inSettingDict =[] #If items in the proposal are not in the translating dict, record them to this list

#dict_Budgets_Report = {} 

#dict_ActualCost_Report = {}

dict_Comparison_report = {}



def BudgetCost_setting(filename:str):
     
     with open(filename,'r') as fd:
          for line in fd:
               line = line.strip()
               
               if not line:
                    continue
               
               line2list = line.split(",")
               
               if line2list[1].strip() =='@':
                    #print("@",line2list[2].strip())
                    list_inhouse_task.append(line2list[2].strip())

               dict_setting_budgetName2standardName[line2list[2].strip()] = line2list[3].strip()
     '''          
     for d in dict_setting_budgetName2standardName:       
         print(d,dict_setting_budgetName2standardName[d])
     print("-----")
     '''    
def ActualCost_setting(filename:str):
     
     with open(filename,'r') as fd:
          for line in fd:
               line = line.strip()
               
               if not line:
                    continue
               
               line2list = line.split(",")
                
               dict_setting_quickbookName2standardName[line2list[1].strip()] = line2list[2].strip()
               
              

def budgetReport_lines2list(lines)-> tuple:
     '''
     This function takes the lines and turns it into a list named list_budgets in the form of
          [('Abatement', 0.0, 0.0, 0.0, '', 'Sub Abatement'),
           ('Rough Carpentry/Framing', 0, 0, 1700.0, 'H', 'Materials'),
           ('Rough Carpentry/Framing', 0, 0, 4200.0, 'H', 'Wage')...]
     Note: (Budget Name, Materials cost, wage cost, Materials cost+ wage cost , In house task/Not, Standard Catergory name)
     '''

     #print("----------------")
     list_MissingBudgetItems_inSettingDict =[] #If items in the proposal are not in the translating dict, record them to this list
     list_budgets = [] # Clean up the list first

     for line in lines:
         littlelist = line.split('\t')
         #print(littlelist)
         
         if len(littlelist) >= 8:
            
             # set the in house tasks with H 
             inhouse_mark = ""
             #print("littlelist[4].strip()",littlelist[4].strip())
             if  littlelist[4].strip() in list_inhouse_task:
                 #"H" means that is for in house task
                 inhouse_mark = "H"

             # Mark the standard catergory to each budget item
             standard_catergory = ""
             """LATER:  IF NOT IN THE DICt, WE NEED A LIST OF THE MISSING CATEGORY """
             if littlelist[4].strip() in dict_setting_budgetName2standardName: #the item in the budget is in the translating dict
                  standard_catergory = dict_setting_budgetName2standardName[littlelist[4].strip()]
             else:
                  list_MissingBudgetItems_inSettingDict.append(littlelist[4].strip())
                  print("Missing:",littlelist[4].strip())
             # Create the tuple for each item
             the_tuple =(littlelist[4].strip(),
                         float(trimDollarMark(littlelist[5])),
                         float(trimDollarMark(littlelist[6])),
                         float(trimDollarMark(littlelist[8])),
                         inhouse_mark,standard_catergory)
             
             list_budgets.append(the_tuple)
     '''         
     for list_budget in list_budgets:        
         if list_budget[4]:
              print(list_budget[0],'\t',list_budget[1],'\t',list_budget[2],'\t',list_budget[3])
     print("-------")
     '''    
     # Split element of the list of in house task item to two elements,  labor cost at one element and materials cost at another element
     for i in range(len(list_budgets) - 1 , 0, -1):
          if list_budgets[i][4] == "H":
               list_budgets.insert( i + 1, (list_budgets[i][0],0,0,list_budgets[i][2],"H","Wage"))
               list_budgets[i] =           (list_budgets[i][0],0,0,list_budgets[i][1],"H","Materials") 

     '''          
     for i in list_budgets:
         if i[4]:
          print(i)
     '''
     return (list_budgets,list_MissingBudgetItems_inSettingDict)



def budgetReport_lines2dict(lines)-> tuple:     
     '''
     '''
     
     tuple_budgets = budgetReport_lines2list(lines)
     
     list_budgets = tuple_budgets[0]
     list_missing = tuple_budgets[1]
     dict_Budgets_Report={}
     #print("list_budgets",list_budgets)
     for list_budget in list_budgets:
          #if list_budget[5] == "Materials":
             #print("Materials key:",list_budget[5],"=",list_budget[3])
          dict_Budgets_Report[list_budget[5]] = dict_Budgets_Report.get(list_budget[5],0.00) + float(list_budget[3])
     #print("dict_Budgets_Report",dict_Budgets_Report)
     return (dict_Budgets_Report, list_missing)    

def actualCostReport_lines2dict(lines)->tuple:
     list_MissingActualCostItems_inSettingDict =[]
     dict_ActualCost_Report = {}
     d_transactions = dict()
     d_transactions = lines2dict(lines)
     #print(d_transactions)

     # Transfer the actyual cost dictionary to the standard dictionary(report)
     for d_transaction in d_transactions:
          """LATER:  IF NOT IN THE DICt, WE NEED A LIST OF THE MISSING CATEGORY """
          if d_transaction in dict_setting_quickbookName2standardName:
               keyofStandard_C = dict_setting_quickbookName2standardName[d_transaction]
               #print("key:",d_transaction,"--->",keyofStandard_C)
               #IIf the amount from the dict_ActualCost_Report[kofStandard_C] = None, dict_ActualCost_Report[kofStandard_C] is set 0
               dict_ActualCost_Report[keyofStandard_C] = dict_ActualCost_Report.get(keyofStandard_C,0.00) + float(d_transactions[d_transaction])
          else:
              list_MissingActualCostItems_inSettingDict.append(d_transaction)
              print("Missing:",d_transaction)
     
     #print("dict_ActualCost_Report",dict_ActualCost_Report)
     return (dict_ActualCost_Report,list_MissingActualCostItems_inSettingDict)
     

if __name__ == '__main__':
    import doctest
    doctest.testmod()

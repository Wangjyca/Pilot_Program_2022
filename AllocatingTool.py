"""
Copyright by Hugo and Jingyu Wang 9.30.2022 

"""
import csv
from SumTool import text2lines, lines2dict, trimDollarMark


list_inhouse_task = [] #Designated which task is in house job
list_budgets = [] #list for the budget
dict_budgetName2standardName = {}
dict_quickbookName2standardName  ={}

def BudgetCost_setting(filename:str):
     
     with open(filename,'r') as fd:
          for line in fd:
               line = line.strip()
               
               if not line:
                    continue
               
               line2list = line.split(",")
               
               if line2list[1] =='@':
                    list_inhouse_task.append(line2list[2].strip())

               dict_budgetName2standardName[line2list[2]] = line2list[3]
               
          print(list_inhouse_task)
          #print(dict_budgetName2standardName)
          
def ActualCost_setting(filename:str):
     
     with open(filename,'r') as fd:
          for line in fd:
               line = line.strip()
               
               if not line:
                    continue
               
               line2list = line.split(",")
               #print(line2list)
               dict_quickbookName2standardName[line2list[1]] = line2list[2]
               
               #print(dict_quickbookName2standardName)

def budgetReport_lines2dictwithTuples(lines):
   
     """This function takes the lines and turns it into dictionary with materials and labor cost budget"""
     print("----------------")
     list_budgets = [] # Clean up the list first
     #sortedlines =  sorted(lines)
     #print(lines)
     #print("Above from lines2dictwithTuples")
     
     #inhouse_task_list = inhouse_tasks_setting_list_from_file("InHouseCatergory.txt")
     #print(list_inhouse_task)
     for line in lines:
         littlelist = line.split('\t')
         #print(littlelist)
         if len(littlelist) >= 9:
             #print(len(littlelist),littlelist[4],littlelist[5],littlelist[6],littlelist[8])
             # set the in house task with H
             inhouse_mark = ""
             if  littlelist[4].strip() in list_inhouse_task:
                 #"H" means that is for in house task
                 inhouse_mark = "H"

             the_tuple =(littlelist[4].strip(),
                         float(trimDollarMark(littlelist[5])),
                         float(trimDollarMark(littlelist[6])),
                         float(trimDollarMark(littlelist[9])),
                         inhouse_mark)
             print(the_tuple)
             list_budgets.append(the_tuple)
     #print(list_budgets)

     #set the labor cost & materials const for in house tasks
     for list_budget in list_budgets:
          if list_budget[4] == 'H':
              print (list_budget[0],list_budget[1])
     labor_cost = sum(list_budget[1] for list_budget in list_budgets if list_budget[4] == 'H')
     print(labor_cost)




if __name__ == '__main__':
    import doctest
    doctest.testmod()

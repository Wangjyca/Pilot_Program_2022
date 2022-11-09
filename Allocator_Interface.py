from tkinter import *

#import Tools
from SumTool import text2lines, lines2dict, trimDollarMark

from AllocatingTool import budgetCost_setting, actualCost_setting ,\
                           budgetReport_lines2list, \
                           actualCostReport_lines2dict,\
                           budgetReport_lines2dict,\
                           comparison_report_2strings2dict

#read data from the clipboard   
def getDatafromClipboard():
    result = root.selection_get(selection = "CLIPBOARD")
    root.clipboard_clear()
    return result

#send data to the clipboard
def copyDatatoClipboard(result):
    root.clipboard_clear()
    root.clipboard_append(result)
    
def Calculation1():
    """
    To take action for user by clicking the button of "Budget Input", follow below steps after the set up:
    1) Gets the block of text from the Clipboard of the operation system by calling result = getDatafromClipboard()
    2) Parses the text block to a list names lines by calling lines = text2lines(result)
    3) Displays the list of lines at the bottom of the budget datawindow (budget_text_disp) to let the user know thr raw data imported
    4) Sends the list(lines) to the function of budgetReport_lines2dict(lines) then get a Tuple return. The Tuple contains (dictionary,list)
       a) The dictionary (named budget_dict) is the report of the budget with the Standard Categories (See Graph 5 at page 9 of the proposal for the meaning of hte Standard Category)
       b) The list (named missing list) conaints the categories from the budget data are not in the setting translating dictionary. See the discription of function budgetCost_setting(filename:str)
       c) If the missing list is not empty, displays its content to the budget datawindow to let the user maintain the translating dictionary.
       f) Displays the budget report to the budget datawindow 
    5) Stores the budget report as a string in the storage datawindow (budget_text_report) for the further usage
    6) Sends the string of the budget report back to the Clipboard by calling copy_budget_report2Clipboard()
    """

    #Set up below --------
    budget_text_disp.delete("1.0","end")
    budget_text_report.delete("1.0","end")
    budget_amount_label.config(text = "0.00")
    comparison_text_disp.delete("1.0","end")
    if budgetCost_setting("Setting_BudgetCost.csv") != True: # To get the translating dictionary
       budget_text_disp.insert("1.0", "File Setting_BudgetCost.csv" + '\n' + "is not at the same folder of the program"  + '\n') 
       return
    #Set up above--------
    
    result = getDatafromClipboard() # To get the data from the clipborad in where the user copy the gross data
    
    if not result:
        budget_text_disp.insert("end","Nothing I can do for the budget data!")
        return -1

    # each transaction in list [major1 \t amount1, major2 \t amount2, ...]
    lines = text2lines(result)
    for line in lines:
           budget_text_disp.insert("end",line + '\n')
    
    budget_tuple= budgetReport_lines2dict(lines)
    budget_dict = budget_tuple[0]
    budget_missing_list = budget_tuple[1]
    budget_text_disp.insert("1.0", "-"*20 + '\n')

    if budget_missing_list:
        for budget_missing in budget_missing_list:
            if budget_missing:
                budget_text_disp.insert("1.0",  budget_missing  + '\n')
        budget_text_disp.insert("1.0", "Missing:"  + '\n')

    budget_text_disp.insert("1.0", "-" * 20 + '\n')
    budget_text_disp.insert("1.0", "Note: (S) means Sub Contractor" + '\n')
    budget_text_disp.insert("1.0", "-" * 20 + '\n')

    
    for budget_d in sorted(budget_dict.keys()):
        if budget_dict[budget_d]:
            budget_text_disp.insert("1.0", budget_d + "\t " + "${:0,.2f}".format(round(budget_dict[budget_d]),2) + '\n')
            budget_text_report.insert("1.0", budget_d + "\t " + "${:0,.2f}".format(budget_dict[budget_d]) + '\n')
    

    val = sum(budget_dict[budget_d] for budget_d in budget_dict)
    budget_amount_label.config(text = "${:0,.2f}".format(round(val,2)))
    

    copy_budget_report2Clipboard()

def copy_budget_report2Clipboard():
    """
    Sends the string of the budget report back to the Clipboard. Then the users can plaste the report anywhere they can
    """
    copyDatatoClipboard(budget_text_report.get("1.0", "end")  +"____"+"\t"+ budget_amount_label["text"] + "\n" )


def Calculation2():
    """
    To take action for user by clicking the button of "Actual Cost Input", follow below steps after the set up:
    1) Gets the block of text from the Clipboard of the operation system by calling result = getDatafromClipboard()
    2) Parses the text block to a list names lines by calling lines = text2lines(result)
    3) Displays the list of lines at the bottom of the actual cost datawindow (actualcost_text_disp) to let the user know thr raw data imported
    4) Sends the list(lines) to the function of actualCostReport_lines2dict(lines) then get a Tuple return. The Tuple contains (dictionary,list)
       a) The dictionary (named actualcost_dict) is the report of the budget by the Standard Categories (See Graph 6 at page 10 of the proposal for the meaning of hte Standard Category)
       b) The list (named missing list) conaints the categories from the actual cost data are not in the setting translating dictionary. See the discription of function actualCost_setting(filename:str):
       c) If the missing list is not empty, displays its content to the actual cost datawindow to let the user maintain the translating dictionary.
       f) Displays the actual cost report to the actual cost datawindow 
    5) Stores the actual cost report as a string in the storage datawindow (actualcost_text_report) for the further usage
    6) Sends the string of the budget report back to the Clipboard by calling copy_actualcost_report2Clipboard()
    """

    #Set uP below --------
    
    actualcost_text_disp.delete("1.0","end")
    actualcost_text_report.delete("1.0","end")
    actualcost_amount_label.config(text = "0.00")
    comparison_text_disp.delete("1.0","end")
    
    if actualCost_setting("Setting_ActualCost.csv") != True: # To get the translating dictionary
       actualcost_text_disp.insert("1.0", "File Setting_ActualCost.csv" + '\n' + "is not at the same folder of the program"  + '\n') 
    return
    
    #Set up above--------

    result = getDatafromClipboard()  # To get the data from the clipborad in where the user copy the gross data
    
    if not result:
        actualcost_text_disp.insert("end","Nothing I can do for the actual data!" + '\n')
        return -1

    lines = text2lines(result)
    for line in lines:
           actualcost_text_disp.insert("end",line + '\n')

    actualcost_tuple = actualCostReport_lines2dict(lines)
    actualcost_dict = actualcost_tuple[0]
    actualcost_missing_list = actualcost_tuple[1]
    
    actualcost_text_disp.insert("1.0", "-" * 20 + '\n')
    
    if actualcost_missing_list:
        for actualcost_missing in actualcost_missing_list:
            if actualcost_missing:
                actualcost_text_disp.insert("1.0", actualcost_missing  + '\n')
        actualcost_text_disp.insert("1.0", "Missing:" + '\n')

    actualcost_text_disp.insert("1.0", "-" * 20 + '\n')
    actualcost_text_disp.insert("1.0", "Note: (S) means Sub Contractor" + '\n')
    actualcost_text_disp.insert("1.0", "-" * 20 + '\n')

    
    
    for actualcost_d in sorted(actualcost_dict.keys()):
        if actualcost_dict[actualcost_d]:
            actualcost_text_disp.insert("1.0", actualcost_d + "\t " + "${:0,.2f}".format(round(actualcost_dict[actualcost_d],2)) + '\n')
            actualcost_text_report.insert("1.0", actualcost_d + "\t " + "${:0,.2f}".format(round(actualcost_dict[actualcost_d],2)) + '\n')

    val = sum(actualcost_dict[actualcost_d] for actualcost_d in actualcost_dict)
    actualcost_amount_label.config(text="${:0,.2f}".format(round(val,2)))
    

    copy_actualcost_report2Clipboard()
   
def copy_actualcost_report2Clipboard():
    """
    Sends the string of the actual cost report back to the Clipboard. Then the users can plaste the report anywhere they can
    """
    copyDatatoClipboard(actualcost_text_report.get("1.0", "end")  +"____"+"\t"+ actualcost_amount_label["text"] + "\n" )


def Calculation3():
    """
    To take action for user by clicking the button of "Comparing", follow below steps after the set up:
    1) Gets the two strings of text from datawindows of budget_text_report and actualcost_text_report at where the data was stored by Calculation1() and Calculation2()
    2) Sends the two strings to function  comparison_report_2strings2dict(budget_report_string, actualcost_report_string) to get the comparsion report
    3) Displays the comparsion report to the datawindow (comparison_text_disp)
    4) Set the labels of "REPORTED" to the top of budget datawindow and actual cost datawindoe to let the user know that the two report were useded
    5) Sends the string of the comparsion report back to the Clipboard by calling copy_comparison_report2Clipboard()
    """
    
    #Set up below --------
    comparison_report_dict ={}
    comparison_text_disp.delete("1.0","end")
    comparison_amount_label.config(text = "0.00")
    #Set up above --------
    
    
    budget_report_string = budget_text_report.get("1.0", "end")
    actualcost_report_string = actualcost_text_report.get("1.0", "end")
    comparison_report_dict = comparison_report_2strings2dict(budget_report_string, actualcost_report_string)

    if comparison_report_dict:
        
        profit = 0.00
        
        for item in sorted(comparison_report_dict.keys()):
            if item:
                comparison_text_disp.insert("1.0", item +"\t"+ "${:0,.2f}".format(round(comparison_report_dict[item][0],2))+"\t"\
                                                             + "${:0,.2f}".format(round(comparison_report_dict[item][1],2))+"\t"\
                                                             + "${:0,.2f}".format(round(comparison_report_dict[item][2],2))+"\n")
                profit = profit + comparison_report_dict[item][2] 
                                    
        comparison_text_disp.insert("1.0", "Category"+"\t"+"Budget" +"\t"+ "Actual Cost" +"\t"+ "P/L" + "\n")
        comparison_amount_label.config(text = "${:0,.2f}".format(round(profit,2)))

        budget_text_disp.insert("1.0", "REPORTED"+"-" * 20 + '\n')
        actualcost_text_disp.insert("1.0", "REPORTED"+"-" * 20 + '\n')

        comparison_text_disp.insert("end", "-" * 20 + '\n')
        comparison_text_disp.insert("end", "Note: (S) means Sub Contractor" + '\n')
        
        
        copy_comparison_report2Clipboard()
        

def copy_comparison_report2Clipboard():
    """
    Sends the string of the comparionreport back to the Clipboard. Then the users can plaste the report anywhere they can
    """
    copyDatatoClipboard(comparison_text_disp.get("1.0", "end")  +"____"+"\t"+"____" +"\t"+ "____" +"\t"+ comparison_amount_label["text"] + "\n" )

root = Tk()
root.title("Allocator")
root.iconbitmap()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

widthofroot = 1180 # interface width
heightofroot = 800 # interface height

# set the window at the center of the screen
x_coordinate = (screen_width - widthofroot) / 2
y_coordinate = (screen_height - heightofroot)/2

root.geometry("%dx%d+%d+%d" % (widthofroot,heightofroot,x_coordinate,y_coordinate))
fontsizeDW = 12
fontsize = 10
window_height = int(heightofroot *(1/2.3) / 10 )
inputwin_width = int( widthofroot  / 3 /10)
reportwin_width = int( widthofroot / 2.6 /10)

button_width = 15


#Yview Function
def multiple_yview(*args):
    budget_text_disp.yview(*args)
    actualcost_text_disp.yview(*args)
    comparison_text_disp.yview(*args)

def multiple_xview(*args):
    budget_text_disp.xview(*args)
    actualcost_text_disp.xview(*args)
    comparison_text_disp.xview(*args)

#Frame
the_frame = Frame(root)
the_frame.pack(fill="both", expand=True, padx=20, pady=20)


#Create scrollbar
text_scroll_vertical = Scrollbar(the_frame,  width = 30)
text_scroll_vertical.grid(row = 1, column= 3, sticky ="ns")

text_scroll_horizontal = Scrollbar(the_frame,orient="horizontal", width = 30)
text_scroll_horizontal.grid(row = 2 , column= 0, columnspan = 3, sticky = "EW" )




# Create text boxes set for budget
budget_text_label = Label(the_frame, text="Budget", font=("Helvetica",fontsize))
budget_text_label.grid(row=0, column=0)

# Budget report datawindow for displaying data
budget_text_disp = Text(the_frame, width=inputwin_width, height=window_height , font=("Helvetica",fontsizeDW), yscrollcommand=text_scroll_vertical.set, xscrollcommand=text_scroll_horizontal.set,wrap="none")
budget_text_disp.grid(row = 1, column= 0)

budget_amount_label = Label(the_frame, text="0.00", font=("Helvetica",fontsize))
budget_amount_label.grid(row = 3, column= 0, sticky = "W")

budget_button = Button(the_frame,text="Budget Input", command=Calculation1,width = button_width,font=("Helvetica",fontsize))
budget_button.grid(row = 4, column= 0)

budget_copy_button = Button(the_frame,text="Copy", command=copy_budget_report2Clipboard,width = button_width,font=("Helvetica",fontsize) )
budget_copy_button.grid(row = 5, column= 0)

# Invisiable budget report datawindow for temporary storage when the comparion repost needed
budget_text_report = Text(the_frame, width=0, height=0,wrap="none")




# Create text boxes set for actual cost
actualcost_text_label = Label(the_frame, text="Actual Cost", font=("Helvetica",fontsize))
actualcost_text_label.grid(row = 0, column= 1)

# Actual cost datawindow for displaying data
actualcost_text_disp = Text(the_frame, width=inputwin_width, height=window_height , font=("Helvetica",fontsizeDW), yscrollcommand=text_scroll_vertical.set, xscrollcommand=text_scroll_horizontal.set,wrap="none")
actualcost_text_disp.grid(row = 1, column= 1)

actualcost_amount_label = Label(the_frame, text="0.00", font=("Helvetica",fontsize))
actualcost_amount_label.grid(row = 3, column=1 , sticky = "W")

actualcost_button = Button(the_frame,text="Actual Cost Input", command=Calculation2,width = button_width,font=("Helvetica",fontsize))
actualcost_button.grid(row = 4, column= 1)

actualcost_copy_button = Button(the_frame,text="Copy", command=copy_actualcost_report2Clipboard,width = button_width,font=("Helvetica",fontsize))
actualcost_copy_button.grid(row = 5, column= 1)

# Invisiable actual report datawindow for temporary storage when the comparion repost needed
actualcost_text_report = Text(the_frame, width=0, height=0,wrap="none")






# Create text boxes set for comparison report
comparison_text_label = Label(the_frame, text="Comparison Report", font=("Helvetica",fontsize))
comparison_text_label.grid(row = 0, column= 2)

# Comparing report datawindow for displaying data
comparison_text_disp = Text(the_frame, width=reportwin_width, height=window_height , font=("Helvetica",fontsizeDW), yscrollcommand=text_scroll_vertical.set,xscrollcommand=text_scroll_horizontal.set, wrap="none")
comparison_text_disp.grid(row = 1, column= 2)

comparison_amount_label = Label(the_frame, text="0.00", font=("Helvetica",fontsize))
comparison_amount_label.grid(row = 3, column= 2, sticky = "W")

comparison_button = Button(the_frame,text="Comparing", command=Calculation3,width = button_width,font=("Helvetica",fontsize))
comparison_button.grid(row = 4, column= 2)

comparison_copy_button = Button(the_frame,text="Copy", command=copy_comparison_report2Clipboard,width = button_width,font=("Helvetica",fontsize))
comparison_copy_button.grid(row = 5, column= 2)



# Configure Scrollbar
text_scroll_vertical.config(command=multiple_yview)
text_scroll_horizontal.config(command=multiple_xview)



root.mainloop()

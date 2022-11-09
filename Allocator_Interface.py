from tkinter import *
#import Tools
from SumTool import text2lines, lines2dict, trimDollarMark

from AllocatingTool import BudgetCost_setting,ActualCost_setting ,\
                           budgetReport_lines2list, \
                           actualCostReport_lines2dict,\
                           budgetReport_lines2dict

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
    BudgetCost_setting("Setting_BudgetCost.csv")
    budget_text_disp.delete("1.0","end")
    budget_text_report.delete("1.0","end")
    budget_amount_label.config(text = "0.00")
    comparison_text_disp.delete("1.0","end")

    #budget_text_disp.insert(END,l)
    result = getDatafromClipboard() # To get the data from the clipborad in where the user copy the gross data
    #print(repr(result))
    if not result:
        budget_text_disp.insert("end","Nothing I can do for the budget data!")
        print("Nothing I can do for the budget data!")
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
    for budget_d in sorted(budget_dict.keys()):
        if budget_dict[budget_d]:
            print(budget_d,"\t ",budget_dict[budget_d])
            budget_text_disp.insert("1.0", budget_d + "\t " + str(budget_dict[budget_d]) + '\n')
            budget_text_report.insert("1.0", budget_d + "\t " + str(budget_dict[budget_d]) + '\n')
    #print("budget_dict",budget_dict)


    val = sum(budget_dict[budget_d] for budget_d in budget_dict)
    budget_amount_label.config(text = str(val))
    print(val)

    copy_budget_report2Clipboard()

def copy_budget_report2Clipboard():
    copyDatatoClipboard(budget_text_report.get("1.0", "end")  +"____"+"\t"+ budget_amount_label["text"] + "\n" )


def Calculation2():

    ActualCost_setting("Setting_ActualCost.csv")
    actualcost_text_disp.delete("1.0","end")
    actualcost_text_report.delete("1.0","end")
    actualcost_amount_label.config(text = "0.00")
    comparison_text_disp.delete("1.0","end")

    result = getDatafromClipboard()  # To get the data from the clipborad in where the user copy the gross data
    # print(repr(result))
    if not result:
        print("Nothing I can do for the actual data!")
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
    
    for actualcost_d in sorted(actualcost_dict.keys()):
        if actualcost_dict[actualcost_d]:
            print(actualcost_d,"\t ",actualcost_dict[actualcost_d])
            actualcost_text_disp.insert("1.0", actualcost_d + "\t " + str(actualcost_dict[actualcost_d]) + '\n')
            actualcost_text_report.insert("1.0", actualcost_d + "\t " + str(actualcost_dict[actualcost_d]) + '\n')

    val = sum(actualcost_dict[actualcost_d] for actualcost_d in actualcost_dict)
    actualcost_amount_label.config(text=str(val))
    print(val)

    copy_actualcost_report2Clipboard()
   
def copy_actualcost_report2Clipboard():
    copyDatatoClipboard(actualcost_text_report.get("1.0", "end")  +"____"+"\t"+ actualcost_amount_label["text"] + "\n" )


def Calculation3():

    comparison_report_dict ={}
    comparison_text_disp.delete("1.0","end")
    comparison_amount_label.config(text = "0.00")
    
    budget_report_string = budget_text_report.get("1.0", "end")
    actualcost_report_string = actualcost_text_report.get("1.0", "end")

    lines = text2lines(budget_report_string)
    budget_report_dict = lines2dict(lines)

    lines = text2lines(actualcost_report_string)
    actualcost_report_dict = lines2dict(lines)

    
  
    key_list_budget = [d for d in budget_report_dict]
    key_list_actualcost = [d for d in actualcost_report_dict ]
    key_set = set(key_list_budget + key_list_actualcost)
    
    for key in key_set:
        if key:
            comparison_report_dict[key] = (budget_report_dict.get(key,0.00),\
                                           actualcost_report_dict.get(key,0.00),\
                                           budget_report_dict.get(key,0.00)- actualcost_report_dict.get(key,0.00))

    print(comparison_report_dict)
    if comparison_report_dict:
        
        profit = 0.00
        
        for item in sorted(comparison_report_dict.keys()):
            if item:
                comparison_text_disp.insert("1.0", item +"\t"+ str(round(comparison_report_dict[item][0],2))+"\t"\
                                                             + str(round(comparison_report_dict[item][1],2))+"\t"\
                                                             + str(round(comparison_report_dict[item][2],2))+"\n")
                profit = profit + comparison_report_dict[item][2] 
                                    
        comparison_text_disp.insert("1.0", "Category"+"\t"+"Budget" +"\t"+ "Actual Cost" +"\t"+ "P/L" + "\n")
        comparison_amount_label.config(text = str(round(profit,2)))

        budget_text_disp.insert("1.0", "REPORTED"+"-" * 20 + '\n')
        actualcost_text_disp.insert("1.0", "REPORTED"+"-" * 20 + '\n')
        
        copy_comparison_report2Clipboard()
        

def copy_comparison_report2Clipboard():
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
inputwin_width =int( widthofroot  / 3 /10)
reportwin_width =int( widthofroot / 2.6 /10)

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
budget_text_disp = Text(the_frame, width=inputwin_width, height=window_height , font=("Helvetica",fontsizeDW), yscrollcommand=text_scroll_vertical.set, xscrollcommand=text_scroll_horizontal.set,wrap="none")
budget_text_disp.grid(row = 1, column= 0)
budget_amount_label = Label(the_frame, text="0.00", font=("Helvetica",fontsize))
budget_amount_label.grid(row = 3, column= 0, sticky = "W")
budget_button = Button(the_frame,text="Budget Input", command=Calculation1,width = button_width,font=("Helvetica",fontsize))
budget_button.grid(row = 4, column= 0)
budget_clean_button = Button(the_frame,text="Copy", command=copy_budget_report2Clipboard,width = button_width,font=("Helvetica",fontsize) )
budget_clean_button.grid(row = 5, column= 0)

budget_text_report = Text(the_frame, width=0, height=0,wrap="none")



# Create text boxes set for actual cost
actualcost_text_label = Label(the_frame, text="Actual Cost", font=("Helvetica",fontsize))
actualcost_text_label.grid(row = 0, column= 1)
actualcost_text_disp = Text(the_frame, width=inputwin_width, height=window_height , font=("Helvetica",fontsizeDW), yscrollcommand=text_scroll_vertical.set, xscrollcommand=text_scroll_horizontal.set,wrap="none")
actualcost_text_disp.grid(row = 1, column= 1)
actualcost_amount_label = Label(the_frame, text="0.00", font=("Helvetica",fontsize))
actualcost_amount_label.grid(row = 3, column=1 , sticky = "W")
actualcost_button = Button(the_frame,text="Actual Cost Input", command=Calculation2,width = button_width,font=("Helvetica",fontsize))
actualcost_button.grid(row = 4, column= 1)
actualcost_clean_button = Button(the_frame,text="Copy", command=copy_actualcost_report2Clipboard,width = button_width,font=("Helvetica",fontsize))
actualcost_clean_button.grid(row = 5, column= 1)

actualcost_text_report = Text(the_frame, width=0, height=0,wrap="none")

# Create text boxes set for comparison report
comparison_text_label = Label(the_frame, text="Comparison Report", font=("Helvetica",fontsize))
comparison_text_label.grid(row = 0, column= 2)
comparison_text_disp = Text(the_frame, width=reportwin_width, height=window_height , font=("Helvetica",fontsizeDW), yscrollcommand=text_scroll_vertical.set,xscrollcommand=text_scroll_horizontal.set, wrap="none")
comparison_text_disp.grid(row = 1, column= 2)
comparison_amount_label = Label(the_frame, text="0.00", font=("Helvetica",fontsize))
comparison_amount_label.grid(row = 3, column= 2, sticky = "W")
comparison_button = Button(the_frame,text="Comparing", command=Calculation3,width = button_width,font=("Helvetica",fontsize))
comparison_button.grid(row = 4, column= 2)
comparison_clean_button = Button(the_frame,text="Copy", command=copy_comparison_report2Clipboard,width = button_width,font=("Helvetica",fontsize))
comparison_clean_button.grid(row = 5, column= 2)



# Configure Scrollbar
text_scroll_vertical.config(command=multiple_yview)
text_scroll_horizontal.config(command=multiple_xview)



root.mainloop()

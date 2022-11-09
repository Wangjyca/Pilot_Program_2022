from tkinter import *
#import Tools
from SumTool import text2lines, lines2dict, trimDollarMark

from AllocatingTool import BudgetCost_setting,ActualCost_setting ,\
                           budgetReport_lines2list, \
                           actualCostReport_lines2dict,\
                           budgetReport_lines2dict


l = ["sdfds","dfsdfds","dfdasa","werwf","sdfds","dfsdfds","dfdasa","werwf","sdfds","dfsdfds","dfdasa","werwf"]
root = Tk()
root.title("Allocator")
root.iconbitmap()
root.geometry("1180x800")

#Yview Function
def multiple_yview(*args):
    budget_text_disp.yview(*args)
    actualcost_text_disp.yview(*args)
    comparison_text_disp.yview(*args)

def multiple_xview(*args):
    budget_text_disp.xview(*args)
    actualcost_text_disp.xview(*args)
    comparison_text_disp.xview(*args)

    
    
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

    #budget_text_disp.insert(END,l)
    result = getDatafromClipboard() # To get the data from the clipborad in where the user copy the gross data
    #print(repr(result))
    if not result:
        print("Nothing I can do for the budget data!")
        return -1


    # each transaction in list [major1 \t amount1, major2 \t amount2, ...]
    lines = text2lines(result)
    for line in lines:
           print(line)
           budget_text_disp.insert("end",line + '\n')
    
    # statistic dictionary { major1: total_amount1, major2: total_amount2, ...  }
    #d_transactions = dict()
    #d_transactions = lines2dict(lines)
 
    ''' Testing '''
    #budgetReport_lines2list(lines)
    budget_tuple= budgetReport_lines2dict(lines)
    budget_dict = budget_tuple[0]
    budget_missing_list = budget_tuple[1]
    budget_text_disp.insert("1.0", "-"*20 + '\n')
    for budget_missing in budget_missing_list:
        if budget_missing:
            budget_text_disp.insert("1.0", "Missing:" + budget_missing  + '\n')

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
    

    #return budget_dict


def Calculation2():

    ActualCost_setting("Setting_ActualCost.csv")
    actualcost_text_disp.delete("1.0","end")
    actualcost_text_report.delete("1.0","end")
    actualcost_amount_label.config(text = "0.00")

    result = getDatafromClipboard()  # To get the data from the clipborad in where the user copy the gross data
    # print(repr(result))
    if not result:
        print("Nothing I can do for the actual data!")
        return -1

    lines = text2lines(result)
    for line in lines:
           actualcost_text_disp.insert("end",line + '\n')

    actualcost_tuple = actualCostReport_lines2dict(lines)
    actualcost_dict = actualcost_tuple[0]
    actualcost_missing_list = actualcost_tuple[1]
    actualcost_text_disp.insert("1.0", "-" * 20 + '\n')
    for actualcost_missing in actualcost_missing_list:
        if actualcost_missing:
            actualcost_text_disp.insert("1.0", "Missing:" + actualcost_missing  + '\n')

    actualcost_text_disp.insert("1.0", "-" * 20 + '\n')
    for actualcost_d in sorted(actualcost_dict.keys()):
        if actualcost_dict[actualcost_d]:
            print(actualcost_d,"\t ",actualcost_dict[actualcost_d])
            actualcost_text_disp.insert("1.0", actualcost_d + "\t " + str(actualcost_dict[actualcost_d]) + '\n')
            actualcost_text_report.insert("1.0", actualcost_d + "\t " + str(actualcost_dict[actualcost_d]) + '\n')

    val = sum(actualcost_dict[actualcost_d] for actualcost_d in actualcost_dict)
    actualcost_amount_label.config(text=str(val))
    print(val)

    #return actualcost_dict


def Calculation3():

    comparison_text_disp.delete("1.0","end")
    comparison_amount_label.config(text = "0.00")

    budget_report_string = budget_text_report.get("1.0", "end")
    actualcost_report_string = actualcost_text_report.get("1.0", "end")

    lines = text2lines(budget_report_string)
    budget_report_dict = lines2dict(lines)

    lines = text2lines(actualcost_report_string)
    actualcost_report_dict = lines2dict(lines)

    for d in budget_report_dict:
        comparison_text_disp.insert("1.0", d +":"+ str(budget_report_dict[d]) + "\n")

    comparison_text_disp.insert("1.0","-"*20)

    for d in actualcost_report_dict:
        comparison_text_disp.insert("1.0", d +":"+ str(actualcost_report_dict[d]) + "\n")

    #comparison_text_disp.insert("1.0",budget_report_string)
    #comparison_text_disp.insert("1.0",actualcost_report_string )



# --- create canvas with scrollbar ---
#canvas = tk.Canvas(root)
#canvas.pack(pady=10)

#Frame
the_frame = Frame(root)
the_frame.pack(fill="both", expand=True, padx=20, pady=10)

fontsize = 14
window_height = 28
inputwin_width = 25
reportwin_width = 50

#Create scrollbar
text_scroll_vertical = Scrollbar(the_frame,  width = 30)
text_scroll_vertical.grid(row = 1, column= 3, sticky ="ns")

text_scroll_horizontal = Scrollbar(the_frame,orient="horizontal", width = 30)
text_scroll_horizontal.grid(row = 2 , column= 0, columnspan = 3, sticky = "EW" )




# Create text boxes set for budget
budget_text_label = Label(the_frame, text="Budget", font=("Helvetica",fontsize))
budget_text_label.grid(row=0, column=0)
budget_text_disp = Text(the_frame, width=inputwin_width, height=window_height , font=("Helvetica",fontsize), yscrollcommand=text_scroll_vertical.set, xscrollcommand=text_scroll_horizontal.set,wrap="none")
budget_text_disp.grid(row = 1, column= 0)
budget_amount_label = Label(the_frame, text="0.00", font=("Helvetica",fontsize))
budget_amount_label.grid(row = 3, column= 0)
budget_button = Button(the_frame,text="Budget Input", command=Calculation1)
budget_button.grid(row = 4, column= 0)
budget_clean_button = Button(the_frame,text="Clean", command=Calculation1)
budget_clean_button.grid(row = 5, column= 0)

budget_text_report = Text(the_frame, width=0, height=0,wrap="none")

#budget_text_report.insert(END,l)

# Create text boxes set for actual cost
actualcost_text_label = Label(the_frame, text="Actual Cost", font=("Helvetica",fontsize))
actualcost_text_label.grid(row = 0, column= 1)
actualcost_text_disp = Text(the_frame, width=inputwin_width, height=window_height , font=("Helvetica",fontsize), yscrollcommand=text_scroll_vertical.set, xscrollcommand=text_scroll_horizontal.set,wrap="none")
actualcost_text_disp.grid(row = 1, column= 1)
actualcost_amount_label = Label(the_frame, text="0.00", font=("Helvetica",fontsize))
actualcost_amount_label.grid(row = 3, column= 1)
actualcost_button = Button(the_frame,text="Actual Cost Input", command=Calculation2)
actualcost_button.grid(row = 4, column= 1)
actualcost_clean_button = Button(the_frame,text="Clean", command=Calculation2)
actualcost_clean_button.grid(row = 5, column= 1)

actualcost_text_report = Text(the_frame, width=0, height=0,wrap="none")

# Create text boxes set for comparison report
comparison_text_label = Label(the_frame, text="Comparison Report", font=("Helvetica",fontsize))
comparison_text_label.grid(row = 0, column= 2)
comparison_text_disp = Text(the_frame, width=reportwin_width, height=window_height , font=("Helvetica",fontsize), yscrollcommand=text_scroll_vertical.set,xscrollcommand=text_scroll_horizontal.set, wrap="none")
comparison_text_disp.grid(row = 1, column= 2)
comparison_amount_label = Label(the_frame, text="", font=("Helvetica",fontsize))
comparison_amount_label.grid(row = 3, column= 2)
comparison_button = Button(the_frame,text="Comparing", command=Calculation3)
comparison_button.grid(row = 4, column= 2)
comparison_clean_button = Button(the_frame,text="Clean", command=Calculation3)
comparison_clean_button.grid(row = 5, column= 2)



# Configure Scrollbar
text_scroll_vertical.config(command=multiple_yview)
text_scroll_horizontal.config(command=multiple_xview)



root.mainloop()

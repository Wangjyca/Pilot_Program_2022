"""
Copyright by Jingyu Wang & Hugo 3/24/2020

"""

import tkinter as tk
from tkinter import *
from tkinter import ttk


#import Tools
from SumTool import text2lines, lines2dict, trimDollarMark

from AllocatingTool import BudgetCost_setting,ActualCost_setting ,\
                           budgetReport_lines2list, \
                           actualCostReport_lines2dict,\
                           budgetReport_lines2dict

global  budget_dict 
global  actual_dict







# ROOT WINDOW
root = Tk()
root.title("Statistic:")

#root.configure(width = 920, height = 400)
# 920x800+0+0 The first 0 is for the window's x coordinate of desktop.
# The the second 0 is for the window's y coordinate of desktop.
#root.geometry("920x800+0+0")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

widthofroot = 908 #screen_width * 0.9
heightofroot = 320 #screen_height * 0.2

# set the window at the center of the screen
x_coordinate = (screen_width - widthofroot) / 2
y_coordinate = (screen_height - heightofroot)/2

root.geometry("%dx%d+%d+%d" % (widthofroot,heightofroot,x_coordinate,y_coordinate))



# To sum up treeview window's amount
def sumup_data(tree):
    items = tree.get_children()
    total = 0
    for item in items:
         itmeamount = float(trimDollarMark(tree.item(item)['values'][1]))
         total += itmeamount
    total = round(total,2)
    return total

# When user click the imput data treeview window (left side), the sumup amount is assigned to labelin
def select_itemIn(event):
    #print(event)
    global imput
    global labelin
    global frame
    labelin = Label(frame,text =sumup_data(imput))
    labelin.grid(row = 0, column = 0)
    
# When user click the output data treeview window (right side), the statistic amount is assigned to labelout    
def select_itemOut(event):
    global output
    global labelout
    global frame
    labelout = Label(frame,text =sumup_data(output))
    labelout.grid(row = 0, column = 2)

#read data from the clipboard   
def getDatafromClipboard():
    result = root.selection_get(selection = "CLIPBOARD")
    root.clipboard_clear()
    return result

#send data to the clipboard
def copyDatatoClipboard(result):
    root.clipboard_clear()
    root.clipboard_append(result)
    

    
#before each calculation, this function initializes the widgets of the root window
def cleanup():
    global imput
    global output
    global labelout
    global labelin
    global frame
    
    imput.delete(* imput.get_children())
    output.delete(* output.get_children())

    labelin.grid_forget() 
    labelout.grid_forget() 
    
    labelin = Label(frame,text = "")
    labelin.grid(row = 0, column = 0)
    
    labelout = Label(frame,text ="")
    labelout.grid(row = 0, column = 2)




def Calculation1():   
    result = getDatafromClipboard() # To get the data from the clipborad in where the user copy the gross data
    #print(repr(result))
    if result  == "":
        print("Nothing I can do for the statistic!")
        return -1

    BudgetCost_setting("Setting_BudgetCost.csv")

    cleanup() # Initialize the widgets of the root window
    
    # each transaction in list [major1 \t amount1, major2 \t amount2, ...]
    lines = text2lines(result)
    
    # statistic dictionary { major1: total_amount1, major2: total_amount2, ...  }
    d_transactions = dict()
    d_transactions = lines2dict(lines)
    #print(lines)
    #print(d_transactions)
    
    for line in lines: # To insert data to the imput window 
        l = line.split("\t")
        imput.insert('','end', values=l)

    sumresult = ""
    for d_transaction in d_transactions: # To insert data to the output window and generate the text string for clip
        #print(d_transaction, d_transactions[d_transaction])
        
        sumresult += d_transaction + "\t " + str(d_transactions[d_transaction])+"\n "
        output.insert('','end', values=[d_transaction,d_transactions[d_transaction]])

    select_itemIn("c")
    select_itemOut("c")


    copyDatatoClipboard(sumresult)

    ''' Testing '''
    #budgetReport_lines2list(lines)
    budget_dict = budgetReport_lines2dict(lines)
    for budget_d in sorted(budget_dict.keys()):
        if budget_dict[budget_d]:
            print(budget_d,"\t ",budget_dict[budget_d]) 
    #print("budget_dict",budget_dict)
        
    val = sum(budget_dict[budget_d] for budget_d in budget_dict)
    print(val)
    

    return budget_dict
    

def Calculation2():
    """  see below text formation from clipboard
            2222 Leavenworth St Unit 302	$3,000.00
            2200 Leavenworth St Unit 202	$3,000.00
            2222 Leavenworth St Unit 302	$3,000.00
            2200 Leavenworth St Unit 202	$3,000.00
            2222 Leavenworth St Unit 302	$3,000.00
            2200 Leavenworth St Unit 202	$3,000.00
            2222 Leavenworth St Unit 202	$3,000.00

    """
    
    result = getDatafromClipboard() # To get the data from the clipborad in where the user copy the gross data
    #print(repr(result))
    if result  == "":
        print("Nothing I can do for the statistic!")
        return -1

    cleanup() # Initialize the widgets of the root window
    ActualCost_setting("Setting_ActualCost.csv")
    
    # each transaction in list [major1 \t amount1, major2 \t amount2, ...]
    lines = text2lines(result)
    
    # statistic dictionary { major1: total_amount1, major2: total_amount2, ...  }
    d_transactions = dict()
    d_transactions = lines2dict(lines)
    #print(lines)
    #print(d_transactions)
    
    for line in lines: # To insert data to the imput window 
        l = line.split("\t")
        imput.insert('','end', values=l)

    sumresult = ""
    for d_transaction in d_transactions: # To insert data to the output window and generate the text string for clip
        #print(d_transaction, d_transactions[d_transaction])
        
        sumresult += d_transaction + "\t " + str(d_transactions[d_transaction])+"\n "
        output.insert('','end', values=[d_transaction,d_transactions[d_transaction]])

    select_itemIn("c")
    select_itemOut("c")


    copyDatatoClipboard(sumresult)

    actual_dict = actualCostReport_lines2dict(lines)
    for actual_d in sorted(actual_dict.keys()):
        if actual_dict[actual_d]:
            print(actual_d,"\t ",actual_dict[actual_d])
    val= sum(actual_dict[actual_d] for actual_d in actual_dict)
    print(val)

    return actual_dict


def Comparison():
    if budget_dict and actual_dict:
        print(budget_dict)
        print(actual_dict)
        pass
        

    
    
frame = LabelFrame(root, text = "Tool:", padx = 5, pady=5, height = heightofroot*0.9)
frame.pack(side = tk.LEFT,padx =5, pady=5)



# labelin for the sum amount of the left datawindow for the gross data
labelin=Label(frame)
# labelout for the sum amount of the right datawindow for the statistic date
labelout=Label(frame)
# After user copy two columns (string & digit columns) from a spread sheet
# and user clicks this button, the gross data fill in the left datawindow
actual_dict ={}
budget_dict = {}
def invoke(self):
    """Invoke the command associated with the button.
    The return value is the return value from the command,
    or an empty string if there is no command associated with
    the button. This command is ignored if the button's state
    is disabled.
    """
    return self.tk.call(self._w, 'invoke')

b1 = Button(frame, text = "Budget", command =  Calculation1) 
actual_dict = b1.invoke()
print("actual_dict",actual_dict)

b2 = Button(frame, text = "Actual Cost", command = Calculation2 )
b3 = Button(frame, text = "Comparing", command = Comparison )

labelin.grid(row = 0, column = 0)
b1.grid(row = 3, column = 0)
b2.grid(row = 3, column = 2)
b3.grid(row = 3, column = 3)


labelout.grid(row = 0, column = 2)




# the left treeview datawindow
imput = ttk.Treeview(frame, columns=(1,2), show = "headings", height="5")
imput.grid(row = 1, column= 0)

imput.heading(1, text = "Major")
imput.heading(2, text = "Amount")
imput.column(1, stretch = True, anchor = "w")
imput.column(2, stretch = True, anchor = "e")
imput.bind('<ButtonRelease-1>',select_itemIn)

# The horizontal scroll bar x for imput treeview
imputScrollbarX = ttk.Scrollbar(frame, orient="horizontal", command=imput.xview)
imput.configure(xscroll = imputScrollbarX.set)
imputScrollbarX.grid(row = 2, column = 0, sticky ="s")

# The vertical scroll bar y for imput treeview
imputScrollbarY = ttk.Scrollbar(frame, orient="vertical", command=imput.yview)
imput.configure(yscroll = imputScrollbarY.set)
imputScrollbarY.grid(row = 1, column = 1, sticky ="ns")


# the right treeview datawindow
output = ttk.Treeview(frame, columns=(1,2), show = "headings", height="5")
output.grid(row = 1, column= 2,pady=5)

output.heading(1, text = "Major")
output.heading(2, text = "Amount")
output.column(1, stretch = True, anchor = "w")
output.column(2, stretch = True, anchor = "e")
output.bind('<ButtonRelease-1>',select_itemOut)

# The horizontal scroll bar x for output treeview
outputScrollbarX = ttk.Scrollbar(frame, orient="horizontal", command=output.xview)
output.configure(xscroll = outputScrollbarX.set)
outputScrollbarX.grid(row = 2, column = 2, sticky ="s")

# The horizontal scroll bar y for output treeview
outputScrollbarY = ttk.Scrollbar(frame, orient="vertical", command=output.yview)
output.configure(yscroll = outputScrollbarY.set)
outputScrollbarY.grid(row = 1, column = 3, sticky ="ns")





root.mainloop()

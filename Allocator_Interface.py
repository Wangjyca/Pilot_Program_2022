from tkinter import *
l = ["sdfds","dfsdfds","dfdasa","werwf","sdfds","dfsdfds","dfdasa","werwf","sdfds","dfsdfds","dfdasa","werwf"]
root = Tk()
root.title("Allocator")
root.iconbitmap()
root.geometry("900x600")

#Yview Function
def multiple_yview(*args):
    budget_text_disp.yview(*args)
    actualcost_text_disp.yview(*args)
    comparison_text_disp.yview(*args)

def Calculation1():
    budget_text_disp.insert(END,l)


def Calculation2():
    pass

def Calculation3():
    pass

#Frame
the_frame = Frame(root)
the_frame.pack(pady=10)

#Create scrollbar
text_scroll = Scrollbar(the_frame)
text_scroll.grid(row = 1, column= 3, sticky ="ns")

fontsize = 14
window_height = 28
inputwin_width = 25
reportwin_width = 50


# Create text boxes set for budget
budget_text_label = Label(the_frame, text="Budget", font=("Helvetica",fontsize))
budget_text_label.grid(row=0, column=0)
budget_text_disp = Text(the_frame, width=inputwin_width, height=window_height , font=("Helvetica",fontsize), yscrollcommand=text_scroll.set, wrap="none")
budget_text_disp.grid(row = 1, column= 0)
budget_amount_label = Label(the_frame, text="0.00", font=("Helvetica",fontsize))
budget_amount_label.grid(row = 2, column= 0)
budget_button = Button(the_frame,text="Budget Input", command=Calculation1)
budget_button.grid(row = 3, column= 0)
budget_clean_button = Button(the_frame,text="Clean", command=Calculation1)
budget_clean_button.grid(row = 4, column= 0)

# Create text boxes set for actual cost
actualcost_text_label = Label(the_frame, text="Actual Cost", font=("Helvetica",fontsize))
actualcost_text_label.grid(row = 0, column= 1)
actualcost_text_disp = Text(the_frame, width=inputwin_width, height=window_height , font=("Helvetica",fontsize), yscrollcommand=text_scroll.set, wrap="none")
actualcost_text_disp.grid(row = 1, column= 1)
actualcost_amount_label = Label(the_frame, text="0.00", font=("Helvetica",fontsize))
actualcost_amount_label.grid(row = 2, column= 1)
actualcost_button = Button(the_frame,text="Actual Cost Input", command=Calculation1)
actualcost_button.grid(row = 3, column= 1)
actualcost_clean_button = Button(the_frame,text="Clean", command=Calculation1)
actualcost_clean_button.grid(row = 4, column= 1)

# Create text boxes set for comparison report
comparison_text_label = Label(the_frame, text="Comparison Report", font=("Helvetica",fontsize))
comparison_text_label.grid(row = 0, column= 2)
comparison_text_disp = Text(the_frame, width=reportwin_width, height=window_height , font=("Helvetica",fontsize), yscrollcommand=text_scroll.set, wrap="none")
comparison_text_disp.grid(row = 1, column= 2)
comparison_amount_label = Label(the_frame, text="", font=("Helvetica",fontsize))
comparison_amount_label.grid(row = 2, column= 2)
comparison_button = Button(the_frame,text="Comparing", command=Calculation1)
comparison_button.grid(row = 3, column= 2)
comparison_clean_button = Button(the_frame,text="Clean", command=Calculation1)
comparison_clean_button.grid(row = 4, column= 2)



# Configure Scrollbar
text_scroll.config(command=multiple_yview)




root.mainloop()
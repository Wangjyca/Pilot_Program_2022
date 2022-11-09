# Pilot_Program_2022
CCSF Pilot (Honor) Program2022
11/4/2022

To get the backgroud of this code, see Allocator Project Proposal.pdf in the repository

Note:
1) Exsiting code
    a) SumTool.py was writen in 2020 at CCSF class CS131B perform below task:

        Copying Data Block 1 then coverting it to Data Report 

        Data Block 1:                       Data Report:
        a $100                              a 300.00
        b 200                               b 250.00
        c $100.00                           c 1100.00
        a $200
        b $100
        c $1,000.00
        c 
        b $
        b ($50)


    c) Functions prototype for SumTool.py:

       1. text2lines(result:str)->list:
          """ 
          To generate a list for the rows of above Data Block 1
          """

       2. trimDollarMark(str_amount:str)->str:
          """
          To convert:
          $3,000.00 -> 3000.00
          ($50) -> -50
          """

       3. lines2dict(lines:list)->dict:
          """
          To generate a dictionry as above Data Report from ths list of Data Block 1
          """



2) New Code
   a) AllocatingTool.py is new file for this project which contains the functions as below:

      1. BudgetCost_setting(filename:str):
         """
         Reading data from a CSV file (filename) then setting up a dictionary for the budget catergories. See more explaition the pages 7 to 9 at the proposal
         """

      2. ActualCost_setting(filename:str):
         """
         Reading data from a CSV file (filename) then setting up a dictionary for the actual cost catergories. See more explaition the pages 6 to 8 and 10 at the proposal
         """
      3. budgetReport_lines2list(lines):
         """
         As part of the budget input (see page 7 at the proposal), takes the lines and turns it into a list named list_budgets in the form of:
            [('Abatement', 0.0, 0.0, 0.0, '', 'Sub Abatement'),
            ('Rough Carpentry/Framing', 0, 0, 1700.0, 'H', 'Materials'),
            ('Rough Carpentry/Framing', 0, 0, 4200.0, 'H', 'Wage')...]
         Note for the member of the list: (Budget Name, Materials cost, wage cost, Materials cost+ wage cost , In house task/Not, Standard Catergory name)

         For the input, see Graph 2 at page 4 of the proposal. 
         """
      4. budgetReport_dict():
         """
         From the list generated by above function of budgetReport_lines2list(lines), this function creates the Budget Dictionary. See the explanation at page 7 for the budget report which is prepared for the Comparing Chart. 

         For the output, see Column A of Graph 3 at page 5 of the proposal. 
         """

      5. actualCostReport_lines2dict(lines):
         """
         For the actual cost data input and output (see page 6 at the proposal), this function will call the three functions at SumTool.py to prepare the actual cost report.

         For the input, see Graph 1 at page 3 of the proposal. For the output, see Column B of Graph 3 at page 5 of the proposal.
         """
      
      6. Comparing _report():
         """
         This function generate a comparison report as Column C of Graph 3 at page 5 of the proposal
         """  

    b) Allocator_Interface.py
      """
      THis file will implement the interface shown as Graph 4 at page 6 of the proposal
      """
      a. Functions:
         1. getDatafromClipboard():
            """
            When users copy data from a spreadsheet, for example like Data Block 1, this fuction can get the whole block of character string from the Clipboard of the operation system
            """
         2. copyDatatoClipboard(result):
            """
            To send the character string in result to the Clipboard of the operation system
            """

         3. Calculation1():
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
         3. copy_budget_report2Clipboard():
            """
            Sends the string of the budget report back to the Clipboard. Then the users can plaste the report anywhere they can
            """
         4. Calculation2():
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
         5. copy_actualcost_report2Clipboard():
            """
            Sends the string of the actual cost report back to the Clipboard. Then the users can plaste the report anywhere they can
            """

         6. Calculation3():
            """
            To take action for user by clicking the button of "Comparing", follow below steps after the set up:
            1) Gets the two strings of text from datawindows of budget_text_report and actualcost_text_report at where the data was stored by Calculation1() and Calculation2()
            2) Sends the two strings to function  comparison_report_2strings2dict(budget_report_string, actualcost_report_string) to get the comparsion report
            3) Displays the comparsion report to the datawindow (comparison_text_disp)
            4) Set the labels of "REPORTED" to the top of budget datawindow and actual cost datawindoe to let the user know that the two report were useded
            5) Sends the string of the comparsion report back to the Clipboard by calling copy_comparison_report2Clipboard()
            """

         7. copy_comparison_report2Clipboard():
            """
            Sends the string of the comparionreport back to the Clipboard. Then the users can plaste the report anywhere they can
            """

      b. GUI
         1.  budget_text_disp
             """ 
             The widget of a text box for displying the raw data and the report for budget
             """
         2.  budget_text_report 
             """
             Invisiable widget to temporary store the report of the budget 
             """
         3.  actualcost_text_disp
             """ 
             The widget of a text box for displying the raw data and the report for actual  cost
             """         
         4.  actualcost_text_report
             """
             Invisiable widget to temporary store the report of the actual cost
             """         
         5.  comparison_text_disp
             """
             To dispaly to comparing report
             """
         6.  budget_button
             """
             To execute the function of Calculation1()
             """
         7.  budget_copy_button
             """
             To execute the function of copy_budget_report2Clipboard()
             """
         8.  budget_amount_label 
             """
             To display the total sum amount for the budget report
             """
         9.  actualcost_button
             """
             To execute the function of Calculation2()
             """
         10. actualcost_copy_button
             """
             To execute the function of copy_actualcost_report2Clipboard():
             """
         11. actualcost_amount_label
             """
             To display the total sum amount for the actual cost report
             """
         12. comparison_button
             """
             To execute the function of Calculation3()
             """
         13. comparison_copy_button
             """
             To execute the function of copy_comparison_report2Clipboard()
             """
         14. comparison_amount_label
             """
             To display the sum up p&L at the comarison report
             """








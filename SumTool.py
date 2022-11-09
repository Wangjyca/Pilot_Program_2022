"""
Copyright by Hugo and Jingyu Wang 4/2/2020 

"""
"""
list_inhouse_task = []

def inhouse_tasks_setting_list_from_file(filename:str)->dict:
     
     with open(filename,'r') as fd:
          for line in fd:
               line = line.strip()
               if not line:
                    continue
               if line[0] =='@':
                    list_inhouse_task.append(line[1:])
               print(line, "---> ",line[0])
          
          return list_inhouse_task
"""

     
def text2lines(result)->list:
     """Returns a list of lines from Clipboard"""
            
     lines = result.split('\n')
         
     for line in lines:
        if line.strip() == "": # remove the empty rows
             lines.remove(line)

     for index in range(len(lines)):
        lines[index] =  lines[index].strip()                  
  
        if lines[index].find("\t") == -1:
             lines[index] = lines[index] +"\t" #To deal with the rows without money amount

        #lines[index] = lines[index].upper()
        #print(lines[index])
     #lines = lines.sort() 
     #print(lines)
     #print("Above from text2lines")
     return lines
     

def trimDollarMark(str_amount)->str: #$3,000.00 -> 3000.00
    
    str_amount = str(str_amount).strip()
    for mark in ['$',',','(',')']: #We can add '&' ... in the list if we need
        if (mark == '(') and (str_amount.find('(') >= 0):
             str_amount = str_amount.replace(mark,'')
             str_amount = '-' + str_amount
             
        str_amount = str_amount.replace(mark,'')
        #print(str_amount)
        
    if str_amount =="":
        str_amount = "0.0"
    if str_amount =="-":
        str_amount = "0"   
    
    return str_amount


def lines2dict(lines)->dict:
     '''This function takes the lines and turns it into dictionary'''
     
     sortedlines =  sorted(lines)

     dict= {}
     for line in sortedlines:
         littlelist = line.split('\t')
         #print(littlelist)
         #IIf the amount from the dict[littlelist[0]] = None, dict.get(littlelist[0],0.00) set 0
         dict[littlelist[0]] = dict.get(littlelist[0],0.00) + float(trimDollarMark(littlelist[1]))
     return dict 




if __name__ == '__main__':
    import doctest
    doctest.testmod()

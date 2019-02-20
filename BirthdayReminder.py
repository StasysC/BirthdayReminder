import sys
import re
from datetime import datetime

file_name = sys.argv[1]
#file_name = "testdoc.txt"
current_lines_count = 1
name_list = ["name"]
email_list = ["email"]
date_list = ["date"]
indexes_list = []
INPUT_FIELDS = 3
WRONG_FORMAT_MSG = "Incorrect file format. File format should be CSV/JSON/TXT"

#checks if file format is correct
def file_check(file_name):
    if not (file_name.endswith(".txt") or
            file_name.endswith(".json") or
            file_name.endswith(".csv")):        
        print (WRONG_FORMAT_MSG)
        quit()
    return 
#reads and formats file data
def read_file(file_open):
    current_lines_count = 1 
    for line in file_open:
        raw_data_line = raw_data(line)
        data_to_lists(raw_data_line, current_lines_count)
        current_lines_count += 1
    return
#applies data to coresponding list
def data_to_lists (line, current_lines_count):
    if (current_lines_count % INPUT_FIELDS == 1):
        name_list.append(line)        
    elif (current_lines_count % INPUT_FIELDS == 0 ):
        date_list.append(line)
    else:
        email_list.append(line)
    return
#removes all persons whose all info is not valid
def delete_empty_info():
    for index,name in enumerate(name_list):
        if (name == ""):
            delete_data(index)

    for index,email in enumerate(email_list):
        if (email == ""):
            delete_data(index)

    for index,date in enumerate(date_list):
        if (date == ""):
            delete_data(index)
#checks if date format is correct (YYYY-MM-DD or MM-DD)
def validate_date ():
    delete_list = []
    for i in range(1,len(date_list)):
        if not(re.match('^[1-2][0-9]{3}-[0-1][0-9]-[0-9]{2}$',date_list[i])
        or re.match('^[0-1][0-9]-[0-9]{2}$',date_list[i])):
            delete_list.append(i)
    for i in reversed(delete_list):
        delete_data(i)
#calculates how many days left to birthday and add to celebrator's (index_list) list
def days_to_birthday():
    today_date = current_today_date()    
    for index in range(1, len(date_list)):
        current_selected_date = current_date(index)
        if (today_date[0] - current_selected_date[0] == 0):
            if (current_selected_date[1] - today_date[1] <= 7 and
                current_selected_date[1] - today_date[1] >= 0):
                indexes_list.append(index)
#return celebrator's date in useful format
def current_date(index):
    current_date_list = date_list[index].split("-")
    current_date = []
    if(len(current_date_list)>2):
        current_date.append(int(current_date_list[1]))
        current_date.append(int(current_date_list[2]))
    else:
        current_date.append(int(current_date_list[0]))
        current_date.append(int(current_date_list[1]))
    return current_date
#return today's date in string format for email
def current_date_string(current_date):
    month = str(current_date[0])
    day = str(current_date[1])
    date = month + "-" + day
    return date
#return today's date in useful format
def current_today_date():
    current_date = datetime.now()
    current_date_formated = current_date.strftime("%m-%d")
    current_date_list = current_date_formated.split("-")
    current_date_list[0] = int(current_date_list[0])
    current_date_list[1] = int(current_date_list[1])
    return current_date_list
#deletes an invalid data from lists
def delete_data (index):
    del name_list[index]            
    del email_list[index]
    del date_list[index]
#formats file data
def raw_data(data_line):
    line_no_numbers = data_line[1:]
    line_no_numbers = line_no_numbers.strip()
    line_no_dots = line_no_numbers.strip(".")
    raw_data = line_no_dots.rstrip(",")
    raw_data = raw_data.strip() 
    return  raw_data
#sends email for persons
def send_emails():
    for a in indexes_list:
       for i in range(1, len(name_list)):
           if not(a == i):
               name_of_birthday_person = name_list[a]
               date_of_birthday = current_date_string(current_date(a))
               receivers_name = name_list[i]
               print ("Subject: Birthday Reminder: %s's birthday on %s" %(name_of_birthday_person,date_of_birthday) )
               print ("Body:")
               print ("Hi %s," % receivers_name)
               print ("This is a reminder that %s will be celebrating their birthday on %s."
                    % (name_of_birthday_person,date_of_birthday))
#execution part
file_check(file_name)
file_open = open(file_name, "r")
raw_file = read_file(file_open)

delete_empty_info()
validate_date()

days_to_birthday()
send_emails()


   
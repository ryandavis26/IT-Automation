#!/usr/bin/env python3
import csv
import os
import re
import operator
from User import User

'''This program takes a log file and generates a small html report

This report contains the type and number of "ERRORS" in a log file, how many times an
error occurred, sorted from greatest to least 
'''

'''This script can be made more efficient by creating a dict from the user and associating the name with
a User object, this would reduce the amount of time it takes to search for a user to check if they exist in the
user_list function. Right now it has to iterate over the list twice per function call, !!NO GOOD!!'''
#TODO Refactor this user list to a user dict
def read_in_log(file_path):
    '''Reads in a Log File and creates two CSV files
     One containing a list of users and their actions, the other containing errors'''
    error_lines = {}
    user_list = []
    with open(file_path, 'r') as file:
        for cur_line in file:
            if "ERROR" in cur_line:
                # Captures the ERROR {error type} (user_name)
                # and stores {error type} in regex register one
                pattern = r"ERROR\s(.*)\s\((.*)\)"
                current_error_line = re.search(pattern, cur_line)

                #Add the error to the error lines dictionary and
                #update the number of occurrences if it already exists in the dict
                if current_error_line[1] not in error_lines:
                    error_lines[current_error_line[1]] = 1
                else:
                    error_lines[current_error_line[1]] = error_lines[current_error_line[1]] + 1
                #Updates the number of errors associated with the username
                if current_error_line[2] not in user_list:
                    #Create a new user if the username has not been seen before
                    new_error_user = User(current_error_line[2], 0, 1)
                    user_list.append(new_error_user)
                else:
                    user_list[user_list.index(current_error_line[2])].addErrorCount()

            if "INFO" in cur_line:
                #Matches onto the INFO {task information} (username)
                #Captures username in the second regex register
                pattern = r"INFO\s(.*)\s\((.*)\)"
                current_info_line = re.search(pattern, cur_line)
                if current_info_line[2] not in user_list:
                    #Create a new user if the username has not been seen before
                    new_info_user = User(current_info_line[2], 1, 0)
                    user_list.append(new_info_user)
                else:
                    #Update the user info in the list
                    user_list[user_list.index(current_info_line[2])].addInfoCount()

        file.close()
    write_errors(error_lines)
    write_users(user_list)
    return

def write_errors(error_lines):
    '''Writes A CSV of the errors from most to least common'''
    #Header Row List Attributes
    keys = ["Error", "Count"]
    with open("error_message.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(keys)
        item_list = list(error_lines.items())

        #Lambda sorts the list by comparing the int stored in the second position in the item tuple
        #which corresponds to the number of errors
        item_list.sort(key=lambda a: a[1], reverse=True)
        for tuple in item_list:
            row = [tuple[0], tuple[1]]
            writer.writerow(row)
        file.close()



def write_users(user_list):
    '''Writes a list of users to the csv file, sorted alphabetically by username'''
    #Header Row List Attributes
    keys = ["Username", "INFO", "ERROR"]
    #This Lambda sorts the list alphabetically
    user_list.sort(key=lambda a: a.getusername())
    with open("user_statistics.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(keys)
        user_count = 0
        for user in user_list:
            if user_count < 8:
                row = [user.getusername(), user.get_info_number(), user.get_error_number()]
                writer.writerow(row)
                user_count += 1
            else:
                break
        file.close()

#Two useful debug functions to see the log file printed in the expected manner
def sort_errors(error_lines):
    print(sorted(error_lines.items(), key=operator.itemgetter(1), reverse=True))
    return error_lines




def main():
    log_file_path = os.path.join(os.getcwd() + "\syslog.log")
    print(log_file_path)
    read_in_log(log_file_path)

if __name__ == "__main__":
    main()
#/usr/bin/env python3
import csv
import os
import re
import operator
import sys

'''This program takes a log file and generates a small html report

This report contains the type and number of "ERRORS" in a log file, how many times an
error occurred, sorted from greatest to least 
'''

def read_in_log(file_path):
    error_lines = {}
    user_stats_errors = {}
    user_stats_info = {}
    with open(file_path, 'r') as file:
        for cur_line in file:
            if "ERROR" in cur_line:
                # Captures the ERROR {error type} (user_name)
                # and stores {error type} in regext register one
                pattern = r"ERROR\s(.*)\s\((.*)\)"
                current_error_line = re.search(pattern, cur_line)

                #Add the error to the error lines dictionary and
                #update the number of occurrences if it already exists in the dict
                if current_error_line[1] not in error_lines:
                    error_lines[current_error_line[1]] = 1
                else:
                    error_lines[current_error_line[1]] = error_lines[current_error_line[1]] + 1
                #Updates the number of errors associated with the username
                if current_error_line[2] not in user_stats_errors:
                    user_stats_errors[current_error_line[2]] = 1
                else:
                    user_stats_errors[current_error_line[2]] = user_stats_errors[current_error_line[2]] + 1
            if "INFO" in cur_line:
                pattern = r"INFO\s(.*)\s\((.*)\)"
                current_info = re.search(pattern, cur_line)
                if current_info[2] not in user_stats_info:
                    user_stats_info[current_info[2]] = 1
                else:
                    user_stats_info[current_info[2]] = user_stats_info[current_info[2]] + 1
        file.close()
    sort_user(user_stats_errors)
    sort_user(user_stats_info)

    write_errors(error_lines)
    write_users(user_stats_info,user_stats_errors)
    return

def write_errors(error_lines):
    '''Writes A CSV of the errors by most common, assumes passed in dict is sorted'''
    keys = ["Error", "Count"]
    with open("error_message.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(keys)
        item_list = list(error_lines.items())
        item_list.sort(key=lambda a: a[1], reverse=True)
        for tuple in item_list:
            row = [tuple[0], tuple[1]]
            writer.writerow(row)
        file.close()



def write_users(users_info, users_errors):
    keys = ["Username", "INFO", "ERROR"]
    with open("user_statistics.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(keys)
        user_names = list(users_info.keys())
        user_names.sort()
        for user_name in user_names:
            row = [user_name, users_info[user_name], users_errors[user_name]]
            writer.writerow(row)
        file.close()

#Two useful debug functions to see the log file printed in the expected manner
def sort_errors(error_lines):
    print(sorted(error_lines.items(), key=operator.itemgetter(1), reverse=True))
    return error_lines

def sort_user(user_dict):
    print(sorted(user_dict.items(), key=operator.itemgetter(0)))
    return user_dict



def main():
    log_file_path = os.path.join(os.getcwd() + "\syslog.log")
    print(log_file_path)
    #log_file_path = sys.argv[1]
    read_in_log(log_file_path)

if __name__ == "__main__":
    main()
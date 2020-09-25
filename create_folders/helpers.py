#!/usr/bin/env python3
# coding: utf-8





import logging
logger = logging.getLogger(__name__)





import sys
import csv
from pathlib import Path
# import PySimpleGUI as sg





def do_exit(e='unknown error in unknown module!', exit_status=99):
    '''handle exits and return exit function with either a soft_exit or hard_exit -
        The returned function can be executed by the calling process when it is ready 
        rather than forcing an exit immediately 
    
        soft_exit prints message and optionally logs message
        hard_exit prints message, logs and calls sys.exit(exit_status)
    
    Args:
        e(`str`): error or message detailing reason for exiting
        exit_status(int): exit value --
            0: soft_exit with no logging -- normal exit with no issues
            1: soft_exit with logging -- exit due to recoverable issue
            >1: hard_exit with logging -- abort execution with sys.exit(exit_status)
            
    Returns:
        function: soft_exit, hard_exit'''
    help_msg = f'try:\n{sys.argv[0]} -h for help'
    def hard_exit():
        print(e)
        sys.exit(exit_status)
        
    def soft_exit():
        print(e)
        return(e)
    
    if exit_status > 1:
        logging.error(f'fatal error:\n\t{e}')
        return(hard_exit)
    
    if exit_status == 1:
        logging.warning(f'exited before completion with code {exit_status}')
        logging.warning(e)
        print(help_msg)
        return(soft_exit)
    
    if exit_status < 1:
        logging.debug(e)
        return(soft_exit)





def csv_to_list(file):
    '''read csv file `file` into a list
    
    Guess the CSV dialect (e.g. tsv, csv, etc.)
    
    Returns `list`'''
    logging.debug(f'reading {file} to list')
    csvFile = Path(file).expanduser().absolute()
    file_csv = []
    # try to figure out the dialect (csv, tsv, etc.)
    with open(csvFile, 'r') as file:
#         dialect = csv.Sniffer().sniff(file.read(1024))
        dialect = csv.Sniffer().sniff(file.readline())
        file.seek(0)
        reader = csv.reader(file, dialect)
        for row in reader:
            file_csv.append(row)

    return file_csv





def map_headers(csv_list, expected_headers=[]):
    '''map row 0 of a csv as formatted as a list to a dictionary of expected header values'''
    missing_headers = []
    header_map = {}
    
    csvHeader = csv_list[0]
    logging.debug('mapping headers')
    logging.debug('checking for missing headers')
    for each in expected_headers:
        if each not in csvHeader:
            missing_headers.append(each)
            
    if len(missing_headers) > 0:
        logging.warning(f'missing expected headers: {missing_headers}')
    for index, value in enumerate(csvHeader):
        if value in expected_headers:
            header_map[value] = index
        
    logging.debug('completed mapping')
    return(header_map, missing_headers)





def validate_data(csv_list, expected_headers, header_map):
    '''validate list items for proper data types
         naievely attempts to coerce strings from CSV into expected_header types
         returns a tuple of list of rows that were successfully coerced and those
         that could not be coerced
    
    Args:
        csv_list(`list` of `list`): csv as a nested list [['h1', 'h2'], ['item', 'item2']]
        expected_headers(`dict`): {'literal_header': type} {'ClassOf':, int, 'Name', str}
        header_map(`dict`): map of list index for each header {'h1': 0, 'h2': 5, 'hN': i}
        
    Returns:
        (`tuple` of `list`): (valid_rows, invalid_rows)
    '''
    valid = []
    invalid = []

    for row in csv_list[1:]:
        good_row = True
        for k in expected_headers.keys():
            # test for coercable types
            try:
                test = expected_headers[k](row[header_map[k]])
            except (ValueError):
#                 do_exit(f'Bad student.export: {k} contained {row[header_map[k]]}\ncannot continue. Please try running the export again.')
                logging.warning(f'bad row: {row}')
                logging.warning(f'column "{k}" contained "{row[header_map[k]]}"--this should be {(expected_headers[k])}')
                invalid.append(row)
                good_row = False
                break
        if  good_row:
            valid.append(row)
        
    return valid, invalid
    





def adjust_handler(handler=None, new_level=None):
    '''adjust a logging handler
    
    Args:
        handler(`str`): partial string in handler name - if none, returns list of all handlers attached to root
            '*' adjusts all handlers to new_level
        new_level(`str`): DEBUG, INFO, WARNING, ERROR
    
    Returns:
        `list`: list of handlers and levels currently set'''
    if not handler:
        return(logging.getLogger().handlers)
    
    my_handler = None    
    for index, val in enumerate(logging.getLogger().handlers):
        if handler == '*':
            my_handler = logging.getLogger().handlers[index]
        else:
            if handler in str(val):
                my_handler = logging.getLogger().handlers[index]
        if my_handler:
            logging.info(f'setting {str(my_handler)} to {new_level}')
            my_handler.setLevel(new_level)
        else:
            logging.warning(f'handler: "{handler}" not found')
        
    return logging.getLogger().handlers





def csv_writer(rows_list, path, dialect=None):
    '''write a list to csv with minimal quoting 
    
    Args:
        rows_list(`list`): list of lists to convert to csv
        path(`str` or `Path`): path to output file
        dialect(`csv.Dialect` or `str`): csv.Dialect object or string of known CSV dialect
            such as excel, excel_tab, unix_dialect'''
#     if dialect:
#         use_dialect = getattr(csv, dialect)
#     else:
#         use_dialect = None
    if isinstance(dialect, type):
        use_dialect = dialect
    else:
        try:
            use_dialect = getattr(csv, dialect)
        except (TypeError, AttributeError):
            use_dialect=None

    logging.debug(f'writing csv file: {path}')
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, dialect=use_dialect, quoting=csv.QUOTE_MINIMAL)
        for each in rows_list:
            writer.writerow(each)





def len_of_dict(my_set):
    '''calculate the overall length of a dict of list like objects
    
    Args:
        my_set(`dict` or dict-like object): dictonary to assess
        
    Returns:
        int - length of all elements'''
    total = 0
    for each_set in my_set:
        total = total + len(my_set[each_set])
    return total



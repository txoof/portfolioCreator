#!/usr/bin/env python
# coding: utf-8


# In[ ]:


#get_ipython().run_line_magic('alias', 'nb_convert ~/bin/develtools/nbconvert helpers.ipynb')




# In[ ]:


#get_ipython().run_line_magic('nb_convert', '')




# In[ ]:


import logging
logger = logging.getLogger(__name__)




# In[ ]:


import sys
import csv
from pathlib import Path




# In[5]:


def do_exit(e='unknown error in unknown module: BSoD!', exit_status=99):

        
    print('\n'*4)
    if exit_status == 1:
        logging.warning(f'exited before completion with exit code {exit_status}')
        logging.warning(e)  
    elif exit_status > 1:
        logging.error(f'fatal error:\n\t{e}')
    print(e)
    sys.exit(exit_status)




# In[28]:


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




# In[ ]:


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




# In[ ]:


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
    




# In[ ]:


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



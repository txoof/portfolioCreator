#!/usr/bin/env python
#!/usr/bin/env python
# coding: utf-8


# In[2]:


#get_ipython().run_line_magic('load_ext', 'autoreload')

#get_ipython().run_line_magic('autoreload', '2')
#get_ipython().run_line_magic('reload_ext', 'autoreload')




# In[3]:


#get_ipython().run_line_magic('alias', 'nb_convert ~/bin/develtools/nbconvert createFolders.ipynb')




# In[ ]:


#get_ipython().run_line_magic('nb_convert', '')




# In[4]:


import constants
# import class_constants
# import & config logging first to prevent any sub modules from creating the root logger
import logging
from logging import handlers
from logging import config
logging.config.fileConfig(constants.logging_config, defaults={'logfile': constants.log_file} )




# In[5]:


from helpers import *

from filestream import GoogleDrivePath, GDStudentPath




# In[6]:


# import csv
import sys
from pathlib import Path
# import subprocess
import time
import ArgConfigParse
import os
import glob

from datetime import datetime

import PySimpleGUI as sg




# In[7]:


def parse_cmdargs():
    '''set known command line arguments, parse sys.argv
    
    Returns:
        `dict`: nested dictionary of command line arguments that matches strcture of .ini file'''
    args = ArgConfigParse.CmdArgs()
    args.add_argument('-s', '--student_export', ignore_none=False, metavar='/path/to/student.export.csv', 
                      type=str, dest='student_export', help='Export from PowerSchool containing: LastFirst, ClassOf, Student_Number')

    args.add_argument('-g', '--google_drive', ignore_none=True, metavar='/Volumes/GoogleDrive/Shared drives/ASH Cum Folders/folder/',
                      type=str, dest='main__drive_path', help='Full path to Google Drive Shared Drive containing cumulative files')

    args.add_argument('-l', '--log_level', ignore_none=True, metavar='ERROR, WARNING, INFO, DEBUG', 
                      type=str, dest='main__log_level', help='Logging level -- Default: WARNING')
    args.add_argument('-v', '--version', dest='version', action='store_true',
                      default=False, help='Print version number and exit')

    args.parse_args()
    return args.nested_opts_dict                  




# In[8]:


def read_config(files):
    '''parse .ini files 
    
    Args:
        files(`list`): list of `str` containing files in .ini format to parse
    
    Returns:
        `dict`: nested dict of configuration'''
    parser = ArgConfigParse.ConfigFile(config_files=files, ignore_missing=True)
    parser.parse_config()
    
    return parser.config_dict




# In[9]:


def check_drive_path(drive_path=None):
    '''check that path is a valid google drive path and contains the appropriate sentry file
    
    Args:
        drive_path(`str`): path to google drive containg cummulative folders and sentry file
    
    Retruns:
        `tuple` of `bool`, `str`: When true, drive is OK; when false, drive is not valid; str contains errors'''
    # this is super redundant -- checks the following:
    # * is a path
    # * is a google drive path
    # * if sentry file exists
    # this may be a good idea considering how some users have run into many problems with this

    drive_ok = True
    msg = None
    if not drive_path:
        logging.info('no google drive specified')
        drive_ok = False
        msg = 'No Google Drive specified'
        return drive_ok, msg
    else:
        drive_path = Path(drive_path)
    
    if not drive_path.exists():
        logging.warning(f'specified path "{drive_path}" does not exist')
        drive_ok = False
        msg = f'The Google Drive "{drive_path}" does not appear to exist on Google Drive'
        return drive_ok, msg
    else:
        google_drive = GoogleDrivePath(drive_path)
    
    try:
        google_drive.get_xattr('user.drive.id')
    except ChildProcessError as e:
        logging.warning(f'specified path "{drive_path}" is not a Google Drive path')
        msg = f'The Google Drive "{drive_path}" does not appear to be a valid google Shared Drive'
        drive_ok = False
        return drive_ok, msg

    sentry_file = constants.sentry_file    
    sentry_file_path = drive_path/Path(sentry_file)
    
    if not sentry_file_path.is_file():
        logging.warning(f'sentry file is missing in specified path "{drive_path}"')
        msg = f'''The chosen google shared drive "{drive_path}"
does not appear to be a Cumulative Student Folder. 

The file: "{sentry_file}" is missing. 
If you are sure {drive_path} is correct, 
please contact IT Support and askfor help. 

Please screenshot or copy this entire text below and provide it to IT Support.

###############################################################################
Run the command below from the terminal of the user that submitted this ticket.
This command will create the necessary files for this script. 

Confirm that {drive_path} is the correct
Google Shared Drive for Cumulative Student Folders BEFORE proceeding.
     $ touch {drive_path}/{sentry_file}'''
        drive_ok = False
    
    
    
    return drive_ok, msg




# In[10]:


def create_folders(drive_path, valid_rows, header_map):
    logging.info(f'creating folders as needed in {drive_path}')
    grade_level_dirs = constants.student_dirs
    
    directories = {'created': [], 'exist': [], 'duplicate': [], 'failed': [], 'multiple': [], 'subdirs': []}
    directories_to_check = []

    total = len(valid_rows)
    remaining = len(valid_rows)
    print(f'{total} will be checked and created if needed')
    
    def make_subdirs(student_dir):
        '''helper function to create multiple child directories in `student_dir`
        
        Args:
            student_dir(`GDStudent`): parent for child directories
        
        Returns:
            None'''
        logging.debug(f'checking grade level dirs for {student_dir}')
        for gld in grade_level_dirs:
            subdir = student_dir.mkchild(gld, exist_ok=True)
            if not subdir.exists():
                try:
                    subdir.mkdir()
                except (OSError, FileNotFoundError) as e:
                    logging.warning(f'error creating grade level directory: {gld}: {e}')
                    directories['failed'].append(subdir)
                else:
                    directories['subdirs'].append(subdir)
            else:
                if not subdir.confirm():
                    logging.debug(f'exists, but is not confirmed: {subdir}')
                    directories['subdirs'].append(subdir)
#         return ok, failed
                
    

    
    # build a list of GDStudentPath objects to check for existence/creation
    
    logging.info(f'processing {len(valid_rows)} rows')
    for student in valid_rows:
        class_of = student[header_map['ClassOf']]
        last_first = student[header_map['LastFirst']]
        student_number = student[header_map['Student_Number']]
        logging.debug(f'class: {class_of}, lastfirst: {last_first}, student number: {student_number}')
        directories_to_check.append(GDStudentPath(drive_path, ClassOf=class_of, Student_Number=student_number, LastFirst=last_first))
    
    
    # check for similar directories
    for directory in directories_to_check:
        print(f'{remaining} of {total} folders to be processed')
        logging.debug(f'checking for existing dirs with student number: {directory.Student_Number}')
        directory.check_similar()
        # new directories
        if len(directory.matches) == 0:
            logging.debug(f'creating new directory for {directory.LastFirst}')
            try:
                directory.mkdir()
            except (OSError, FileNotFoundError) as e:
                logging.warning(f'error creating directory: {directory.path}: {e}')
                directories['failed'].append(directory)
            else:
                directories['created'].append(directory)
            
            # queue subdirs for creation
            make_subdirs(directory)
                    
        # existing directories           
        if len(directory.matches) == 1 and not directory.duplicate:
            logging.debug(f'existing directory for {directory.LastFirst}, this is OK')
            directories['exist'].append(directory)
            # queue subdirs for creation
            make_subdirs(directory)
        
        if len(directory.matches) == 1 and directory.duplicate:
            logging.warning(f'a directory already exists with a different LastFirst, but the same Student_Number; this is NOT OK')
            logging.info('this directory will not be created')
            directories['duplicate'].append(directory)
            
    
        # directories that have multiple matches
        if len(directory.matches) > 1:
            logging.warning(f'{len(directory.matches)} existing directories found for {directory.LastFirst}; this is NOT OK')            
            logging.info('this directory will not be created')            
            directories['multiple'].append(directory) 
        remaining = remaining - 1

                
    return directories




# In[11]:


def check_folders(directories):
    '''Verify that processed rows have synchronized over filestream
    report on those that have failed to sync
    
    Args:
        directories(`dict`): {'created': [], 'subdirs': [], 'exist': []}
            all other keys will be returned in the unconfirmed_sets of the tuple
        
    Returns:
        tuple(confirmed_sets, unconfirmed_sets)'''
    # try to confirm created files N times before giving up
    confirm_retry = constants.confirm_retry
    #  wait N seconds for first try, N*retry for each subsiquent retry
    base_wait = constants.base_wait  
    checks_complete = False
    
    sets_to_check = ['created', 'subdirs', 'exist']
    
    unconfirmed_sets = {}
    confirmed_sets = {}    
    
    for each_set in directories:
        if not each_set in sets_to_check:
            unconfirmed_sets[each_set] = set(directories[each_set])
    
    for each_set in sets_to_check:
        unconfirmed_sets[each_set] = set(directories[each_set])
        confirmed_sets[each_set] = set()


    for i in range(0, confirm_retry):        
        logging.info(f'checking student directories: attempt {i+1} of {confirm_retry}')
        unconfirmed_dir_total = 0
        delay = base_wait * i
        if i > 0:
            logging.info(f'pausing {delay} seconds before checking again ')
            time.sleep(delay)
        
        for each_set in sets_to_check:
            logging.debug(f'verifying set: {each_set}')
            confirmed_dirs = set()
            for each_dir in unconfirmed_sets[each_set]:
                logging.debug(f'checking {each_dir}')
                if each_dir.confirm():
                    logging.debug('confirmed')
                    confirmed_dirs.add(each_dir)
            unconfirmed_sets[each_set].difference_update(confirmed_dirs)
            confirmed_sets[each_set].update(confirmed_dirs)
        
        for each_set in sets_to_check:
            unconfirmed_dir_total = unconfirmed_dir_total + len(unconfirmed_sets[each_set])
        logging.debug(f'{unconfirmed_dir_total} directories remain unconfirmed')
        
        if unconfirmed_dir_total <= 0:
            break
            
    return confirmed_sets, unconfirmed_sets




# In[12]:


def write_csv(confirmed, unconfirmed, invalid_list, csv_output_path=None):
    '''write out processed directories to a CSV file for import into PowerSchool SIS
    
    Args:
        confirmed(`dict` of `set`): directories that were created and confirmed to exist
        unconfirmed(`dict` of `set`): directories that were created and could not be confirmed
        invlaid_list('list'): rows from imported csv that contained bad data types 
        output_path(`str`): override default directory pulled from constants.csv_output_path 
            to use for output of CSV file
        
    Returns:
        `tuple` of path to confirmed and unconfirmed csv files'''
    
    
    
    if csv_output_path:
        csv_output_path = Path(csv_output_path)
    else:
        csv_output_path = constants.csv_output_path
        
        
    if not csv_output_path.exists():
        logging.info(f'creating output directory: {csv_output_path}')
        try:
            csv_output_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            do_exit(e, 1)
        
    date = datetime.now().strftime(constants.date_format)
    
    confirmed_file = f'{constants.csv_output_name}'.format(date=date)
    unconfirmed_file = f'{constants.csv_error_name}'.format(date=date)
    invalid_file = f'{constants.csv_invalid_name}'.format(date=date)
    
    # handle confirmed directories
    csv_output_headers = constants.csv_output_headers
    csv_output_list = []
    
    confirmed_dirs = confirmed['created']
    confirmed_dirs.update(confirmed['exist'])
    
    logging.info('processing confirmed directories')
    # add the headers to the list
    csv_output_list.append(list(csv_output_headers.keys()))
    for each_dir in confirmed_dirs:
        row = []
        for column in csv_output_headers:
            # retreive a property from an object using a string
            # https://stackoverflow.com/qu            
            object_property = getattr(each_dir, column)
            # create a formatted string based on prop value and formatter from headers dict
            formatted_string = f'{csv_output_headers[column]}'.format(val=object_property)
            row.append(formatted_string)
        csv_output_list.append(row)
    try:
        csv_writer(csv_output_list, csv_output_path/confirmed_file)
    except Exception as e:
        logging.warning(f'{e}')    
        
    # handle unconfirmed directories
    csv_error_headers = constants.csv_error_headers
    csv_error_strings = constants.csv_error_strings
    csv_error_list = []

    # add the headers to the output file
    csv_error_list.append(list(csv_error_headers.keys()))

    for each_set in unconfirmed:
        if each_set in csv_error_strings:
            logging.debug(f'processing unconfirmed set: {each_set}')
            for each_dir in unconfirmed[each_set]:
                logging.debug(f'processing: {each_dir}')
                row = []
                for column in csv_error_headers:
                    try:
                        object_property = getattr(each_dir, column)
                    except AttributeError:
                        formatted_string = csv_error_strings[each_set]
                    else:
                        formatted_string = f'{csv_error_headers[column]}'.format(val=object_property)
                    row.append(formatted_string)
                csv_error_list.append(row)
        else:
            # handle rows that are do not have a key
            logging.warning(f'unknown set type in unconfirmed set: {each_set}')   
    if len(csv_error_list) > 1:
        logging.info('writing unconfirmed dirs csv')
        try:
            csv_writer(csv_error_list, csv_output_path/unconfirmed_file)
        except Exception as e:
            logging.warning(f'{e}')    
    else:
        logging.info('no unconfirmed directories found; no error output needed')
        
    #handle invalid rows that could not be processed due to bad or missing data
    if len(invalid_list) > 1:
        logging.info('writing invalid rows csv')
        try:
            csv_writer(invalid_list, csv_output_path/invalid_file)
        except Exception as e:
                logging.warning(f'{e}')

    
    return {'confirmed': csv_output_path/confirmed_file, 
            'unconfirmed': csv_output_path/unconfirmed_file, 
            'invalid': csv_output_path/invalid_file}
    
    




# In[13]:


def window_drive_path():
    drive_path = sg.Window(constants.app_name,
                          [[sg.Text ('Choose the Google Shared Drive and folder that contains student cummulative folders.')],
                                     [sg.In(), sg.FolderBrowse()],
                                     [sg.Ok(), sg.Cancel()]]).read(close=True)[1][0]
    return Path(drive_path)




# In[14]:


class multi_line_string():
    def __init__(self, s=''):
        self._string = ''
        self.string = s
    
    def __str__(self):
        return self.string
    
    @property
    def string(self):
        return self._string
    
    @string.setter
    def string (self, s):
        self._string = self._string + s + '\n'
        
        
    




# In[15]:


def main():    
    # set the local logger
    logger = logging.getLogger(__name__)
    logging.info('*'*50+'\n')

    if sys.argv == 1:
        run_gui = True
    else:
        run_gui = True
    
    
    ##### REMOVE THIS!
    if '-f' in sys.argv:
        print('Likely in jupyter environment -- remove this!')
        run_gui = True
    
    # base configuration fle
    config_file = Path(constants.config_file)
    # user config file (~/.config/app_name/app.ini)
    user_config_path = Path(constants.user_config_path)
    
    # if the user configuration file is missing set to True & create later at end
    update_user_config = not(user_config_path.exists)
    logging.debug(f'user config will be created: {update_user_config}')

    # parse command line and config files - 
    cmd_args_dict = parse_cmdargs()
    cfg_files_dict = read_config([constants.config_file, constants.user_config_path])

    # merge the command line arguments and the config files; cmd line overwrites files
    config = ArgConfigParse.merge_dict(cfg_files_dict, cmd_args_dict)
    
#     return config
    
    # launch a window for monitoring stdout if run_gui
    if run_gui:
        sg.Print('Re-routing the stdout', do_not_reroute_stdout=False)
        pass
    
    # get drive_path through gui if needed
    if not config['main']['drive_path'] and run_gui:
        logging.debug('launching GUI folder browser')
        ret_drive_path = window_drive_path()
        if not ret_drive_path:
            do_exit('You must specify a Google Shared drive to proceed.', 1)
        else:
            config['main']['drive_path'] = ret_drive_path
            update_user_config = True

    if config['__cmd_line']['version']:
        print(f'{constants.app_name} version:{constants.version}')
        print(f'Developer contact information:\n\t{constants.contact}\n\t{constants.git_repo}')
        do_exit('', 0)

    # adjust the logging levels if needed
    if config['main']['log_level']:
        ll = config['main']['log_level']
        if ll in (['DEBUG', 'INFO', 'WARNING', 'ERROR']):
            logging.root.setLevel(ll)
            handlers = adjust_handler('*', ll)
            logging.debug(f'adjusted log levels: {handlers} to {ll}')
        else:
            logging.warning(f'unknown or invalid log_level: {ll}')
    
    # load file constants
    expected_headers = constants.expected_headers    
    student_dirs = constants.student_dirs
        
    # get csv_file and drive_path from the command line
    try:
        csv_file = Path(config['__cmd_line']['student_export'])
    except TypeError:
        logging.info('No student export file specified on command line')
        csv_file = None
        
    # check drive path is a google drive path
    drive_path = Path(config['main']['drive_path'])

    drive_status = check_drive_path(drive_path)    
    if not drive_status[0]:
        do_exit(drive_status[1], 1)
        # consider prompting user at this point to enter a valid drive
    
    if not csv_file and run_gui:
        csv_file = Path(sg.popup_get_file('Select a Student Export File to Process'))
    
    # read CSV into a list
    if not csv_file:
        do_exit('No student export CSV file specified. Exiting.', 1)
    try:
        print(f'\nProcessing {csv_file} file...')
        csv_list = csv_to_list(csv_file)
    except (FileNotFoundError, OSError, IOError, TypeError) as e:
        logging.error(f'could not read csv file: {csv_file}')
        logging.error(f'{e}')
        do_exit(e, 1)
    except csv.Error as e:
        logging.error(f'e')
        do_exit(f'{e} of file "{csv_file}". Try using the field delimiter "Comma" when preparing the export', 1)
    finally:
        print(f'file successfully read ')
    
    # map the expected headers to the appropriate columns
    print(f'checking for appropriate column headers')
    header_map, missing_headers = map_headers(csv_list, expected_headers.keys())
    
    # error out if there are any missing headers in the export file
    if len(missing_headers) > 0:
        do_exit(f'{csv_file.name} is missing one or more headers:\n\t{missing_headers}\nprogram cannot continue', 1)
    
    # validate the csv list
    print(f'checking rows for invalid data')
    valid_rows, invalid_rows = validate_data(csv_list, expected_headers, header_map)
    print(f'{len(valid_rows)} student rows were found')
    print(f'{len(invalid_rows)} improperly formated student rows were found')
    
    # FIX ME add checks here for bad valid_rows, invalid rows
    
    # insert the headers to the invalid rows list for output later
    invalid_rows.insert(0, csv_list[0])
    
#     return valid_rows, invalid_rows, header_map
    
    print(f'\nPreparing to create student folders for {len(valid_rows)} students')
    print(f'using Google Shared Drive: {drive_path}')
    print(f'this could take a while...')
    directories = create_folders(drive_path=drive_path, valid_rows=valid_rows, header_map=header_map)
    
    print(f'checking that {len(directories)} student folders were properly created in the cloud')
    confirmed_dirs, unconfirmed_dirs = check_folders(directories)
    print(f'{len(confirmed_dirs)} were confirmed; {len(unconfirmed_dirs)} could not be confirmed')
#     return confirmed_dirs, unconfirmed_dirs

    csv_files = write_csv(confirmed_dirs, unconfirmed_dirs, invalid_rows)
        
    if update_user_config:
        try:
            logging.info(f'updating user configuration file: {user_config_path}')
            ArgConfigParse.write(config, user_config_path, create=True)
        except Exception as e:
            m = f'Error updating user configuration file: {e}'
            do_exit(m, 1)
    
    
    len_confirmed = len_of_dict(confirmed_dirs)
    len_unconfirmed = len_of_dict(unconfirmed_dirs)
            
    # Add a summary output:
    s = multi_line_string()
#     print('********* Summary **********')
    s.string = '********* Summary **********'
#     print(f'Processed {len(csv_list)-1} student records from "{csv_file}"')
    s.string = f'Processed {len(csv_list)-1} student records from "{csv_file}"'
#     print(f'{len(valid_rows)} records contained valid data and were processed.')
    s.string = f'{len(valid_rows)} records contained valid data and were processed.'
    if len(invalid_rows) > 1:
#         print(f'{len(invalid_rows)-1} records contained invalid data and could not be used')
        s.string = f'{len(invalid_rows)-1} records contained invalid data and could not be used\n'
#     print(f'\n')

    if len_confirmed > 0:
#         print(f'Succesfully created or validated folders are stored in: \n{csv_files["confirmed"]}\n\tShare this file with the PowerSchool Administrator\n')
        s.string = f'Succesfully created or validated folders are stored in: \n{csv_files["confirmed"]}\n\tShare this file with the PowerSchool Administrator\n'
    if len_unconfirmed > 0:
#         print(f'Records that could not be confirmed are stored in: \n{csv_files["unconfirmed"]}\n\tPlease run the tool again')
        s.string = f'Records that could not be confirmed are stored in: \n{csv_files["unconfirmed"]}\n\tPlease run the tool again'
    if len(invalid_rows) > 1:
        s.string = f'Rows that contained invalid data that were NOT processed are stored in: \n{csv_files["invalid"]}\n\tReview this file to learn more.'
#         print(f'Rows that contained invalid data that were NOT processed are stored in: \n{csv_files["invalid"]}\n\tReview this file to learn more.')  
    sg.popup(s)
    logging.debug('done')
    # final print
    print('.')

    if run_gui:
        sg.easy_print_close()

    return valid_rows, invalid_rows




# In[17]:


if __name__ == '__main__':
    if '-f' in sys.argv:
        print = sg.Print
        print('running gui')
    f = main()




# In[ ]:


# adjust_handler('*', 'DEBUG')
# adjust_handler('*', 'INFO')




# In[ ]:


# # sys.argv.append('-g')
# # sys.argv.append('/Volumes/GoogleDrive/Shared drives/IT Blabla I/Student Cumulative Folders (AKA Student Portfolios)')

# # # sys.argv.append('-g')
# # # sys.argv.append('/xVolumes/GoogleDrive/Shared drives/IT Blabla I/Student Cumulative Folders (AKA Student Portfolios)')

# sys.argv.append('-s')
# # sys.argv.append('./data/student.export.text')
# sys.argv.append('./data/invalid.student.export.text')
# # sys.argv.append('./bad.student.export.text')

# sys.argv.append('-v')

# # sys.argv.append('-l')
# # sys.argv.append('INFO')




# In[ ]:


# sys.argv.pop()

# # sys.argv




# In[ ]:


# sys.argv



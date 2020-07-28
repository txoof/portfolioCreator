#!/usr/bin/env python
# coding: utf-8


# In[1]:


#get_ipython().run_line_magic('load_ext', 'autoreload')

#get_ipython().run_line_magic('autoreload', '2')
#get_ipython().run_line_magic('reload_ext', 'autoreload')




# In[2]:


#get_ipython().run_line_magic('alias', 'nb_convert ~/bin/develtools/nbconvert createFolders_graceful.ipynb')
#get_ipython().run_line_magic('nb_convert', '')




# In[3]:


import builtins

# I'm not sure why this is needed, but this resolves a runtime crash when run from the command line
# reassign the builtins.print function to bprint
bprint = builtins.print

# import & config logging first to prevent any sub modules from creating the root logger
import logging
from logging import handlers
from logging import config
logging.config.fileConfig(constants.logging_config, defaults={'logfile': constants.log_file} )




# In[ ]:


import constants
import error_msgs
from helpers import *
from filestream import GoogleDrivePath, GDStudentPath




# In[ ]:


import sys
from pathlib import Path
import time
import ArgConfigParse
import os
import glob
from datetime import datetime
import textwrap

from rich.console import Console
from rich.markdown import Markdown
import PySimpleGUI as sg




# In[ ]:


class multi_line_string():
    '''multi-line string object 
    
    each time  multi_line_string.string is set equal to a string, it is added to 
    the existing string with a new line character
    
    Properties:
        string(`str`): string'''

    def __init__(self, s=''):
        self._string = ''
        self.append(s)
    
    def __str__(self):
        return str(self.string)
    
    def __repr__(self):
        return(str(self.string))
    
    @property
    def string(self):
        return self._string
    
    @string.setter
    def string(self, s):
        self._string = s
    
    def append (self, s):
        self._string = self._string + s + '\n'
        
    




# In[ ]:


def wrap_print(t='', width=None):
    if not width:
        width = constants.TEXT_WIDTH
        
    wrapper = textwrap.TextWrapper(width=width, break_long_words=False, replace_whitespace=False)
#     pdb.set_trace()
    result = '\n'.join([wrapper.fill(line) for line in t.splitlines()])
#     pdb.set_trace()
# this causes a runtime crash; it's unclear why, but is resolved by reassigning bprint = builtins.print 
#     builtins.print(result)
    bprint(result)




# In[ ]:


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
    
    args.add_argument('--more_help', dest='more_help', action='store_true',
                       default=False, help='Print extened help and exit')

    args.parse_args()
    return args.nested_opts_dict                  




# In[ ]:


def read_config(files):
    '''parse .ini files 
    
    Args:
        files(`list`): list of `str` containing files in .ini format to parse
    
    Returns:
        `dict`: nested dict of configuration'''
    parser = ArgConfigParse.ConfigFile(config_files=files, ignore_missing=True)
    parser.parse_config()
    
    return parser.config_dict




# In[ ]:


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
#         msg = f'The Google Drive "{drive_path}" does not appear to exist on Google Drive'
        msg = error_msgs.PATH_ERROR.format(drive_path=drive_path)
        return drive_ok, msg
    else:
        google_drive = GoogleDrivePath(drive_path)
    
    try:
        google_drive.get_xattr('user.drive.id')
    except ChildProcessError as e:
        logging.warning(f'specified path "{drive_path}" is not a Google Drive path')
#         msg = f'The Google Drive "{drive_path}" does not appear to be a valid google Shared Drive'
        msg = error_msgs.NON_GDRIVE_ERROR.format(drive_path=drive_path)
        drive_ok = False
        return drive_ok, msg

    sentry_file = constants.sentry_file    
    sentry_file_path = drive_path/Path(sentry_file)
    
    if not sentry_file_path.is_file():
        logging.warning(f'sentry file is missing in specified path "{drive_path}"')
        msg = error_msgs.SENTRY_ERROR.format(drive_path=drive_path, sentry_file=sentry_file)
#         msg = f'''The file: "{sentry_file}" is missing from the chosen shared drive:
# `{drive_path}`

# This does not appear to be the correct folder for `Cumulative Student Folders.` 

# Choose a different Shared Drive with the button:
# #######################
# # Change Shared Drive #
# #######################


# If you are sure 
# `{drive_path}` 
# is correct, please contact IT Support and ask for help. 

# Screenshot or copy this entire text below the line and provide it to IT Support.
# ###########################################################

# IT Support:
# {sys.argv[0]}
# The program above uses Google File Stream to create student folders on a Google Shared Drive. The Shared Drive should contain a folder called `Student Cumulative Folders (AKA Student Portfolios)` or something similar. 

# The program checks for `{sentry_file}` to ensure that the user has selected the appropriate Google Shared Drive **AND** the appropriate folder.

# BEFORE PROCEEDING: Confirm that {drive_path} is correct and contains the `Student Cumulative Folders (AKA Student Portfolios)` folder.

# The following steps should be run on the user's computer, signed in as the user

# 1) Check Google File Stream is running on the user's computer and the use is signed in
# 2) Use Finder to verify the user has access to {drive_path}
# 3) Check that `Student Cumulative Folders (AKA Student Portfolios)` exists on the Shared Drive above
# 4) Open `terminal.app` and run the command below

#      $ touch {drive_path}/{sentry_file}
     
# 5) Try running the program again'''
        drive_ok = False
        
    
    
    
    return drive_ok, msg




# In[ ]:


import error_msgs
f = check_drive_path('/Volumes/GoogleDrive/Shared drives/IT Blabla/')
print(f[1])




# In[ ]:


def create_folders(drive_path, valid_rows, header_map, window=None):
    logging.info(f'creating folders as needed in {drive_path}')
    grade_level_dirs = constants.student_dirs
    
    directories = {'created': [], 'exist': [], 'duplicate': [], 'failed': [], 'multiple': [], 'subdirs': []}
    directories_to_check = []

    total = len(valid_rows)
    print(f'{total} student directories will be checked and created if needed')
    
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
                
    

    if window:
        window.Refresh()
    
    # build a list of GDStudentPath objects to check for existence/creation
    
    logging.info(f'processing {total} rows')
    
    for student in valid_rows:
        class_of = student[header_map['ClassOf']]
        last_first = student[header_map['LastFirst']]
        student_number = student[header_map['Student_Number']]
        logging.debug(f'class: {class_of}, lastfirst: {last_first}, student number: {student_number}')
        directories_to_check.append(GDStudentPath(drive_path, ClassOf=class_of, Student_Number=student_number, LastFirst=last_first))
    
    
    # check for similar directories
    for index, directory in enumerate(directories_to_check):
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
        print(f'{(index+1)/total*100:.0f}% completed')

        if window:
            sg.one_line_progress_meter(title='Cumulative Folder Creation', 
                                       current_value=index+1, 
                                       max_value=len(directories_to_check), 
                                       key='key',
                                       orientation='h')
            window.Refresh()

                
    return directories




# In[ ]:


def check_folders(directories, window=None):
    '''Verify that processed rows have synchronized over filestream
    report on those that have failed to sync
    
    Args:
        directories(`dict`): {'created': [], 'subdirs': [], 'exist': []}
            all other keys will be returned in the unconfirmed_sets of the tuple
        window(`PySimpleGUI window): window object; refresh after each print statement
        
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
        print(f'attempt {i+1} of {confirm_retry}')
        
        delay = base_wait * i
        if i > 0:
            logging.info(f'pausing {delay} seconds before checking again ')
            print(f'pausing for {delay} seconds')
            time.sleep(delay)
            
        if window:
            window.Refresh()
            
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
            print(f'all folders confirmed')
            break
        print(f'{unconfirmed_dir_total} remain to be checked')
        if window:
            window.Refresh()
    
    return confirmed_sets, unconfirmed_sets




# In[ ]:


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
    
    




# In[ ]:


# def window_drive_path():
#     '''launch an interactive window to ask user to specify a google drive shared folder'''
#     drive_path = sg.Window(constants.app_name,
#                           [[sg.Text ('Choose the Google Shared Drive and folder that contains student cummulative folders.')],
#                                      [sg.In(), sg.FolderBrowse()],
#                                      [sg.Ok(), sg.Cancel()]]).read(close=True)[1][0]
    
#     if drive_path:
#         drive_path = Path(drive_path)
#         logging.debug(f'user selected: {drive_path}')
#     else: 
#         drive_path = None
#         logging.info('no drive path selected')
        
#     return drive_path




# In[ ]:







# In[ ]:


def window_drive_path():
    drive_path = sg.popup_get_folder('Choose the Google Shared Drive **AND** folder that contains student cumulative folders.', 
                                     title='Select A Shared Drive', 
                                     initial_folder='/Volumes/GoogleDrive/',
                                     keep_on_top=True, font=constants.FONT, location=constants.WIN_LOCATION)
    
    if drive_path:
        drive_path=Path(drive_path)
        logging.debug(f'user selected: {drive_path}')
    else:
        drive_path = None
        logging.info('no drive path selected by user')
    return drive_path




# In[ ]:


def window_csv_file():
    '''launch an interactive window to ask user to specify a student export file'''
    logging.debug('launching interactive prompt for csv file')
    csv_file = sg.popup_get_file('Select a Student Export File to Process', 
                                 title='Select A Student Export',
                                 initial_folder=Path('~/Downloads').expanduser(),
                                 keep_on_top=True, font=constants.FONT, location=constants.WIN_LOCATION)
    
    if csv_file:
        csv_file = Path(csv_file)
    else: 
        csv_file = None
        logging.info('no student_export path selected')
        
    return csv_file




# In[ ]:


def print_help():
    
    logging.debug('getting help')
    console = Console()
    console.options.max_width = constants.TEXT_WIDTH
    try:
        with open(constants.HELP_FILE) as help_file:
            markdown = Markdown(help_file.read())
    except Exception as e:
        logging.error(e)
        return do_exit(f'Error getting help!\n{e}', 1)
    
    console.print(markdown)
#     return do_exit(' ', 0)




# In[ ]:


def main_program(interactive=False, window=None):
    # set the local logger
    logger = logging.getLogger(__name__)
    logging.info('*'*50+'\n')

    version_info = f'{constants.app_name} version: {constants.version}\n{constants.contact}\n{constants.git_repo}'
    logging.debug(version_info)    
    logging.debug(f'python version: {sys.version}')
    
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

    logging.debug('processing command line options')
    
    if config['__cmd_line']['version']:
        logging.debug('display version and exit')
        return do_exit(version_info, 0)
    
    if config['__cmd_line']['more_help'] and not interactive:
        logging.debug('display help and exit')
        print_help()
        return do_exit(' ', 0)

    
    # handle missing google shared drive paths
    if not config['main']['drive_path']:
        if interactive:
            print('No Google Shared Drive has been set yet.')
            print('Locate the proper Google Shared Drive **and** then locate the `Student Cumulative Folders (AKA Student Portfolios)` folder')
            drive_path_interactive = window_drive_path()
            if not drive_path_interactive: 
                return do_exit('Please choose a Google Shared Drive to proceed', 0)
            else:
                config['main']['drive_path'] = drive_path_interactive
                update_user_config = True
                
        if not interactive:
            return (do_exit(f'Can not run without a Google Shared Drive Configured.\ntry:\n{sys.argv[0]} -h for help', 1))
    
    # adjust logging levels if needed
    if config['main']['log_level']:
        ll = config['main']['log_level']
        if ll in (['DEBUG', 'INFO', 'WARNING', 'ERROR']):
            logging.root.setLevel(ll)
            handlers = adjust_handler ('*', ll)
            logging.debug(f'adjusted log levels: {handlers} to {ll}')
        else:
            logging.warning(f'unknown or invalid log_level: {ll}')

    logging.debug('loading constants')
    
    # load file constants
    expected_headers = constants.expected_headers    
    student_dirs = constants.student_dirs
    
    # set local vars
    drive_path = Path(config['main']['drive_path'])
    
    # check that supplied path is a valid cummulative folder path
    drive_status = check_drive_path(drive_path)
    if not drive_status[0]:
        return do_exit(drive_status[1], 0)
    
    logging.debug(f'drive status: {drive_status}')

    # get csv_file and drive path
    if interactive:
        print('Select a student export file to process')
        csv_file = window_csv_file()
        if not csv_file:
            return do_exit('Can not proceed without a student export file.', 0)
    else:
        try:
            csv_file = Path(config['__cmd_line']['student_export'])
        except TypeError:
            return do_exit('No student export file specified on command line', 1)
        
    if not csv_file:
        return do_exit('Student export file missing', 1)
    
    logging.debug(f'processing csv file: {csv_file}')
    # read the CSV file
    try:
        print(f'Processing {csv_file}...')
        csv_list = csv_to_list(csv_file)
    except (FileNotFoundError, OSError, IOError, TypeError) as e:
        logging.error(f'could not read csv file: {csv_file.name}')
        logging.error(e)
        return do_exit(e, 1)
    except csv.Error as e:
        logging.error(f'could not process csv file: {csv_file.name}')
        logging.error(e)
        return do_exit(e, 1)
    finally:
        print('done processing')
        
    if interactive:
        window.Refresh()
   
    # map the headers 
    print(f'checking for appropriate column headers')
    header_map, missing_headers = map_headers(csv_list, expected_headers.keys())
    
    if len(missing_headers) > 0:
        return do_exit(f'{csv_file.name} is missing one or more column headers:\n{missing_headers}\n\ncan not proceed with this file', 0)
    
    # validate rows in the CSV file
    print(f'checking each row for valid data')
    valid_rows, invalid_rows = validate_data(csv_list, expected_headers, header_map)
    print(f'{len(valid_rows)} student rows were found and will be processed')
    print(f'{len(invalid_rows)} improperly formatted student rows were found and will be skipped')
    
    if interactive:
        window.Refresh()
    
    # insert the header into the invalid_rows for later output
    invalid_rows.insert(0, csv_list[0])
    
    print(f'\nPreparing to process and create student folders for {len(valid_rows)} students')
    print(f'using Google Shared Drive: {drive_path}')
    print(f'this could take some time...')
    
    if interactive:
        window.Refresh()
    
    directories = create_folders(drive_path=drive_path, valid_rows=valid_rows, header_map=header_map, window=window)
    
    
    print(f'Confirming that student folders were properly created in the cloud')
    confirmed_dirs, unconfirmed_dirs = check_folders(directories, window=window)
    
    
#     return directories, confirmed_dirs, unconfirmed_dirs    
    
    print('Preparing records...')
    if interactive:
        window.Refresh()
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
    
    s = multi_line_string()
    
    s.append('*****Summary*****')
    s.append(f'Processed {len(csv_list)-1} student recods from "{csv_file}"')
    s.append(f'{len(valid_rows)} rows contained valid data and were processed')
    if len_confirmed > 0:
        s.append('-'*10)
        t_str = csv_files["confirmed"]
        s.append(f'\nsend the file below with the PowerSchool Administrator for import')
        s.append(f'*************************\n')
        s.append(f'{t_str}')
        s.append(f'\n*************************')
    
    if len_unconfirmed > 0:
        t_str = csv_files["unconfirmed"]
        s.append('-'*10)
        s.append(f'{len_unconfirmed} rows could not be confirmed')
        s.append(f'review the file below for more information on the failed rows:')
        s.append(f'*************************\n')
        s.append(f'{t_str}')
        s.append(f'\n*************************')
    
    if len(invalid_rows) > 1:
        s.append('-'*10)
        s.append(f'{len(invalid_rows)-1} rows contained invalid data and were skipped')
        s.append('please ONLY use student.export files produced by PowerSchool')
        t_str = csv_files["invalid"]
        s.append(f'review the file below for more information on the invalid rows:')
        s.append(f'*************************\n')
        s.append(f'{t_str}')
        s.append(f'\n*************************')

    

    
    print(s.string)
    if interactive:
        window.Refresh()
    
    if interactive:
        sg.popup(s, title='Summary', font=constants.FONT, keep_on_top=True)
    

    logging.debug('done')
    
    return do_exit('Done - Ready to process another file', 0)




# In[ ]:


run_gui = False
if len(sys.argv) <= 1:
    run_gui = True
    
if '-f' in sys.argv:
    logging.debug('likely running in a jupyter environment')
    run_gui = True


if run_gui:
    # set the global constant for text width
    TEXT_WIDTH = constants.TEXT_WIDTH
    FONT = constants.FONT

    # create a wrapper that matches the text output size
    logging.debug('redefining `print` to use `wrap_print`')
    print = wrap_print
    version_info = f'{constants.app_name} version: {constants.version}\n{constants.contact}\n{constants.git_repo}'
    
    def text_fmt(text, *args, **kwargs): return sg.Text(text, *args, **kwargs)
    layout =[ [text_fmt('Cumulative Portfolio Creator', font=f'{constants.FONT_FACE} {constants.FONT_SIZE+2}')],             
      [text_fmt(version_info, font=f'{constants.FONT_FACE} {constants.FONT_SIZE}')],
      [sg.Text('Create Cumulative Folders on Google Shared Drive', font=f'{constants.FONT_FACE} {constants.FONT_SIZE}')],
      [sg.Output(size=(TEXT_WIDTH+30, 40), font=FONT)],
      [sg.Button('Process File', font=FONT), sg.Button('Change Shared Drive', font=FONT), sg.Button('Help', font=FONT), sg.Button('Exit', font=FONT)],
            ]

    window = sg.Window('Cumulative Portfolio Creator', layout=layout, keep_on_top=False, location=constants.WIN_LOCATION)
    
    bprint('Choose a file to process...')
    window.Refresh()

    while True:
        
        window.finalize()
        window.BringToFront()
        (event, value) = window.read()

        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Process File':
            ret_val = main_program(run_gui, window)
            ret_val()
        if event == 'Change Shared Drive':
            drive = window_drive_path()
            if drive:
                sys.argv.append('-g')
                sys.argv.append(str(drive))
                print(f'Shared drive will be updated to\n{drive}\non next execution.')
                window.Refresh()
            else:
                print('Shared drive will not be updated')
        if event == 'Help':
            print_help()
            window.Refresh()
    window.close()
    sg.easy_print_close()

# run in non-interactive command line mode
else:
    ret_val = main_program()
    ret_val()



from pathlib import Path


# basics #
##########
version = '0.1.00-rc1'
app_name = 'createFolders'
devel_name = 'com.txoof'
contact = 'Aaron Ciuffo -- aaron.ciuffo@gmail.com'
git_repo = f'https://github.com/txoof/{app_name}'

# local root directory -- avoid relative path hell!
_root_dir = Path(__file__).absolute().parent

# config files #
################

# logging configuration
#logging_config = Path('./logging_cfg.ini').absolute()
logging_config = _root_dir/'logging_cfg.ini'
# logging file location
log_file = Path('~/'+app_name+'.log').expanduser().absolute()

# base configuration
config_file = '.'.join((app_name, 'ini'))
# user configuration
config_dir = '.'.join((devel_name, app_name))
user_config_path = Path('~/.config').expanduser()/config_dir/config_file


# runtime constants #
#####################

# number of times to attempt to confirm remote file creation
confirm_retry = 4
# multiplier for each retry cycle - confirm_retry * base_wait
base_wait = 10

# sentry file that program expects to find in root of Cumulative folders dir
sentry_file = 'sentryFile_DO_NOT_REMOVE.txt'

# headers and data types expected in CSV file export from PS
expected_headers ={'LastFirst': str,
                   'ClassOf': int,
                   'Student_Number': int}

# student grade level directories to create:
student_dirs = ['00-Preschool',
                '00-Transition Kindergarten',
                '01-Grade',
                '02-Grade',
                '03-Grade',
                '04-Grade',
                '05-Grade',
                '06-Grade',
                '07-Grade',
                '08-Grade',
                '09-Grade',
                '10-Grade',
                '11-Grade',
                '12-Grade']

# csv output #
##############
# date format YYYY-MM-DD_HH:MM:SS
date_format = "%Y-%m-%d_%H.%M"

# default output path
csv_output_path = Path('~/Desktop/').expanduser()/app_name
# PowerSchool Admin Import CSV filename
csv_output_name = '{date}_Portfolio_Links_for_PowerSchool.csv.txt'

# CSV output dictionary - property name, format string for csv
csv_output_headers = {'LastFirst': '{val}',
                      'ClassOf': '{val}',
                      'Student_Number': '{val}',
                      'webview_link': '<a href={val}>Right click link and *Open Link in New Tab* to view student folder</a>'
                      }

# invalid rows CSV file name
csv_invalid_name = '{date}_Portfolio_Invalid_Rows.csv'

# ERROR CSV output dictionary:
csv_error_name = '{date}_Portfolio_ERRORS.csv'
csv_error_headers = dict(csv_output_headers)
csv_error_headers.update({'error': '{val}', 'matches': '{val}'})

# Strings ERROR output in CSV
csv_error_strings = {'duplicate':
                      'This Student_Number has an existing folder (see the "matches" column), but with a different LastFirst name. Correct the folder name using the webview_link.',
                     'multiple':
                      'Multiple folders exist for this Student_Number. THIS IS NNOT OK. You MUST do the following: 1) choose one of the existing folders. 2) move the contents of the other folders into this folder. 3) Delete the unneeded folders. Use the links in the "matches" column to locate the existing folders',
                     'failed':
                      f'This folder could not be created. Try again later. If the errors persist, check the log file: {log_file}',
                     'other': 
                      f'There was an unknown issue creating this folder. Try again later. If this error persists, check the log file: {log_file}',
                     'created': '',
                     'subdirs': '',
                     'exist': ''
                      }

# GUI Settings #
################

FONT_FACE = 'Courier'
FONT_SIZE = 14
FONT = f'{FONT_FACE} {FONT_SIZE}'
TEXT_WIDTH = 65
TEXT_ROWS = 40

WIN_LOCATION = (80, 80)

POPUP_LOCATION = (WIN_LOCATION[0], WIN_LOCATION[1]+(TEXT_ROWS*FONT_SIZE))

HELP_FILE = './Help.md'

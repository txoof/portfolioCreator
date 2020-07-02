from pathlib import Path

# basics #
##########
version = '0.0.1'
app_name = 'createFolders'
devel_name = 'com.txoof'
contact = 'aaron.ciuffo@gmail.com'
git_repo = f'github.com/txoof/{app_name}'

# config files #
################

# logging configuration
logging_config = Path('logging_cfg.ini')
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

# output format strings #
#########################

## CSV output strings
# URL formatter
url_format = '<a href={}>Right click link and *Open Link in New Tab* to view student folder</a>'


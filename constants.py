from pathlib import Path
# basics
version = '0.0.1'
app_name = 'createFolders'
devel_name = 'com.txoof'
contact = 'aaron.ciuffo@gmail.com'
git_repo = f'github.com/txoof/{app_name}'

# config file locations
config_file = '.'.join((app_name, 'ini'))
config_dir = '.'.join((devel_name, app_name))
user_config_path = Path('~').expanduser()/config_dir/config_file

# logging setup
log_file = Path('~/'+app_name+'.log').expanduser().absolute()
# max log size in bytes
log_size = 1000000


# program specific constants
# sentry file that program expects to find in root of Cumulative folders dir
sentry_file = 'sentryFile_DO_NOT_REMOVE.txt'

# headers and data types expected in CSV file export from PS
expected_headers ={'LastFirst': str, 'ClassOf': int, 'Student_Number': int}

# number of times to attempt to confirm remote file creation
confirm_retry = 4
# multiplier for each retry cycle - confirm_retry * base_wait
base_wait = 10

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

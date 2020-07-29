# Error Messages #

# path does not exist on Google Drive
# Vars: {drive_path}
PATH_ERROR = '''"{drive_path}" does not appear to exist on Google Drive.
Choose a different Drive and folder.'''

# not a valid shared drive
# Vars: {drive_path}
NON_GDRIVE_ERROR = '''"{drive_path}" is not a Google Drive.
Choose a Google Shared Drive.'''

# sentry file error
# Vars: {drive_path}, {sentry_file}
SENTRY_ERROR = '''The file: "{sentry_file}" is missing from the chosen shared drive:
`{drive_path}`

This does not appear to be the correct folder for `Cumulative Student Folders.` 

Choose a different Shared Drive with the button:
#######################
# Change Shared Drive #
#######################

If you are sure 
`{drive_path}` 
is correct, please contact IT Support and ask for help. 

Screenshot or copy this entire text below the line and provide it to IT Support.
###########################################################

IT Support:

This program uses Google File Stream to create student folders on a Google Shared Drive. The Shared Drive should contain a folder called `Student Cumulative Folders (AKA Student Portfolios)` or something similar. 

The program checks for `{sentry_file}` to ensure that the user has selected the appropriate Google Shared Drive **AND** the appropriate folder.

BEFORE PROCEEDING: Confirm that {drive_path} is correct and contains the `Student Cumulative Folders (AKA Student Portfolios)` folder.

The following steps should be run on the user's computer, signed in as the user

1) Check Google File Stream is running on the user's computer and the use is signed in
2) Use Finder to verify the user has access to {drive_path}
3) Check that `Student Cumulative Folders (AKA Student Portfolios)` exists on the Shared Drive above
4) Open `terminal.app` and run the command below

     $ touch {drive_path}/{sentry_file}

5) Try running the program again'''

test = '''this is a string
{drive_path)'''

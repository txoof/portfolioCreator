# createFolders
Create student cumulative folders on Google Drive using Google FileStream using exports from PowerSchool.



## Quick Start
**IMPORTANT if you have never run the application see the [First Run Instructions](#FirstRun) below!**

This assumes you already have [Google FileStream](https://dl.google.com/drive-file-stream/GoogleDriveFileStream.dmg) installed and are signed in as well as a prepared student.export file from PowerSchool.

1. Download the application from [this link](https://github.com/txoof/portfolioCreator/raw/master/createFolders.tgz)
2. Locate the file `createFolders.tgz` -- likely in your `Downloads` folder
3. Double click on the file to decompress it
4. Locate the createFolders icon and drag it into your `Applications` folder
5. Locate the createFolders icon in your `Applications` folder and double click on it to run
    * If you receive error messages or popups preventing you from running the application see the [Help](#Help) section
7. Click "Process File" to begin processing a student.export file from PowerSchool
6. If this is the first time you have run this program, you will be asked to choose a Google Shared drive **and** cumulative student folder. 
    * If you are unsure how to do this, see the [Help](#Help) section
8. When prompted slect a student export file to process by clicking "Browse"
9. Click "Ok" to begin the processing
10. When the process is complete, review the summary
    * A record of the completed tasks is made on your desktop in a folder called `createFolders`
    * Make sure to send the `YYYY-MM-DD_Portfolio_Links_for_PowerSchool.csv` to the PowerSchool Administrator
11. You may process another file immediately if needed

## Instructions
createFolders depends on a working instance of [Google FileStream](https://dl.google.com/drive-file-stream/GoogleDriveFileStream.dmg) installed and signed in with an account that can write to the Student Cumulative Folders shared drive. See the [Help](#Help) section for assistance in setting up FileStream.

### Prepare a student.export.text file
<a name="prepareExport"> </a>
createFolders reads data from PowerSchool exports to create folders in Google Drive and prepare links for the demographics page. This section details the preparation of a student.export.text file that can be used with createFolders.

createFolders will **not create duplicate folders** for existing students and will not create folders when a duplicate student number is found. This means that you can run the same batch of students several times without harm. If a folder already exists, it will simply be checked for consistency and further ignored.

#### Locate Students for Export
Locate any new students in PowerSchool and run a quick export. This query can be very helpful: `Grade_Level=X;DistrictEntryDate>=MM/DD/YYYY`

#### Quick Export Fields
When running a Quick Export the following fileds **must be included**. Any additional fields will be ignored. 
```
LastFirst
Student_Number
ClassOf
```

### Program Opperation
createFolders has only four options when run in graphical mode:
* Process File
* Change Shared Drive
* Help
* Exit

#### Process File
<a name="ProcessFile"></a>

Select a student.export file and create student folders as needed. The student.export file must be in a delimited format such as a tsv or csv with the folowing column headers: `LastFirst, Student_Number, ClassOf`. These fields can be in any order. Additional fields will be ignored.

Data rows must follow the following data types:
* `LastFirst` -- string 
* `Student_Number` -- integer
* `ClassOf` -- integer

Data rows that do not conform will be ignored and recorded in `~/Desktop/createFolders` as a csv file.

Once the opporation is completed, a summary of the completed procedures will open. **READ** all of the summary. There may be some students that could not be processed. 

Share the Links TXT file with the PS Administrator so PowerSchool links can be updated.

A report of any Errors and files that must be sent to the PS Administator is stored in a folder on your Desktop called *createFolders*. **READ** the entire window. Be sure to review the any ERROR files and correct the errors! **YOU MUST** run the application again to create forlders for the students with errors. It is possible to simply process the Error file by selecting it. You may also run the same student export again; duplicate folders will ***not*** be created.
![Summary window](./documentation/summary.png)

#### Change Shared Drive
Choose the shared drive **and folder** where cumulative folders are stored. This is the location where all cumulative folders are stored. createFolders preforms several checks to ensure you have chosen the appropriate drive. For more help see the help section: [Choosing the Shared Drive and Cumulative Student Folder](#ChooseSharedDrive)
![choose the Google Shared Drive and Cumulative folder](./documentation/choose_gdrive.png)

createFolders looks for a specific file called `sentryFile_DO_NOT_REMOVE.txt` in the `Student Cumulative Folders (AKA Student Portfolios)` folder. If this file is missing, createFolders will not proceed. See below for more information in remedying this problem.

Choosing an improper Google Shared drive will result in the following errors:
* Local or Non-Google Drive: `"/Users/spamham/Documents" is not a Google Drive. Choose a Google Shared Drive.`
* Google Drive, but typo in folder name: `"/Volumes/GoogleDrive/Shared drives/ASH Student Cumulative Folders/Student Cumulative Folders (AKA Student Portfolios)TYPO!" does not appear to exist on Google Drive. Choose a different Drive and folder.`
* Google Shared Drive that does not contain **`sentryFile_DO_NOT_REMOVE.txt`**: `This does not appear to be the correct folder for Cumulative Student Folders...`

In the event that the **`sentryFile_DO_NOT_REMOVE.txt`** is not found, double check the following:
1. The appropriate google shared drive is chosen
2. The proper **folder** within the drive is chosen and contains **`sentryFile_DO_NOT_REMOVE.txt`**

If the sentry file is has been deleted or is otherwise missing, a new file can be created by running the following command from the terminal. This command must be run from an account that has FileStream running and with access to the shared drive. **It is critical that you double, tripple and quadruple check that this is actually the correct drive and folder before proceeding.**

`$ touch /Volumes/GoogleDrive/Shared drives/DRIVE NAME/FOLDER NAME/sentryFile_DO_NOT_REMOVE.txt`

#### Program Help
The help button provides a brief version of this document.

#### Exit
Exit the program.

#### Command Line Mode
More debugging features are available on the command line. createFolders will accept student.export files with the `-s [file]` option.

```
$ ./createFolders -h
usage: createFolders [-h] [-s /path/to/student.export.csv]
                     [-g /Volumes/GoogleDrive/Shared drives/ASH Cum Folders/folder/]
                     [-l ERROR, WARNING, INFO, DEBUG] [-v] [--more_help]

optional arguments:
  -h, --help            show this help message and exit
  -s /path/to/student.export.csv, --student_export /path/to/student.export.csv
                        Export from PowerSchool containing: LastFirst,
                        ClassOf, Student_Number
  -g /Volumes/GoogleDrive/Shared drives/ASH Cum Folders/folder/, --google_drive /Volumes/GoogleDrive/Shared drives/ASH Cum Folders/folder/
                        Full path to Google Drive Shared Drive containing
                        cumulative files
  -l ERROR, WARNING, INFO, DEBUG, --log_level ERROR, WARNING, INFO, DEBUG
                        Logging level -- Default: WARNING
  -v, --version         Print version number and exit
  --more_help           Print extened help and exit
```

## Help
### "createFolders" Cannot Be Opened
![unidentified developer window](./documentation/unidentified_devel.png)

This error indicates that the program was not created by an "official" developer. In this case, this is not a problem. Take the following steps to run the program:
1. Locate the program file (likely in your `Applications` folder)
2. Right-click or ctrl-click on the file and choose "Open"
3. A pop-up window will likely appear -- *if no pop-up appears, no further action is needed*
    ![macOS cannot verify the developer](./documentation/cannot_verify_devel.png)
4. Read the text and choose "Open" -- *this will permenently allow you to open this application by double clicking on the icon*
    * If you download a new version of the application, you *may* need to repeat these steps
    
### Choosing the Shared Drive and Cumulative Student Folder
<a name="ChooseSharedDrive"></a>
![choose the Google Shared Drive and Cumulative folder](./documentation/choose_gdrive.png)

createFolders needs to know both which Google Shared Drive to use and the folder where Student Cumulative Folders are stored. The first time you run createFolders, it will ask you to choose the appropriate drive and folder.

1. Click "Browse" to open a folder chooser window
    ![choose a google shared drive](./documentation/folder_picker.png)
    * If FileStream is active and working properly, you will be automatically directed to the Google Drives available to you.
3. Double click the "Shared drives" folder and locate the appropriate folder
    * This is likely called `ASH Student Cumulative Folders` or something similar
4. Locate the folder within the shared drive that contains cumulative folders and click on it
    * This is likely called `Student Cumulative Folders (AKA Student Portfolios)`
5. Click "Choose" to select the folder to return back to createFolders
6. Click "OK" to accept the shared drive
    * createFolders works very hard to ensure you have selected the appropriate drive and will try to prevent you from using an improper folder.
    * You can always change this folder later if you have made a mistake
7. Click "Process File" to begin processing a student.export file

### Setup Google FileStream
<a name="filestream"></a>
Google FileStream is required for createFolders. The user must be signed in with an account that has write permissions to the Student Cumulative folders drive.

1. Download [Google FileStream](https://dl.google.com/drive-file-stream/GoogleDriveFileStream.dmg) and run the installer.
2. Launch Google FileStream if it is not running (look for the icon in the menu bar) and click "Sign in"
    ![filestream icon](./documentation/filestream_ico.png)
3. Use your @ash.nl credentials for an account that has access to the cumulative folders drive.
    * You will likely be asked to sign in using your two-step verification; this is normal
4. Click on the filestream icon in the menu bar and click on the folder icon to view your google drive files
    * It may take several minutes before your folders and files are all visible
5. Browse to the `Shared drives` and locate the `ASH Student Cumulative Folders` drive to confirm you have access
    * If you do not have access, you have likely used an account that does not have permissions. Sign out and try again.
    
### Complete Uninstall
To completely uninstall the application do the following:
1. Remove the executable `createFolders` application
2. From the terminal run `$ rm -rf ~/.config/com.txoof.createFolders`

# FirstRun

The first time you run the Portfolio Creator application you will need to take some special steps:
0. Make sure [Google FileStream{(#filestream) installed.
1. Download the latest version from [here](https://github.com/txoof/portfolioCreator/raw/master/createFolders.tgz)
2. Locate and unpack the applicaton in your Downloads folder
   * Double click to unzip
   * Move into your Applications folder
   * Right click on the createFolders application icon and choose *"Open"*
3. Click *"Process File"* to get started
   * If this is the **very first** time you have run the application it will ask you to choose the Google Shared Drive and the FOLDER where portfolio/cummulative files are stored.
   * Click the *"Browse"* button and find the Google Shared drive likely called *ASH Student Cumulative Folders*
   * Within the *ASH Student Cumulative Folders* drive locate the folder that contains the folder *Student Cumulative Folders (AKA Student Portfolios)* and click *"Choose"* then click *"Ok"* to accept the drive and folder. 
   * If there are any problems, the applicaiton will warn you and stop you from proceeding
   * See [Choosing the Shared Drive and Cumulative Student Folder](#ChooseSharedDrive) for screenshots and more information
4. Create an export from powerschool 
   * See: [Create a Student Export](prepareExport)
5. Click *"Process File"* to process a student export
6. Review

```python
%alias mdc /Users/aaronciuffo/bin/develtools/mdconvert README.ipynb
%mdc
```

    [NbConvertApp] Converting notebook README.ipynb to markdown



```python

```

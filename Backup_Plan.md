# Backup Plan for CreateFolders
If the create folders application is not available, an alternative method can be used for creating student folders manually.

A short video version of these instructions can be found [here](https://drive.google.com/file/d/1K7LQUSNoOL8uj0MYqbRi0WV_58dTYj7J/view?usp=sharing)

<a name="setup"></a>
## Setup
You will need:
* An account with access to the [student cumulative folders shared drive](https://drive.google.com/drive/folders/0AKKRR6NkiaQBUk9PVA)
* Google Chrome -- please make sure you are signed in with an account that has access to the shared drive above (test by clicking the link)
* The student template file available at this link: [Template File] (https://github.com/txoof/portfolioCreator/raw/master/backup/Cumulative_Folder_Template.zip) 

<a name="create_folder"></a>
## Creating a Folder
Make sure you have downloaded the template file in the [previous step](#setup) before proceeding.
1. Double click on the Template File to unzip it and produce a folder named "XXXXXX - LName, FName"
2. Rename the folder so it matches the student ID, LastName, FirstName:
    * `186768 - Lloyd Wright, Frank`
2. Open Google Drive and Browse to the Shared Drive: [ASH Student Cumulative Folders](https://drive.google.com/drive/folders/176UqrsfSHrJX-9AXMzpTm7wtZYfPQj8U)
    * Please use Google Chrome for this -- Safari and Firefox do not always handle uploading folders with sub-folders correctly
3. Locate the correct ClassOf-XXXX Folder for the student and double click to open it
    * If the ClassOf-XXXX folder does not yet exist, you may create one (e.g. for a new group of preschool students)
4. Drag and drop the Template Folder into the the ClasOf-XXXX folder
5. Select and copy the URL at the top of the screen -- you will need this in the next step
6. Repeat steps 1-5 as needed for all new students.

<a name="create_spreadsheet"></a>
## Creating the PowerSchool Data Import for the PS Administrator
The procedure below will generate a TSV document that the PS Administrator can import into PowerSchool. You may add multiple students to the spreadsheet.
1. Open the spreadsheet found [here](https://docs.google.com/spreadsheets/d/1DKuoQ_GjuOzyw07Nq1JXI39n4KJ1hvBT-9XwE-mbuEQ/copy) and make a copy when prompted
2. Enter the Last Name, First Name, ClassOf information
3. Paste the [URL copied in the previous section](#create_folder) into the URL field 
4. The final field will populate automatically
5. Repeat as needed for each new student

## Sending the Data to the PS Administrator
The spreadsheet file must be downloaded as a TSV and sent to the PowerSchool Administrator for import into powerschool. Use the [spreadhseet created in the previous step](#create_spreadsheet) to complete these steps.
1. Open the spreadsheet if it is not already open
2. Click on the sheet tab "WebView Links For PowerSchool"
3. Click *File > Download > Tab-Separated Values*
4. Download the file
5. Create an email and attach the file. Send the email to the PowerSchool Administrator with the subject line "Cumulative Folder/Portfolio Links for PowerSchool Import"






```python
!jupyter-nbconvert --to markdown Backup_Plan.ipynb

```

    [NbConvertApp] Converting notebook Backup_Plan.ipynb to markdown
    [NbConvertApp] Writing 3167 bytes to Backup_Plan.md



```python

```

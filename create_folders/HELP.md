# createFolders
This program creates student cumulative folders on Google Shared Drives using records pulled from PowerSchool. It is intended to be used by ASH employees that have admin access to PowerSchool learning and edit access to the Student Cumulative Folders on Google Drive.

## Running the Program
Make sure you have the latest version. The latest version can be found on GitHub - see the title bar of the application for the exact URL.

Before you get can begin creating folders on Google Drive, you will need a `Quick Export` from PowerSchool with the appropriate information. The program will only create **new** folders when they are needed. It will not create duplicate folders if you accidentally run the same `student.export.txt` multiple times.

### Get a student.export.txt file
* Sign in to PowerSchool with an admin account and run a `Quick Export` with the following fields:
    - `LastFirst`, `Student_Number`, `ClassOf`
    - use a query similar to this to find recently enrolled students that may be missing Cumulative Folders: `Grade_Level=3;DistrictEntryDate>=07/31/2018`

### Process the export file
Once you have a `student.export.txt` file downloaded from PowerSchool, you can begin processing the file.

* Click the `Process File` button to get started
* If this is the first time you have run this program you will be prompted to select a Google Shared Drive
    - Locate the Google Shared Drive that contains the `Student Cumulative Folders` folder. 
    - Make sure you select the correct Drive and the correct folder.
        - The program will not allow you to continue if you select an improper drive.
* You will now be prompted to select a `student.export.txt` file. This is typically found in the `Downloads` folder.
    - Select the downloaded `student.export.txt` file
* The program will process the export file and provide some information about the progress. 
    - It may take a long time to process all of the students. This is normal.
    
### Review the output
When the program completes processing the export, it will provide a summary. Review the summary for any problems.

* A folder will be created on your `Desktop` that contains data for the PowerSchool Administrator and information about any problems.
* Example files:
    - `2020-04-11_12.25_Portfolio_Links_for_PowerSchool.csv` -- Contains all of the successfully processed students.
        * Send this to the PowerSchool Administrator
    - `2020-04-11_12.25_Portfolio_Invalid_Rows.csv` -- Contains any rows that contain "bad" data in the `LastFirst`, `Student_Number`, `ClassOf` columns such as letters or spaces in the `Student_Number` or `ClassOf` column.
        * Review this file to see which students were not processed.
    - `2020-04-11_12.25_Portfolio_ERRORS.csv` -- Contains any rows that generated errors
        * The file contains the entire row as well as more detailed information. **YOU MUST REVIEW THIS**
        
## Getting More Help
Check the GitHub Repository for more detailed instructions with tutorials, images and detailed contact information -- see the title bar above in this applicaiton for the exact URL. 

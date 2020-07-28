#!/usr/bin/env python
# coding: utf-8


# In[1]:


#get_ipython().run_line_magic('alias', 'nb_convert ~/bin/develtools/nbconvert filestream.ipynb')




# In[8]:


#get_ipython().run_line_magic('nb_convert', '')




# In[ ]:


import logging
logger = logging.getLogger(__name__)




# In[4]:


# import class_constants
from . import class_constants
from pathlib import Path
import subprocess
import os
import glob




# In[ ]:


class GoogleDrivePath():
    def __init__(self, path=None):
        '''google drive filestream path class for files and directories
        
        Attributes:
            path(`str`): path to google drive filestream object
            root(`str`): parent path if object is a file, else same as path
            confirmed(`bool`): local object has synced over filestream
            is_file(`bool`): True when object is a file, not a directory
            file_id(`list`): unique Google Drive identifier 
            webview_link(`str`): full url to object'''
        self.confirmed = False
        self._file_base = class_constants.file_base
        self._dir_base = class_constants.dir_base
        self.is_file = False
#         self.exists = False
        self.path = path
    
    @property
    def path(self):
        '''full local path to google dirve filestream object
        
        Args:
            path(`str` or `Path`): /path/to/object
            
        Sets Attributes:
            self.path: path to object
            self.root: same as path for directories, parent directory for files
            self.is_file: true for files and file-like objects, false for directories'''
        return self._path
    
    @path.setter
    def path(self, path):
        if not path:
            self._path = None 
        else:
            self._path = Path(path)
            if self._path.is_dir() and self._path.exists():
                self.root = self._path
                self.is_file = False
#                 self.exists = True
            if self.path.is_file() and self._path.exists():
                self.root = self._path.parent
                self.is_file = True
#                 self.exists = True
            
            if not self._path.exists():
                self.is_file = False
                self.root = self._path.parent
#                 self.exists = False

#     @property
    def exists(self):
        '''check if root AND path exits on the local file system
        for file objects, root and path are checked separately, return False if either does not exist
        for directory objects, root and path are the same, return False if either does not exist
        
        Returns:
            `bool`: true if both root and path exist'''
        root_exists = self.root.exists()
        path_exists = self.path.exists()
        return (root_exists and path_exists)
                
    @property
    def file_id(self):
        '''unique file id for each object (directories or file)
        
        Args:
            path(`str` or `Path`): path to object; defaults to self.path
        
        Returns:
            `list` of `str` containing the file id'''
        try:
            file_id = self.get_xattr('user.drive.id')
        except FileNotFoundError as e:
            logging.info(f'\'{self.path}\' does not appear to exist; cannot get attributes')
            file_id = None
        return file_id                

    @property
    def webview_link(self, confirm=True):
        '''full webview link to object in google drive'''
        self._webview_link = None
        
        file_id = None
        self._webview_link = None
        
        if confirm:
            self.confirm()
        
        if self.exists() and self.confirmed:
            try:
                file_id = self.file_id
            except FileNotFoundError:
                file_id = None


            if len(file_id) < 1:
                file_id = None
            else:
                file_id = file_id[0]

            if not self.is_file and file_id:
                self._webview_link = f'{self._dir_base}{file_id}'

            if self.is_file and file_id:
                self._webview_link = f'{self._file_base}{file_id}'
            
        return self._webview_link
            

    def get_xattr(self, attribute, path=None):
        '''get the extended attributes of a file or directory
        for more see: https://stackoverflow.com/questions/51439810/get-google-drive-files-links-using-drive-file-stream
        
        Args:
            attribute('`str`'): attribute key to access

        Returns:
            `list` - attribute or key: attribute pairs
            
        Raises:
            FileNotFoundError - file or directory does not exist
            ChildProcessError - xattr utility exits with non-zero code 
                This is common for files that have no extended attributes or do not
                have the requested attribute'''
        if not path:
            path = self.path
        else:
            path = Path(path).absolute()
            
        attributes = []
        if not path.exists():
            raise FileNotFoundError(self.path)

        p = subprocess.Popen(f'xattr -p  {attribute} "{path.resolve()}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            attributes.append(line.decode("utf-8").strip())
    #         attributes = attributes + line.decode("utf-8").strip()
        retval = p.wait()
        if retval != 0:
            raise ChildProcessError(f'"{path}" is likely not a google filestream object: xattr exited with code {retval}')
        return attributes    
    
    
    def children(self, path=None, max_depth=1, pattern="*", child_type='all'):
        '''return list of all child objects in a path matching  `pattern` glob of `child_type` 
        
        to an arbitrary `max_depth`

        Args:
            path(`str`): path to recurse
            pattern(`str`): pattern to match (default "*")
            child_type(`str`): "all" files and dirs (default); "file" file only; "dir" directory only

        Returns:
            `list`

        based on: https://codereview.stackexchange.com/questions/161989/recursively-listing-files-in-python/162322'''
        if not path:
            path = self.path
        output = []
        known_child_types = {'all': os.path.exists, 
                             'file': os.path.isfile, 
                             'dir': os.path.isdir}
        if not child_type in known_child_types.keys():
            raise ValueError(f'"{child_type}" not a known type: {[k for k in known_child_types.keys()]}')
        else:
            func = known_child_types[child_type]

        for depth in range(0, max_depth):
            search_path = os.path.join(path, *("*" * depth), pattern)
            output.extend(filter(func, glob.iglob(search_path)))
        return output
    
    def mkdir(self, path=None, parents=False, exist_ok=False, **kwargs):
        '''create a directory using pathlib.Path().mkdir()
        
        Args:
            path(`str` or `Path`): path to create
            parents(`bool`): create parent directories - default false
            exists_ok(`bool`): do not raise error if directory exists
            kwargs: kwargs for pathlib.Path().mkdir()
            
        Returns:
            `list` containing file_id'''
        if not path:
            path = self.path
            logging.debug(f'using self.path: {path}')
        else:
            logging.debug(f'using supplied path: {path}')
            
        if path.is_file():
            raise TypeError(f'{path} is a file')
            
        path = Path(path)
            
        path.mkdir(parents=parents, exist_ok=exist_ok, **kwargs)
#         if self.confirm(path):
        file_id = self.get_xattr('user.drive.id', path)
        return file_id        
    
    def confirm(self, path=None):
        '''confirm that an object has been synced over filestream 
        
        Args:
            path(`str` or `Path`): path to object; default is self.path
        
        Returns:
            `list` of `str` containing the file id
            
        Attributes Set:
            self.confirmed: True when object has been sent'''
        
        if not path:
            path = self.path
        file_id = self.file_id
        
        if file_id:
            if 'local-' in file_id[0]:
                self.confirmed = False
                file_id = None
            else:
                self.confirmed = True
        return file_id
    
    @classmethod
    def mkchild(cls, path, create_now=False, **kwargs):
        '''Factory - create child directory and return a GoogleDrivePath object
        
        Args:
            path(`pathlib.Path`): path to create
            create_now(`bool`): True create immediately
            kwargs: additional keyword arguments to pass on to pathlib.Path().mkdir()
        Returns:
            GoogleDrivePath object with path set'''
        
        child = cls(path=path)
        if create_now:
            child.path.mkdir(**kwargs)
        return child
    
    def __repr__(self):
        return f'GoogleDrivePath({self.path})'
    
    def __str__(self):
        return f'{self.path}'    




# In[ ]:


class GDStudentPath(GoogleDrivePath):
    def __init__(self, root=None, ClassOf=None, Student_Number=None, LastFirst=None):
        '''student directory in google drive; child class of GoogleDrivePath
        
        Student directories are constructed from root/Class Of-YYY/Last, First - Student_Number:
        /Volumes/GoogleDrive/Shared drives/Cumm Drive/Cumm Folders/Class Of-2020/Flynn, Erol - 123567
        
        Args:
            root(`str`): root directory for student paths ( /Volumes/GoogleDrive/Shared drives/Cumm Drive/Cumm Folders/)
            ClassOf(`str`): "Class Of-YYYY" string representation of projected graduation year
            LastFirst(`str`): "Last, First" string representation of student name
            Student_Number(`int`): student id number
            
        Properties:
            ClassOf(`str`): "Class Of-YYYY" string representation of projected graduation year
            LastFirst(`str`): "Last, First" string representation of student name
            Student_Number(`int`): student id number
            matches(`dict`):  name and webview link of directories that contain "id_number"
            duplicate(`bool`): True this object's Student_Number matches an existing record, 
                but this object's LastFirst does not match one or more existing objects
            path_parts(`dict`): path compontents stored as dictionary keys'''
        super(GDStudentPath, self).__init__(path=root)
        self.matches = {}
        self.duplicate = False
        self.path_parts = {'ClassOf': None, 'Student_Number': None, 'LastFirst': None}
        self.ClassOf = ClassOf
        self.LastFirst = LastFirst
        self.Student_Number = Student_Number
        
        
    def __repr__(self):
        return f'GDStudentPath({self.path})'
        
        
    def __str__(self):
        return f'{self.path}'
    
    
    def _set_path(self):
        '''attempt to set the path based on the root and the path_parts once they are all set'''
        for key in self.path_parts:
            if not self.path_parts[key]:
                self._path = None
                break
            else:
                student_dir = f"Class Of-{self.path_parts['ClassOf']}/{self.path_parts['LastFirst']} - {self.path_parts['Student_Number']}"
                student_dir = f'{str(self.root)}/{student_dir}'
                self._path = Path(student_dir)
        return self._path
            
    
#     @property
#     def exists(self):

    def exists(self):
        '''check if self.path exists
        *** overrides class method
        
        Returns:
            `bool`: True if object exists on local file system'''
        if not self._path:
            exists = False
        else:
            exists = self.path.exists()
        return exists
    
    def check_similar(self):
        '''check for similarly named directories based on student id number 
        within the root/Class Of-XXXX/ directory
        
        Properties Set:
            self.matches(`dict`): dictionary of similar directories
        Returns:
            `bool`: True if matching directories found'''
        similar = False
        matches = {}
        if self.path:
            classof_path = f"Class Of-{self.path_parts['ClassOf']}"
            search_path = self.root/classof_path
            logging.info(f'checking for similar existing dirs in {search_path}')
            glob = f"*{self.path_parts['Student_Number']}*"
            for i in search_path.glob(glob):
                logging.debug(f'examining {search_path/i}')
                match_id = self.get_xattr('user.drive.id', search_path/i)
                if i.absolute().is_dir():
                    url = '/'.join((self._dir_base, match_id[0]))
                else:
                    url = '/'.join((self._file_base, match_id[0]))
                matches[str(i)] = url
            
        
        # multiple matches are found; indicates there exist multiple duplicate records
        if len(matches) > 1:
            logging.warning(f'{len(matches)} exist')
            self.duplicate = True

        # a match is found and self.path does not exist indicates that this is a duplicate record, but 
        # with a name chagne eg. exists: Doe, Jon - 123456 and this record is Doe, John - 123456
        if (len(matches) == 1) and (not self.exists()):
            logging.warning(f'Student_Number: "{self.Student_Number}" matches existing object: {matches}')
            logging.warning(f'this object appears to be a duplicate')
            self.duplicate = True
        self.matches = matches
        return matches
    
    
    @property
    def ClassOf(self):
        return self.path_parts['ClassOf']
    
    @ClassOf.setter
    def ClassOf(self, ClassOf):
        '''string representation of projected graduation date in format: "Class Of-YYYY"
        
        Properties Set:
            path_parts(`dict`): dictionary of component parts of path'''
        if not ClassOf:
            self.path_parts['ClassOf'] = None
        else:
            # attempt to coerce strings from cSV file into type int
            ClassOf = int(ClassOf)
            if not isinstance(ClassOf, int):
                raise TypeError('class_of must be of type `int`')
        self.path_parts['ClassOf'] = f'Class Of-{ClassOf}'
        self.path_parts['ClassOf'] = ClassOf
        self._set_path()
        
        
    @property
    def LastFirst(self):
        return self.path_parts['LastFirst']
    
    @LastFirst.setter
    def LastFirst(self, name):
        '''string representation of "Last, First" names
        
        Properties Set:
            path_parts(`dict`): dictionary of component parts of path'''
        if not name:
            self.path_parts['LastFirst'] = None
        else:
            if not isinstance (name, str):
                raise TypeError('name must be of type `str`')
        self.path_parts['LastFirst'] = name
        self._set_path()
        
    @property
    def Student_Number(self):
        return self.path_parts['Student_Number']
    
    @Student_Number.setter
    def Student_Number(self, number):
        '''integer of student id number
        
        Properties Set:
            path_parts(`dict`): dictionary of component parts of path'''
        if not number:
            self.path_parts['Student_Number'] = None
        else:
            # try to coerce number into type int
            number = int(number)
            if not isinstance (number, int):
                raise TypeError('id_number must be of type `int`')
        self.path_parts['Student_Number'] = number  
        self._set_path()

    def mkchild(self, path, create_now=False, **kwargs):
        '''Factory - generates GoogleDrivePath objects and associated paths on file system
        **overrides GDStudentPath inherited mkchild to return a pure GoogleDrivePath object
        
        Args:
            path(`pathlib.Path`): path to create
            create_now(`bool`): True create immediately
            kwargs: additional keyword arguments to pass on to pathlib.Path().mkdir()
            
        Returns:
            `GoogleDrivePath` object'''
        child = GoogleDrivePath(self.path/path)
        if create_now:
            child.mkdir(**kwargs)
        return child
                                    
    def mkdir(self, **kwargs):
        '''make the student directory
        **overrides base class mkdir'''
        if not self.path:
            raise TypeError(f'"{type(self.path)}"" object is not a Path() object')
        file_id = super(GDStudentPath, self).mkdir(self.path, exist_ok=True, parents=True, **kwargs)
        return file_id
    




# In[ ]:


def main():
    my_drive = GoogleDrivePath('/Volumes/GoogleDrive/My Drive')
    
    if not my_drive.path.parent.exists():
        print(f'{my_drive.parent} could not be found. Is Google Filestream Running and are you signed in?')
        return
    
    try:
        print(f'My Drive ID: {my_drive.file_id}')
        print(f'My Drive WebView Link: {my_drive.webview_link}')
        print(f'My Drive x-attributes:\n{my_drive.get_xattr("user.drive.itemprotostr")}' )
    except ChildProcessError as e:
        print(f'error accessing {my_drive.path}. Is Google Filestream Running and are you signed in?')

if __name__ == '__main__':
    main()




# In[ ]:






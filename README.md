# excel2web2py
Parse excel file and create a web app with _web2py_ 2.14.3

__Author__ : Tanguy Jourde  
__Supervisor__ : Chambon Laurent

_Python 2.7_ is needed

Functionalities :
----------------
Define a database in the databases folder of the application TEMPLATE in web2py from an excel file.  
Upon visiting the web2py server, you are able to access and search specific content from the excel file.  
You are also being able to insert, update and delete data if you are logged in as an authentified user.

Before Installation :
---------------------

__Excel:__

The excel file's name cannot contain special characters or spaces.  
The name of the first sheet is used as the name of the table and the first element of the first row defines the names of the columns of the database so they both should not contain special characters.  
Separate elements with the '|' (or "pipe") sign. 

Keywords to use to define the table with an example:
- Nom_francais|type='string'|length=30|notnull=False|unique=True|reference=Nom_anglais|idthis
- type can be integer,float,string
- length : the number of characters in one cell.
- notnull : means that if True, prevent a new row to be inserted if the row contains an empty cell on this column.
- unique : means that if True, prevent 2 rows to have the same value on this column.
- reference="" : means that you want to link values to another sheet with the same name
- idthis: means that values on this column represent the row instead of the row's number.

__Programs:__

You will need to install web2py.

You will also need to install these modules before deploying the application:
- xlrd 0.9.4 to read excel files
- sys to perform some basic system operations
- os to retrieve informations on the system
- time to retrieve the time on the machine
- errno to retreive errors
- logging to create logs of the code
- sqlite3 to use databases
- subprocess to use threads and multi-execution

On Unix, install these packages through the terminal using your favorite package manager.  
Example: `apt-get install xlrd`

You may need to execute those operations as an administrator though(put `sudo` first before an install adn input the admin's password)

Installation :
--------------
__Unix :__ 

unzip the folder in your web2py folder, where web2py.py and applications are located
run these commands : 
> cd path/to/web2py && python web2py.py

Then input the password for the administrator of the web2py server  
Launch the server  
Then navigate to /admin/site  
Look to Upload application and input __TEMPLATE__ for the application's name  
Select the .w2p file  
Install  
Close the server  
Then run these commands:
> cd excel2web2py && python script.py path/to/nameExcelfile

Then input the password for the administrator of the web2py server  
For now, it is only accessible at _127.0.0.1:8000_  
If the page is not launched automatically, launch a web browser and type in the address bar the address above or under this line.  
You are now located at 127.0.0.1:8000/TEMPLATE/default/index.html

__Bugs :__

If the page cannot load (syntax error __init__.py), refresh the page (fixed : removed __init__.py + pyc w/o repercussions so far)

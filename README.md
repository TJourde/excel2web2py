# excel2web2py
Parse excel file and create a web app
with web2py 2.14.3
Author : Tanguy Jourde
Supervisor : Chambon Laurent

Needed to run this program : python 2.7 , xlrd 0.9.4

Functionalities :

Generate a db file(not use for now) and define a database in the databases folder of the application TEMPLATE in web2py from an excel file.
Upon visiting the web2py server, you are able to access and search specific content from the excel file.

Before Installation :

The excel file's name cannot contain special characters or spaces.
The name of the first sheet is used as the name of the table and the first element of the first row defines the names of the columns of the database 
so they both should not contain special characters. 
Separate elements with the '|' (or "pipe") sign. 
Keywords to use to define the table with an example:
Nom francais|type='string'|length=30|notnull=False|unique=True
type can be integer,float,string
length : the number of characters in one cell.
notnull : means that if True, prevent a new row to be inserted if the row contains an empty cell on this column.
unique : means that if True, prevent 2 rows to have the same value on this column.

Codes|idthis: means that values on this column represent the row instead of the row's number.

You will need to install web2py.

You will also need to install these modules before deploying the application:
-xlrd 0.9.4 to read excel files
-sys to perform some basic system operations
-os to retrieve informations on the system
-time to retrieve the time on the machine
-errno to retreive errors
-logging to create logs of the code
-sqlite3 to use databases
-subprocess to use threads and multi-execution

On Unix, install these packages through the terminal using your favorite package manager.
Example: apt-get install xlrd
You may need to execute those operations as an administrator though(put sudo first before an install)

Installation :
Unix : 
unzip all files in the same folder
run these commands : 
cd pathUnzippedFolder
python script.py pathtonameExcelfile

then input the password for the administrator of the web2py server

for now, it is only accessible at 127.0.0.1:8000

if the page is not launched automatically,
launch a web browser and type in the address bar that address

You are now located at web2py/TEMPLATE/default/index.html

Bugs :  if the page cannot load (syntax error __init__.py), refresh the page (fixed : removed __init__.py + pyc w/o repercussions so far)

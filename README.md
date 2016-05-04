# excel2web2py
Parse excel file and create a web app with _web2py_ 2.14.3

__Author__ : Tanguy Jourde  
__Supervisor__ : Chambon Laurent

_Python 2.7_ is needed, more on that below with matplotlib

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
- Nom_francais|type='string'|reference=Nom_anglais|idthis
- type can be integer,float,string
- reference="" : means that you want to link values to another sheet with the same name
- idthis: means that values on this column represent the row instead of the row's number.

__Programs:__

To run commands, use the terminal on Unix and the command console on Windows  

You will need to install web2py.

You will also need to have these modules installed before deploying the application:
- xlrd 0.9.4 to read excel files
- sys to perform some basic system operations
- os to retrieve informations on the system
- time to retrieve the time on the machine
- errno to retrieve errors
- logging to create logs of the code
- sqlite3 to use databases
- subprocess to use threads and multi-execution
- matplotlib to create plots  

__Important__: It is highly recommended to download Python(x,y) as it comes packaged with many modules needed to run matplotlib, only if you have not already installed Python 2.7.  
If you have, you want to check out the documentation [here](http://matplotlib.org/users/installing.html#windows) to lookup what modules you will need to install.

__Unix:__   
On Unix, install these packages through the terminal using your favorite package manager.  
Example: `apt-get install xlrd`

__Windows__:  
You will have to download python 2.7, follow the instructions on the official website  
Xlrd is packaged with this application, run :
> cd path/to/xlrd  
python setup.py install

You may need to execute those operations as an administrator though(put `sudo` first before an install adn input the admin's password)

Installation :
--------------

unzip the folder in your web2py folder, where web2py.py and applications are located  
copy TEMPLATE to the applications folder in web2py

Then run these commands:
> Unix: cd excel2web2py && python script.py path/to/nameExcelfile  
Windows: cd excel2web2py && python script.py path\to\nameExcelfile

Then input the password for the administrator of the web2py server  
For now, it is only accessible at _127.0.0.1:8000_  
If the page is not launched automatically, launch a web browser and type in the address bar the address under this line.  
You are now located at __127.0.0.1:8000/TEMPLATE/default/index.html__

To relaunch your server without import files, you will need to launch it from web2py.exe(Windows) or web2py.py(Unix)  
On Unix, run these commands : 
> cd path/to/web2py && python web2py.py

On Windows, simply execute it.

__Bugs :__ Matplotlib may not load correctly
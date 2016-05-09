# excel2web2py
Parse excel file and create a web app with _web2py_ 2.14.3

__Author__ : Tanguy Jourde  
__Supervisor__ : Chambon Laurent

_Python 2.7_ is needed, more on that below with matplotlib

Functionalities :
----------------

The main purpose of this application is to generate a database from an Excel file on web2py.  
Upon visiting the web2py server, you are able to access and search specific content from the excel file.  
You are also being able to insert, update and delete data if you are logged in as an authentified user.  
You can also create plots from columns containing only numbers : a picture will appear on the page showing the plot(s) with the column(s) selected.  

Before Installation :
---------------------

__Excel:__

The excel file's name cannot contain special characters or spaces.  
It will be used to create a SQL Table, so it must respect the same constraints.

The name of the first sheet is used as the name of the table and the first element of the first row defines the names of the columns of the database so they both should not contain special characters.  
Separate elements with the '|' (or "pipe") sign. 

Look at this example to get a better picture of what is expected to be present on the first cell of a column:  
> Nom_francais|type='string'|reference=Nom_anglais|idthis  

The first element is used to generate the SQL Table, it also must follow the same rules that a SQL Table's name does.  

Keywords to use to define the table with an example: 
- _type_ can be integer,float,string  
- _reference_= Another_Table : means that you want to link values to another sheet with the same name; it will display elements from that table on the page.  
- _idthis_: means that values on this column represent the row instead of the row's number; it will be useful when you are linking tables with reference as it will use data from that column.

If you do not define yourself the type of a column, the program can still work but the data may not be formatted the way it is meant; for example, integers may be typecasted to floats.  
Also, reference and idthis can only work on column containing only integers.  Don't forget to put a '|' at the end of each number 
A file called _Test_ has been joined to complete these explanations.

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
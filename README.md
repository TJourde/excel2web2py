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

The excel file cannot contain special characters or spaces.
The name of the first sheet is used as the name of the table and the first row defines the names of the columns of the database 
so they both should not contain special characters (but can have spaces, they will be replaced by "_")


Installation :
Unix : 
unzip all files in the same folder
install xlrd
run these commands : 
cd pathUnzippedFolder
python script.py nameExcelfile

then input the password for the administrator of the web2py server

for now, it is only accessible at 127.0.0.1:8000

launch a web browser and type in the address bar this address

You are now located at web2py/TEMPLATE/default/index.html

Bugs : if the page cannot load (syntax error __init__.py), refresh the page
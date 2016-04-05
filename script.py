#!usr/bin/env/python
# -*- coding: utf-8 -*-
import sys, os, time, errno
import os.path
import sqlite3
#lib read excel files
import xlrd
import subprocess

path=""

def creationDossier():
	global path
	localtime = time.localtime(time.time()) #heure machine
	timedate = str(localtime[0])+'_'+str(localtime[1])+'_'+str(localtime[2])
	if os.name =="nt":
		path="C:\\TMP\\"+timedate+'\\'
	else:
		path="/tmp/"+timedate+'/'
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
	#os.chdir(path) # change de répertoire courant


if( len(sys.argv)>1 ):
	
	
	if(" " in sys.argv[1]):
		sys.exit("Erreur: le nom du fichier contient des espaces")

	try:
		sys.argv[1].encode('ascii')
	
	except (UnicodeError):
		sys.exit("Erreur: le nom du fichier n'est pas unicode")

	try:
		#workbook doesn't need to be explicitly closed
		wb = xlrd.open_workbook(sys.argv[1])
	except(IOError):
		sys.exit("Erreur: le fichier n'a pas pu être consulté")

	# get name of first sheet
	sh = wb.sheet_by_name(wb.sheet_names()[0])

	# get names of columns (1st row value)
	namecol = []
	for colnum in range(sh.ncols):
		 namecol.append(sh.col_values(colnum)[0])

	print("Sheet: "+ wb.sheet_names()[0])
	for i in namecol:
		print("Column: "+i)


	#erase old db
	creationDossier()
	if(os.path.isdir(path)):
		if(os.path.isfile(path+sys.argv[1].split('.')[0]+".db")):
			os.remove(path+sys.argv[1].split('.')[0]+".db")
	

	#db
	print (path)
	print(str(path)+sys.argv[1].split('.')[0]+".db")
	conn = sqlite3.connect(path+sys.argv[1].split('.')[0]+".db")
	c = conn.cursor()


	# Create table
	s ='CREATE TABLE "'+ wb.sheet_names()[0]+'"('
	for i in namecol:
		s+='"'+i+'",'
	s=s[:-1]
	s+=')'
	c.execute(s)

	# Insert a row of data
	#c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()
	
	#var a creer : logs/log	

	from subprocess import call
	try:
		subprocess.check_call(["cp","-R", path+'.',"web2py/applications/TEMPLATE/tmp/"])
	except subprocess.CalledProcessError:
		sys.exit("Erreur: "+path+", web2py ou un de ses dossiers a disparu de l'emplacement prévu")

	try:
		subprocess.check_call(["python", "web2py/web2py.py"])
	except subprocess.CalledProcessError:
		sys.exit("Erreur: python n'est pas présent sur la machine ou web2py a changé d'emplacement")

else:
	print("Erreur : pas de fichier sélectionné")

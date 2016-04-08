#!usr/bin/env/python
# -*- coding: utf-8 -*-
import sys, os, time, errno
import os.path
import sqlite3
#lib read excel files
import xlrd
import subprocess



def createFolder():
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
	finally:
		return path
	#os.chdir(path) # change de répertoire courant

def fileWellFormatted(pathFile):
	if(" " in pathFile):
		sys.exit("Erreur: le nom du fichier contient des espaces")

	try:
		pathFile.encode('ascii')
	
	except (UnicodeError):
		sys.exit("Erreur: le nom du fichier n'est pas unicode")

def tryOpenWorkbookFile(pathFile):
	try:
		#workbook doesn't need to be explicitly closed
		wb = xlrd.open_workbook(pathFile)
		return wb
	except(IOError):
		sys.exit("Erreur: le fichier n'a pas pu être consulté")

def getSheet(wb):
	sh = wb.sheet_by_name(wb.sheet_names()[0])
	return sh

def getSheetName(sh):
	return getattr(sh,"name")

def getNameFirstSheetAsTableName(wb):
	# get name of first sheet
	try:
		wb.sheet_names()[0].encode('ascii')
	
	except (UnicodeError):
		sys.exit("Erreur: le nom de la feuille n'est pas unicode")
	
	shname = wb.sheet_names()[0].replace(" ","_").replace("(","").replace(")","")
	return shname

def getColumnsNames(sheet,shname):
	# get names of columns (1st row value)
	namecols = []

	for colnum in range(sh.ncols):
		try:#necessary or else db attributes will look funny 
			sh.col_values(colnum)[0].encode('ascii')
	
		except (UnicodeError):
			sys.exit(sh.col_values(colnum)[0]+"Erreur: Nom de colonne n'est pas unicode")

		namecols.append(sh.col_values(colnum)[0].replace(" ","_").replace("(","").replace(")",""))

	print("Sheet: "+ shname)
	for i in namecols:
		print("Column: "+i)

	return namecols

def requestCreateTable(name,namecols):
	s ='CREATE TABLE "'+ shname+'"(id,'
	for i in namecols:
		s+='"'+i+'",'
	s=s[:-1]
	s+=')'
	return s

def insertRowsData(nameTable,sheet,cursor):

	query = ""
	idcpt = 0
	firstline=True
	for rownum in range(sheet.nrows):
		if(not firstline):
			query = "INSERT INTO "+nameTable+" VALUES ("+str(idcpt)+","
			for rowval in sheet.row_values(rownum):
				#if ((rowval != "")and(not rowval.isspace())):
				query+='"'+rowval+'"'+','
			query=query[:-1]
			query+=')'
			idcpt+=1
		else:
			firstline=False
		cursor.execute(query)

path=str(createFolder())
#if there is at least an argument, the script is launched
if( len(sys.argv)>1 ):
	
	fileWellFormatted(sys.argv[1])
	wb = tryOpenWorkbookFile(sys.argv[1])
	sh = getSheet(wb)
	shname = getNameFirstSheetAsTableName(wb)
	namecols= getColumnsNames(sh,shname)
	

	#if(os.path.isdir(path)):
	#	if(os.path.isfile(path+sys.argv[1].split('.')[0]+".db")):
	#		os.remove(path+sys.argv[1].split('.')[0]+".db")
	
	#db
	print ("Path: "+path)
	#print("Db :"+str(path)+sys.argv[1].split('.')[0]+".db")
	conn = sqlite3.connect("web2py/applications/TEMPLATE/databases/storage.sqlite")
	#path+sys.argv[1].split('.')[0]+".db")
	c = conn.cursor()

	#Remove old table
	try:
		c.execute("DROP TABLE "+shname)
	except:
		pass

	#Create table
	c.execute(requestCreateTable(shname,namecols))

	# Insert rows of data
	insertRowsData(shname,sh,c)

	# Save (commit) the changes
	conn.commit()

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()
	#var a creer : logs/log	

	from subprocess import call
	#subprocess.call(["rm","-R","web2py/applications/TEMPLATE/tmp/"])
	try:
		subprocess.check_call(["cp","-R", path+'.',"web2py/applications/TEMPLATE/tmp/"])
	except subprocess.CalledProcessError:
		sys.exit("Erreur: "+path+", web2py ou un de ses dossiers a disparu de l'emplacement prévu")

	try:
		subprocess.check_call(["cp","web2py/applications/TEMPLATE/models/db_backup.py","web2py/applications/TEMPLATE/models/db.py"])
	except subprocess.CalledProcessError:
		sys.exit("db_backup n'est plus présent")	

	with open("web2py/applications/TEMPLATE/models/db.py","a") as f:
		#getDb -> called from default.py to get the same db as db.py
		f.write('\ndef getDb():\n    module_path=os.path.abspath(os.path.dirname(__file__))\n    dbpath = module_path + "/../databases"\n    db_name = "storage.sqlite"\n    db = DAL("sqlite://"+ db_name ,folder=dbpath, auto_import=True)\n    return db')
		#getTable -> called from default.py to get the table generated
		f.write('\ndef getTable(db):\n    return db.'+shname)
		#Create table
		#f.write('\ndb.define_table("'+shname+'"')
		
		#for i in namecols:
		#	f.write(',Field("'+i.encode('utf8')+'")')
		#f.write(')')

		# Insert rows of data
		#firstline=True
		#for rownum in range(sh.nrows):
		#	if(not firstline):
		#		query = "INSERT INTO "+shname+"("
		#		for i in namecols:
		#			query+=i+','
		#		query=query[:-1]
		#		query+=") VALUES("				

		#		for rowval in sh.row_values(rownum):
		#			if ("'" in rowval):
		#				index = rowval.find("'")
		#				rowval=rowval[:index]+"'"+rowval[index:]
		#			query+="'"+rowval+"'"+","
		#		query=query[:-1]
		#		query+=')'
		#		f.write('\ndb.executesql("'+query.encode('utf8')+'")')
		#	else:
		#		firstline=False

		
	#with open("/home/tanguyl/Documents/projetPython/web2py/applications/TEMPLATE/models/db.py","r") as f:
	#	print(f.read())


	try:
		subprocess.check_call(["python", "web2py/web2py.py"])

	except subprocess.CalledProcessError:
		sys.exit("Erreur: python n'est pas présent sur la machine ou web2py a changé d'emplacement")


else:
	print("Erreur : pas de fichier sélectionné")



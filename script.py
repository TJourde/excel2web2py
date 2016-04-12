#!usr/bin/env/python
# -*- coding: utf-8 -*-
import sys, os, time, errno
import os.path
import sqlite3
import logging
#passing var
import pickle
#lib read excel files
import xlrd
import subprocess

def sendVars(sh,namecols):
	list =[]
	list.append(sh)
	list.append(namecols)
	pickle.dump(list,sys.stdout)

def getStoragePath():
	return str(os.path.abspath(os.path.dirname(__file__)))+"/web2py/applications/TEMPLATE/databases/storage.sqlite"

def getTimeH():
	localtime = time.localtime(time.time()) #heure machine
	timeh =  str(localtime[3])+'_'+str(localtime[4])+'_'+str(localtime[5])
	return timeh

def createLogs(zepath):
	localtime = time.localtime(time.time()) #heure machine
	timeh =  str(localtime[3])+'_'+str(localtime[4])+'_'+str(localtime[5])
	logpath = str(zepath)+"Log_"+timeh+".log"	
	return logpath

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

	for colnum in range(sheet.ncols):
		try:#necessary or else db attributes will look funny 
			sheet.col_values(colnum)[0].encode('ascii')
	
		except (UnicodeError):
			sys.exit(sheet.col_values(colnum)[0]+"Erreur: Nom de colonne n'est pas unicode")

		namecols.append(sheet.col_values(colnum)[0].replace(" ","_").replace("(","").replace(")",""))

	#print("Sheet: "+ shname)
	#for i in namecols:
		#print("Column: "+i)

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
		try:
			cursor.execute(query)
		except:
			pass			
			#sys.exit("Erreur insertion")

#prevent execution on import
if __name__ == '__main__':
	script_path=os.path.abspath(os.path.dirname(__file__))
	path=str(createFolder())
	logpath = str(createLogs(path))
	print ("Consult log file at"+logpath)
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	logging.info('Log created at :'+getTimeH())
	logging.info("script.py is executed")
	logging.info("Looking for the file in argument")
	#if there is at least an argument, the script is launched
	if( len(sys.argv)>1 ):
		logging.info("File found")
		logging.info("Checking if file is well formatted")
		fileWellFormatted(sys.argv[1])
		logging.info("File is well formatted")
		logging.info("Trying to open file")
		wb = tryOpenWorkbookFile(sys.argv[1])
		logging.info("Successfully opened the file")
		logging.info("Trying to get sheet")
		sh = getSheet(wb)
		logging.info("Successfully opened the sheet")
		logging.info("Trying to the name of the sheet")
		shname = getNameFirstSheetAsTableName(wb)
		logging.info("Successfully retrived the name of the sheet")
		logging.info("Trying to the names of the columns")
		namecols= getColumnsNames(sh,shname)
		logging.info("Successfully retrieved the name of the columns")
	

		#if(os.path.isdir(path)):
		#	if(os.path.isfile(path+sys.argv[1].split('.')[0]+".db")):
		#		os.remove(path+sys.argv[1].split('.')[0]+".db")
	
		#db
		#print ("Path: "+path)
		#print("Db :"+str(path)+sys.argv[1].split('.')[0]+".db")
		#conn = sqlite3.connect("web2py/applications/TEMPLATE/databases/storage.sqlite")
		#path+sys.argv[1].split('.')[0]+".db")
		#c = conn.cursor()

		#Remove old table
		#try:
		#	c.execute("DROP TABLE IF EXISTS "+shname)
		#	print("db effacée")
		#except:
			#sys.exit("db not removed")
		#	pass

		#Create table
		#try:
		#	c.execute(requestCreateTable(shname,namecols))
		#except:
		#	sys.exit('Probleme de creation')

		# Insert rows of data
		#insertRowsData(shname,sh,c)

		# Save (commit) the changes
		#conn.commit()

		# We can also close the connection if we are done with it.
		# Just be sure any changes have been committed or they will be lost.
		#conn.close()
		#var a creer : logs/log	

		from subprocess import call
		#subprocess.call(["rm","-R","web2py/applications/TEMPLATE/tmp/"])
		#try:
		#	subprocess.check_call(["cp","-R", path+'.',"web2py/applications/TEMPLATE/tmp/"])
		#except subprocess.CalledProcessError:
		#	sys.exit("Erreur: "+path+", web2py ou un de ses dossiers a disparu de l'emplacement prévu")

		try:
			logging.info("Trying to recover backup of db")
			subprocess.check_call(["cp","web2py/applications/TEMPLATE/models/db_backup.py","web2py/applications/TEMPLATE/models/db.py"])
			logging.info("Successfully recover backup of db")
		except subprocess.CalledProcessError:
			logging.exception("Error while retrieving db_backup")
			sys.exit("db_backup n'est plus présent")	

		with open("web2py/applications/TEMPLATE/models/db.py","a") as f:
			logging.info("Successfully opened db")
			#Drop table
			#f.write('\ntry:\n    db.'+shname+'.drop()\nexcept:\n    pass')

			#Create table
			f.write('\ndb.define_table("'+shname+'"')
		
			for i in namecols:
				f.write(',Field("'+i.encode('utf8')+'")')
			f.write(')')

			#getDb -> called from default.py to get the same db as db.py
			f.write('\ndef getDb():\n    module_path=os.path.abspath(os.path.dirname(__file__))\n    dbpath = module_path + "/../databases"\n    db_name = "storage.sqlite"\n    db = DAL("sqlite://"+ db_name ,folder=dbpath, auto_import=True)\n    return db')
			#getTable -> called from default.py to get the table generated
			f.write('\ndef getTable(db):\n    return db.'+shname)

		logging.info("Writing in db finished")
		#Insert Rows
		try:
			logging.info("Trying to recover backup of default")
			subprocess.check_call(["cp","web2py/applications/TEMPLATE/controllers/default_backup.py","web2py/applications/TEMPLATE/controllers/default.py"])
			logging.info("Successfully recover backup of default")
		except subprocess.CalledProcessError:
			logging.exception("Error while retrieving default_backup")
			sys.exit("default_backup n'est plus présent")

		#passing vars
		#sendVars(sh,namecols)
		#used for calling scriptInit once page has loaded
		with open("web2py/applications/TEMPLATE/controllers/default.py","a") as f:
			logging.info("Successfully opened default")
			f.write('def initData():')
			f.write('\n    from subprocess import check_call')
			f.write('\n    try:\n        subprocess.check_call(["python",'+'"'+str(script_path)+"/scriptInit.py"+'","'+str(script_path)+"/"+sys.argv[1]+'"'+"])")
			f.write('\n    except subprocess.CalledProcessError:\n        sys.exit("Une erreur vient de se produire : scriptInit.py est-il présent?")')
		
		try:
			logging.info("Trying to launch web2py")
			subprocess.check_call(["python", "web2py/web2py.py"])

		except subprocess.CalledProcessError:
			logging.exception("Error while executing web2py")
			sys.exit("Erreur: python n'est pas présent sur la machine ou web2py a changé d'emplacement")


	else:
		sys.exit("Erreur : pas de fichier sélectionné")



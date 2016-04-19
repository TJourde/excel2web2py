#!usr/bin/env/python
# -*- coding: utf-8 -*-
import sys, os, time, errno
import os.path
import sqlite3
import logging
#passing var
#import pickle
#lib read excel files
import xlrd
import subprocess
#import matplotlib.pyplot as plt

#plt.plot([1,2,3])
#plt.show()



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

def getSheetAsTableName(shname):
	try:
		shname.encode('ascii')
	
	except (UnicodeError):
		sys.exit("Erreur: le nom de la feuille n'est pas unicode")
	
	if " " in shname or "(" in shname or ")" in shname:
		return False
	else:
		return True
			#newshname = shname.replace(" ","_").replace("(","").replace(")","")
	#return newshname

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
	isThereId = False
	ref = []
	for rownum in range(sheet.nrows):
		if(not firstline):
			query = "INSERT INTO "+nameTable+" VALUES ("
			if not isThereId:
				query += str(idcpt)+","
			for rowval in sheet.row_values(rownum):
				#for null value
				try:
					query+='"'+rowval+'"'+','
				except:
					query+='"'+str(rowval)+'"'+','
			query=query[:-1]
			query+=')'
			idcpt+=1
		else:
			if any("idthis" in s for s in sheet.row_values(rownum)):
				isThereId = True
			cpt = 0
			for s in sheet.row_values(rownum):
				if ("reference=" in s ):
					ref.append(str(cpt)+'/'+s.split("=")[1])
				cpt+=1
			firstline=False
		try:
			
			cursor.execute(query)
		except:
			print query
			print("Ins:Smth went wrong")
			pass			
			#sys.exit("Erreur insertion")
	cptc=0
	for i in ref:
		j = i.split("/")
		query= "INSERT INTO "+nameTable+j[1]+" VALUES ("
		for colval in sheet.col_values(int(j[0]))[+1:]:
			print colval
			ncode = colval.split('|')
			if(len(ncode)>0):
				for n in ncode:
					print str(n)
					try:
						cursor.execute(query+str(cptc)+','+str(n)+')')
					except:
						print query+str(cptc)+','+str(n)+')'
						print("Ref:Smth went wrong")
						pass
						#sys.exit("Erreur insertion")
			cptc+=1

def getColumns(sheet):
	# get names of columns (1st row value)
	namecols = []

	for colnum in range(sheet.ncols):
		try:#necessary or else db attributes will look funny 
			sheet.col_values(colnum)[0].encode('ascii')
			nc = sheet.col_values(colnum)[0].split('|')
			i = 0
			while i < len(nc):
				nc[i] = nc[i].replace(" ","_").replace("(","").replace(")","")
				i+=1
			namecols.append(nc)
	
		except (UnicodeError):
			sys.exit(sheet.col_values(colnum)[0]+"Erreur: Nom de colonne n'est pas unicode")
	return namecols

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
		logging.info("Trying to get sheets & names")
		allshnames = wb.sheet_names()
		for s in allshnames:
			if not getSheetAsTableName(s):
				sys.exit("Erreur: le nom de cette feuille contient des caractères spéciaux: "+str(s))

		allsheets = wb.sheets()
		logging.info("Successfully opened the sheets")
		logging.info("Trying to retrieve the names of the columns of each sheets")
		allcolumns = []
		for i in allsheets:
			allcolumns.append(getColumns(i))
		logging.info("Successfully retrieved the name of the columns")
	
		try:
			logging.info("Trying to recover backup of db")
			subprocess.check_call(["cp","web2py/applications/TEMPLATE/models/db_backup.py","web2py/applications/TEMPLATE/models/db.py"])
			logging.info("Successfully recover backup of db")
		except subprocess.CalledProcessError:
			logging.exception("Error while retrieving db_backup")
			sys.exit("db_backup n'est plus présent")	

		with open("web2py/applications/TEMPLATE/models/db.py","a") as f:
			logging.info("Successfully opened db")
			logging.info("Creating tables")
			cptC = 0
			ref = []
			for i in allshnames:
				pk = []
				f.write('\ndb.define_table("'+str(i).encode('utf8')+'"')
				for j in allcolumns[cptC]:
					#nameColumn should always be first element
					f.write(',Field("'+j[0].encode('utf8')+'"')
					for h in j[+1:]:
						if h == "primarykey":
							pk.append(j[0])
						elif h ==  "idthis":
							f.write(', "id"')
						elif "reference=" in h:
							ref.append(i+"/"+h.split("=")[1])		
						else:
							f.write(","+h.encode('utf8'))	
					f.write(')')
				cptC += 1
				if len(pk) > 0:
					f.write(',primarykey=["'+pk[0].encode('utf8')+'"')
					for pki in pk[+1:]:
						f.write(',"'+pki.encode('utf8')+'"')
					f.write(']')
				f.write(')')

			for r in ref:
				s=r.split("/")
				f.write('\ndb.define_table("'+(s[0]+s[1]).encode('utf8')+'",Field("'+s[0].encode('utf8')+'",type="integer"),Field("'+s[1].encode('utf8')+'",type="integer"),primarykey=["'+s[0].encode('utf8')+'","'+s[1].encode('utf8')+'"])')
				
			#getDb -> called from default.py to get the same db as db.py
			f.write('\ndef getDb():\n    from os import path\n    module_path=os.path.abspath(os.path.dirname(__file__))\n    dbpath = module_path + "/../databases"\n    db_name = "storage.sqlite"\n    db = DAL("sqlite://"+ db_name ,folder=dbpath, auto_import=True)\n    return db')
			#getTable -> called from default.py to get the table generated
			f.write('\ndef getTable(db):\n    return db.'+str(allshnames[0]).encode('utf8'))

		logging.info("Writing in db finished")
		
		
		try:
			logging.info("Trying to recover backup of default")
			subprocess.check_call(["cp","web2py/applications/TEMPLATE/models/backup_menu.py","web2py/applications/TEMPLATE/models/menu.py"])
			logging.info("Successfully recover backup of menu")
		except subprocess.CalledProcessError:
			logging.exception("Error while retrieving backup_menu")
			sys.exit("menu_backup n'est plus présent")
		with open("web2py/applications/TEMPLATE/models/menu.py","a") as f:
			logging.info("Writing menu shortcuts")
			f.write("def _():\n    app = request.application\n    ctr = request.controller\n    response.menu += [")
			f.write("\n        (T('Main'), False, URL('default', 'main'))")
			f.write("\n        ]")
			f.write("\n_()")
            
			logging.info("Menu done")
			
		#Insert Rows
		try:
			logging.info("Trying to recover backup of default")
			subprocess.check_call(["cp","web2py/applications/TEMPLATE/controllers/default_backup.py","web2py/applications/TEMPLATE/controllers/default.py"])
			logging.info("Successfully recover backup of default")
		except subprocess.CalledProcessError:
			logging.exception("Error while retrieving default_backup")
			sys.exit("default_backup n'est plus présent")

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



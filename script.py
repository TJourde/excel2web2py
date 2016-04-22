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


# not used
def sendVars(sh,namecols):
	list =[]
	list.append(sh)
	list.append(namecols)
	pickle.dump(list,sys.stdout)

def getStoragePath():
	return str(os.path.abspath(os.path.dirname(__file__)))+"/../applications/TEMPLATE/databases/storage.sqlite"

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

# test if name file pass criteria
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
		
# test if sheet's name pass criteria
def isSheetATableName(shname):
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
	
#not used
def requestCreateTable(name,namecols):
	s ='CREATE TABLE "'+ shname+'"(id,'
	for i in namecols:
		s+='"'+i+'",'
	s=s[:-1]
	s+=')'
	return s
#execute sql request to insert data
def insertRowsData(nameTable,sheet,cursor):
	
	query = ""
	idcpt = 0
	firstline=True
	isThereId = False
	ref = []
	##insert data of sheets
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
			#print query
			print("Ins:Smth went wrong")
			pass			
			#sys.exit("Erreur insertion")
	cptc=0
	## insert data on reference tables
	for i in ref:
		j = i.split("/")
		query= "INSERT INTO "+nameTable+j[1]+" VALUES ("
		for colval in sheet.col_values(int(j[0]))[+1:]:
			#print colval
			ncode = colval.split('|')
			if(len(ncode)>0):
				print ncode
				for n in ncode:
					#print str(n)
					try:
						cursor.execute(query+str(cptc)+','+str(n)+')')
					except:
						#print query+str(cptc)+','+str(n)+')'
						print("Ref:Smth went wrong")
						pass
						#sys.exit("Erreur insertion")
			cptc+=1

def dropTable (nameTable,cursor):
	try:
		cursor.execute("DROP TABLE "+str(nameTable))
	except:
		print("Drop:Smth went wrong")
		pass

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

#prevent execution on import from scriptInit
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
			if not isSheetATableName(s):
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
			subprocess.check_call(["cp","-v","../applications/TEMPLATE/models/db_backup.py","../applications/TEMPLATE/models/db.py"])
			logging.info("Successfully recover backup of db")
		except subprocess.CalledProcessError:
			logging.exception("Error while retrieving db_backup")
			sys.exit("Cannot access db_backup")	


### Defining tables

		ref = [] #used also to write represent attr in default controller
		zeids = []
		with open("../applications/TEMPLATE/models/db.py","a") as f:
			logging.info("Successfully opened db")
			logging.info("Creating tables")
			##Defining sheet table
			cptC = 0
			for i in allshnames:
				pk = []
				zeid = "id"
				f.write('\ndb.define_table("'+str(i).encode('utf8')+'"')
				for j in allcolumns[cptC]:
					
					#nameColumn should always be first element
					s=""
					for h in j[+1:]:
		
						if h == "primarykey":
							pk.append(j[0])
						elif h ==  "idthis":
							s+=',"id"'
							zeid=j[0]
						elif "reference=" in h:
							ref.append(i+"/"+h.split("=")[1])		
						else:
							#f.write(',Field("'+j[0].encode('utf8')+'"')
							s+=","+h.encode('utf8')
					
					f.write(',Field("'+j[0].encode('utf8')+'"'+s+')')
							
				zeids.append(zeid+"/"+i)
				cptC += 1
				if len(pk) > 0:
					f.write(',primarykey=["'+pk[0].encode('utf8')+'"')
					for pki in pk[+1:]:
						f.write(',"'+pki.encode('utf8')+'"')
					f.write(']')
				f.write(')')
				
			#table + generated table [:] prevent copy reference	
			alltables = allshnames[:]
			
			##Defining reference table
			for idx,r in enumerate(ref):
				s=r.split("/")
				# ___ means reference table
				alltables.append(s[0]+"___"+s[1])
				realid = "id"
				
				for z in zeids:
					if z.split("/")[1] == s[1]:
						realid = z.split("/")[0]
				# ___ means reference table
				nameref= s[0]+"___"+s[1]
				f.write('\ndb.define_table("'+(nameref).encode('utf8')+'",Field("'+s[0].encode('utf8')+'",type="integer"),Field("'+s[1].encode('utf8')+'",type="integer"),primarykey=["'+s[0].encode('utf8')+'","'+s[1].encode('utf8')+'"])')
				# boo links tables for sqlform.grid
				f.write('\ndef boo'+str(idx)+'(value,row,db):\n    rows = db((db.'+(nameref).encode('utf8')+'.'+s[0]+' == row.id)&(db.'+(nameref).encode('utf8')+'.'+s[1]+' == db.'+s[1]+'.'+realid.encode('utf8')+')).select(db.'+s[1]+'.ALL)')
				f.write('\n    t=["w2p_odd odd","w2p_even even"]')
				f.write('\n    return TABLE(*[TR(r.'+s[1]+', _class=t[idx%2]) for idx,r in enumerate(rows)])')
	
			##Defining some heplful functions
			#getDb -> called from default.py to get the same db as db.py
			f.write('\ndef getDb():\n    from os import path\n    module_path=os.path.abspath(os.path.dirname(__file__))\n    dbpath = module_path + "/../databases"\n    db_name = "storage.sqlite"\n    db = DAL("sqlite://"+ db_name ,folder=dbpath, auto_import=True)\n    return db')
			#getTable -> called from default.py to get the table generated
			f.write('\ndef getTable(db):\n    return db.'+str(allshnames[0]).encode('utf8'))
			
			### Defining tables end
			
			### Dropping tables


			#allow to know if tables should be dropped
			allfiles = os.listdir('../applications/TEMPLATE/databases')
			tableFile = False
			tableHere = ""
			

			##Test if table's name is a file in databases
			for i in alltables:
				if not tableFile:
					for f in allfiles:
						if not tableFile:
							if str(i)+'.table' in f:
								tableFile = True
								tableHere = i
								
			##Warning user : delete possible
			if tableFile:
				logging.info("Table exists :"+str(tableHere))
				print "This sheet's name "+str(tableHere)+" is already used"
				print "Continuing will erase all tables with a sheet's name on this file"
				print "Change this name if you wish to keep your data"
				print "Or do you want to clear your data and generate new tables ? (y/n)"
				drop = False
				# only continue if drop, else quit exec
				while not drop:
					answer = raw_input()
					if answer == "y":
						logging.info("Deleting files in databases and view")
						
						try:
							logging.info("Trying to access database")
							conn = sqlite3.connect(getStoragePath())
							c = conn.cursor()
						except:
							logging.error("Database couldn't be reached"+getStoragePath())
							sys.exit("Database couldn't be reached")
						
						logging.info("Success: connected to database")
						drop = True
						
						for s in alltables:
							delTable= ""
							for f in allfiles:
								#tmp solution don't know if always 7
								if "7_"+str(s)+'.table' in f:
									
									dropTable(s,c)
									delTable = f
									#don't seem necessary but just in case
									try:
										subprocess.check_call(["rm","-rfv","../applications/TEMPLATE/views/default/"+s+".html"])
									except subprocess.CalledProcessError:
										logging.exception("Error while deleting"+s+".html")
										pass
									
							if delTable is not "":		
								try:
									logging.info("Trying delete file")
									subprocess.check_call(["rm","-rfv","../applications/TEMPLATE/databases/"+str(delTable)])
									
									logging.info("Successfully deleted file")
								except subprocess.CalledProcessError:
									logging.exception("Error while deleting"+str(f))
									sys.exit("Cannot erase file")
						
						# Save (commit) the changes
						conn.commit()
						# We can also close the connection if we are done with it.
						# Just be sure any changes have been committed or they will be lost.
						conn.close()
						logging.info("Done deleting files and dropping")
						
					
					elif answer == "n":
						logging.info("Stopping script on user's demand")
						print "Stopping script"
						exit()
					

			### Dropping tables end


			#actualize allfiles in case of delete
			allfiles = os.listdir('../applications/TEMPLATE/databases')
			
			
			logging.info("Writing in db finished")
			logging.info("Closing file")
			
		### Making menu
		try:
			logging.info("Trying to recover backup of menu")
			subprocess.check_call(["cp","-v","../applications/TEMPLATE/models/backup_menu.py","../applications/TEMPLATE/models/menu.py"])
			logging.info("Successfully recover backup of menu")
		except subprocess.CalledProcessError:
			logging.exception("Error while retrieving backup_menu")
			sys.exit("menu_backup cannot be found")
			
			
		## Retrieve all existing tables'name
		# keep files with table extension
		# doesn't contain auth
		extables = []
		for e in allfiles:
			if ((".table" in e) and ("auth" not in e ) and ( "___" not in e)):
				#to make sure we get the real table's name, we remove the extension and keep what is after the hash key
				#___ design reference table, we don't want them to show up
				extables.append(e.split("_",1)[1].split(".")[0])
		
		#so we know if we have dropped tables when running this script, they are in the file
		# maybe test if table in there instead
		if not tableFile :
			with open ("menucategory.txt","a") as f:
				f.write("\n"+sys.argv[1])
				for n in allshnames:
					f.write('|'+n)
		
		#get all menu categories
		listmenu = []
		with open ("menucategory.txt") as f:
			for line in f:
				listmenu.append(str(line))	
				
		#we ignore empty lines
		listmenu = [val for val in listmenu if val != '\n']
		
		## Shortcuts
		
		with open("../applications/TEMPLATE/models/menu.py","a") as f:
			logging.info("Writing menu shortcuts")
			f.write("def _():\n    app = request.application\n    ctr = request.controller")
			f.write("\n    response.menu += [")
			s = ""
			for l in listmenu:
				lsplit = l.split("|")
				s += "\n        (T('"+lsplit[0]+"'), False, None, ["
				for e in lsplit[+1:]:
					tmp = e.strip("\n")
					s +="\n            (T('"+tmp+"'), False, URL('default', '"+tmp+"')),"
				s=s[:-1]
				s += "\n        ])"
				s += ","
			s = s[:-1]
			s+=("\n    ]\n_()")
			f.write(s)
            
			logging.info("Menu done")
			
		### Making menu end
		
		### Insert Rows
		try:
			logging.info("Trying to recover backup of default")
			subprocess.check_call(["cp","-v","../applications/TEMPLATE/controllers/default_backup.py","../applications/TEMPLATE/controllers/default.py"])
			logging.info("Successfully recover backup of default")
		except subprocess.CalledProcessError:
			logging.exception("Error while retrieving default_backup")
			sys.exit("default_backup cannot be found")

		#used for calling scriptInit once page has loaded
		with open("../applications/TEMPLATE/controllers/default.py","a") as f:
			logging.info("Successfully opened default")
			# first, we define all links to views from this file
			for e in extables + allshnames: 
				f.write('\ndef '+e+'():')
				f.write('\n    db = getDb()')
				f.write('\n    table = db.'+e)
				# necessary to differentiate to prevent dal errors
				if e in allshnames:
					for idx,r in enumerate(ref):
						s=r.split("/")
						f.write('\n    db.'+s[0]+'.'+s[1]+'.represent = lambda val,row:boo'+str(idx)+'(val,row,db)')
						f.write('\n    rows = db(table).select()')
						f.write('\n    if (len(rows) == 0):')
						f.write('\n        initData()')
				else:
					f.write('\n    rows = db(table).select()')
					
				f.write('\n    form = forming(table)')
				f.write('\n    records=SQLFORM.grid(table)')
				f.write('\n    return dict(form=form, records=records)')
				
			# used in case main table is empty	
			f.write('\ndef initData():')
			f.write('\n    from subprocess import check_call')
			f.write('\n    try:\n        subprocess.check_call(["python",'+'"'+str(script_path)+"/scriptInit.py"+'","'+str(script_path)+"/"+sys.argv[1]+'"'+"])")
			f.write('\n    except subprocess.CalledProcessError:\n        sys.exit("Une erreur vient de se produire : scriptInit.py est-il présent?")')
			
		logging.info("Writing in default finished")
		logging.info("Closing file")
		
		###create new views
		try:
			logging.info("Trying to create views")
			for e in allshnames:
				subprocess.check_call(["cp","-v","../applications/TEMPLATE/views/default/table.html","../applications/TEMPLATE/views/default/"+e+".html"])
				logging.info("Successfully created view :"+e)
		except subprocess.CalledProcessError:
			logging.exception("Error while retrieving table.html")
			sys.exit("table.html cannot be found")
			
		###create new views end
			
		###launch web2py
		
		try:
			logging.info("Trying to launch web2py")
			subprocess.check_call(["python", "../web2py.py"])

		except subprocess.CalledProcessError:
			logging.exception("Error while executing web2py")
			sys.exit("Erreur: python n'est pas présent sur la machine ou web2py a changé d'emplacement")
		
		###launch web2py end

	else:
		sys.exit("Erreur : pas de fichier sélectionné")



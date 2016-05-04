#!usr/bin/env/python
# -*- coding: utf-8 -*-
import sys, os, time, errno
import os.path
import sqlite3
import logging
#lib read excel files
import xlrd
import subprocess

#import matplotlib.pyplot as plt

#plt.plot([1,2,3])
#plt.show()

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
	
# test if name file pass criteria
def fileWellFormatted(pathFile):
	
	path=str( createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	
	if(" " in pathFile):
		logging.error("File's name has spaces")
		sys.exit("Error: file's name has spaces")

	try:
		pathFile.encode('ascii')
	
	except (UnicodeError):
		logging.exception("File's name couldn't be encoded in ascii")
		sys.exit("Error : File's name couldn't be encoded in ascii")

def tryOpenWorkbookFile(pathFile):
	path=str( createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	try:
		#workbook doesn't need to be explicitly closed
		wb = xlrd.open_workbook(pathFile)
		return wb
	except(IOError):
		logging.exception("File couldn't be opened")
		sys.exit("Error: File couldn't be opened")
		
# test if name pass criteria (does it pass )
def isNametATableName(name):
	path=str( createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	try:
		name.encode('ascii')
	
	except (UnicodeError):
		logging.exception("Name couldn't be encoded in ascii")
		sys.exit("Name couldn't be encoded in ascii")
	
	for i in name.split("_"):
		if not i.isalpha():
			logging.exception("Namehas special characters: "+ name)
			sys.exit("Name has special characters: "+ name )
		
	


def dropTable (nameTable,cursor):
	path=str( createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	try:
		logging.info("DROP TABLE "+str(nameTable))
		cursor.execute("DROP TABLE "+str(nameTable))
	except  sqlite3.Error as er:
		print("Drop:Smth went wrong")
		logging.warning( str(nameTable))
		logging.warning( er.message)
		pass
#return first line
def getColumns(sheet):
	path=str( createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	# get names of columns (1st row value)
	namecols = []

	for colnum in range(sheet.ncols):
		try:#necessary or else db attributes will look funny 
			sheet.col_values(colnum)[0].encode('ascii')
			# first line of that column
			nc = sheet.col_values(colnum)[0].split('|')
			isNametATableName(nc[0])
			namecols.append(nc)
	
		except (UnicodeError):
			logging.exception(sheet.col_values(colnum)[0]+" Column's name couldn't be encoded in ascii")
			sys.exit(sheet.col_values(colnum)[0]+" Error: Column's name couldn't be encoded in ascii")
	return namecols

def createDict(ref,filePath,numRef):
	#ref: name of table referenced
	#filePath: file's path which will be modified
	#numRef : reference number in case of multiple references in 'sheet'
	path=str( createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	
	with open(filePath,"a") as f:
		##Defining reference dict
				
		# boo links to dict for sqlform.grid
		nameFunc = sys.argv[1].split('/')[-1].split('.')[0]
		f.write('\ndef boo'+str(nameFunc)+str(numRef)+'(value,row,db):')
		f.write('\n    listOfRefs = []')
		f.write('\n    listAttr=[]')
		f.write('\n    rowvals = row.'+ref+'.split("|")')
		f.write('\n    for val in rowvals :')
		f.write('\n        res=db(db["'+ref+'"].id == val).select()')
		f.write('\n        listValAttr=[]')
		f.write('\n        for row in res:')
		f.write('\n            for attr in row:')
		f.write('\n                if attr != "id":')
        #there are attr that are also update or delete record object  that need to be taken in account
		f.write('\n                    if ((type(row[attr]) is str) or (type(row[attr]) is int) or (type(row[attr]) is float)):')
		f.write('\n                        if attr not in listAttr:')
		f.write('\n                            listAttr.append(attr)')
		f.write('\n                        listValAttr.append(row[attr])')
		f.write('\n        listOfRefs.append(listValAttr)')
		f.write('\n    listOfRefs.insert(0,listAttr)')
		f.write('\n    t=["w2p_odd odd","w2p_even even"]')
		f.write('\n    return TABLE(*[TR(r, _class=t[idx%2]) for idx,r in enumerate(listOfRefs)])')

            
		
		

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
			isNametATableName(s)
		
		allsheets = wb.sheets()
		logging.info("Successfully opened the sheets")
		logging.info("Trying to retrieve the names of the columns of each sheets")
		allcolumns = []
		for i in allsheets:
			allcolumns.append(getColumns(i))
		logging.info("Successfully retrieved the name of the columns")
	
		try:
			logging.info("Trying to recover backup of db")
			if os.name =="nt":
				subprocess.check_call(["copy","/Y","%cd%"+"\..\\applications\\TEMPLATE\\models\\db_backup.py","%cd%"+"\..\\applications\\TEMPLATE\\models\\db_"+sys.argv[1].split('.')[0]+".py"],shell=True)
			else:
				subprocess.check_call(["cp","-v","../applications/TEMPLATE/models/db_backup.py","../applications/TEMPLATE/models/db_"+sys.argv[1].split('.')[0]+".py"])	
			logging.info("Successfully recover backup of db")
		except subprocess.CalledProcessError as er:
			logging.exception("Error while retrieving db_backup: " + er.message)
			sys.exit("Cannot access db_backup")
			
		


### Defining tables

		ref = [] #used also to write represent attr in default controller
		zeids = []
		with open("../applications/TEMPLATE/models/db_"+sys.argv[1].split('.')[0]+".py","a") as f:
			logging.info("Successfully opened db")
			logging.info("Creating tables")
			##Defining sheet table
			cptC = 0
			for i in allshnames:
				pk = []
				zeid = "id"
				f.write('\ndb.define_table("'+str(i).encode('utf-8')+'"')
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
						elif (("type='integer'" == h) or ("type='float'" == h) or ("type='string'" == h)) :
								s+=","+h.encode('utf-8')
					f.write(',Field("'+j[0].encode('utf-8')+'"'+s+')')
							
				zeids.append(zeid+"/"+i)
				cptC += 1
				if len(pk) > 0:
					f.write(',primarykey=["'+pk[0].encode('utf-8')+'"')
					for pki in pk[+1:]:
						f.write(',"'+pki.encode('utf-8')+'"')
					f.write(']')
				f.write(')')
			


	
			##Defining some heplful functions
			#getDb -> called from default.py to get the same db as db.py
			f.write('\ndef getDb():\n    from os import path\n    module_path=os.path.abspath(os.path.dirname(__file__))\n    dbpath = module_path + "/../databases"\n    db_name = "storage.sqlite"\n    db = DAL("sqlite://"+ db_name ,folder=dbpath, auto_import=True)\n    return db')
			#getTable -> called from default.py to get the table generated
			f.write('\ndef getTable(db):\n    return db.'+str(allshnames[0]).encode('utf-8'))
			
			### Defining tables end
			
			### Dropping tables


			#allow to know if tables should be dropped
			allfiles = os.listdir('../applications/TEMPLATE/databases')
			tableFile = False
			tableHere = ""
			

			##Test if table's name is a file in databases
			for i in allshnames:
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
							logging.exception("Database couldn't be reached"+getStoragePath())
							sys.exit("Database couldn't be reached")
						
						logging.info("Success: connected to database")
						drop = True
						
						for s in allshnames:
							delTable= ""
							for f in allfiles:
								#7 is the last digit of the hashkey of the files table
								if "7_"+str(s)+'.table' in f:
									
									dropTable(s,c)
									delTable = f
									
							if delTable is not "":		
								try:
									logging.info("Trying delete file")
									if os.name =="nt":
										subprocess.check_call(["DEL","%cd%"+"\..\\applications\\TEMPLATE\\databases\\"+str(delTable)],shell=True)
									else:
										subprocess.check_call(["rm","-rfv","../applications/TEMPLATE/databases/"+str(delTable)])
									
									logging.info("Successfully deleted file")
								except subprocess.CalledProcessError as er:
									logging.exception("Error while deleting "+str(f)+" : "+er.message )
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
			

		
		### Insert Rows
		try:
			logging.info("Trying to recover backup of default")
			if os.name =="nt":
				subprocess.check_call(["copy","/Y","%cd%"+"\..\\applications\\TEMPLATE\\controllers\\default_backup.py","%cd%"+"\..\\applications\\TEMPLATE\\controllers\\"+sys.argv[1].split('.')[0]+".py"],shell=True)
			else:
				subprocess.check_call(["cp","-v","../applications/TEMPLATE/controllers/default_backup.py","../applications/TEMPLATE/controllers/"+sys.argv[1].split('.')[0]+".py"])
			
			
			logging.info("Successfully recover backup of default")
		except subprocess.CalledProcessError as er:
			logging.exception("Error while retrieving default_backup : " + er.message)
			sys.exit("default_backup cannot be found")

		###Dicts
		#we need to define boo functions before the views fuctions
		logging.info("Creating dicts")

		nameController = sys.argv[1].split('.')[0]

		cptC=0
		for i in allshnames:
			refs=[]
			for j in allcolumns[cptC]:
				for h in j[+1:]:
					if "reference=" in h:
						refs.append(i+"/"+h.split("=")[1])
			if refs is not None:
				for idx,r in enumerate(refs):
					createDict(r.split('/')[1],"../applications/TEMPLATE/controllers/"+nameController+".py",idx)
			cptC += 1

		logging.info("Dicts written")



		#used for calling scriptInit once page has loaded
		with open("../applications/TEMPLATE/controllers/"+nameController+".py","a") as f:
			logging.info("Successfully opened "+nameController+".py")
			
			
			# then, we define all links to views from this file
			for nameTable in allshnames: 
				f.write('\ndef '+nameTable+'():')
				f.write('\n    db = getDb()')
				f.write('\n    table = db.'+nameTable)
				# necessary to differentiate to prevent dal errors
				#for each reference
				for idx,r in enumerate(ref):
					s=r.split("/")
					#for each column of the table
					for c in getColumns(wb.sheet_by_name(nameTable)):
						if ((s[1] == c[0])) :
							f.write('\n    db.'+s[0]+'.'+s[1]+'.represent = lambda val,row:boo'+sys.argv[1].split('.')[0]+str(idx)+'(val,row,db)')
				f.write('\n    rows = db(table).select()')
				f.write('\n    if (len(rows) == 0):')
				f.write('\n        initData()')
				f.write('\n    rows = db(table).select()')
				
				s="\n    form = FORM("
				for c in getColumns(wb.sheet_by_name(nameTable)):
					if (("type='integer'" in c) or( "type='float'" in c)):
						s+="DIV(LABEL('"+c[0]+"'),INPUT(_name='"+c[0]+"',_type='checkbox'),_class='row'),"
				s+="DIV(LABEL('Simple plot'),INPUT(_type='radio',_name='plot',_value='plot' ,value='plot'),LABEL('Histogram'),INPUT(_type='radio',_name='plot',_value='hist'),LABEL('Subplots'),INPUT(_type='radio',_name='plot',_value='sub'),_class='row'),"
				s+="INPUT(_type='submit',_class='btn btn-primary',_name='makeplot'),_class='form-horizontal',_action='',_method='post')"
				if "DIV" in s:
					f.write(s)
				else:
					f.write("\n    form=''")
				f.write("\n    plot=DIV('')")
				f.write('\n    if ((len(request.post_vars)>2) and ("makeplot" in request.post_vars)):')
				f.write("\n        vars = request.post_vars.keys()")
				f.write("\n        vars.remove('makeplot')")
				f.write('\n        fields=""')
				f.write("\n        typeplot=''")   
				f.write("\n        for v in vars :")
				f.write("\n            if v == 'plot' :")
				f.write("\n                typeplot = request.post_vars.plot")
				f.write("\n            else :")
				f.write("\n                fields+=str(v)+','")
				f.write("\n        fields=fields[:-1]")
				f.write("\n        nameTable ='"+nameTable+"'")
				f.write("\n        foo = os.path.abspath(os.path.dirname(__file__))")
				f.write("\n        foo = foo + '/../static/foo.png' ")
				f.write("\n        makePlot(typeplot,fields,nameTable,foo)")
				f.write("\n        plot=IMG(_src=URL('static','foo.png'),_alt='plot')")
				f.write('\n    records=SQLFORM.grid(table,paginate=10,maxtextlength=256,showbuttontext=False)')
				f.write('\n    return dict(form=form, plot=plot, records=records)')
				
			# used in case main table is empty	
			f.write('\ndef initData():')
			f.write('\n    from subprocess import check_call')
			f.write('\n    try:\n        subprocess.check_call(["python",'+'"'+str(script_path)+"/scriptInit.py"+'","'+str(script_path)+"/"+sys.argv[1]+'"'+"])")
			f.write('\n    except subprocess.CalledProcessError:\n        sys.exit("Error : scriptInit.py could not be reached")')
			
			#used to create plot
			f.write('\ndef makePlot(typeplot,fields,nameTable,whereToSave):')
			f.write('\n    from subprocess import check_call')
			f.write('\n    try:')
			f.write('\n        subprocess.check_call(["python",'+'"'+str(script_path)+"/scriptPlot.py"+'",typeplot,fields,nameTable,whereToSave])')
			f.write('\n    except subprocess.CalledProcessError:')
			f.write('\n        sys.exit("Error : scriptPlot.py could not be reached")')
			
		logging.info("Writing in "" finished")
		logging.info("Closing file")
		
		###create new views
		try:
			logging.info("Trying to create views")
			for nameTable in allshnames:
				if os.name =="nt":
					subprocess.call(["mkdir","%cd%"+"\..\\applications\\TEMPLATE\\views\\"+sys.argv[1].split('.')[0]],shell=True)
					subprocess.check_call(["copy","/Y","%cd%"+"\..\\applications\\TEMPLATE\\views\\default\\table.html","%cd%"+"\..\\applications\\TEMPLATE\\views\\"+sys.argv[1].split('.')[0]+"\\"+nameTable+".html"],shell=True)
				else:
					subprocess.call(["mkdir","-v","../applications/TEMPLATE/views/"+sys.argv[1].split('.')[0]+"/"])
					subprocess.check_call(["cp","-v","../applications/TEMPLATE/views/default/table.html","../applications/TEMPLATE/views/"+sys.argv[1].split('.')[0]+"/"+nameTable+".html"])
			
				logging.info("Successfully created view :"+nameTable)
		except subprocess.CalledProcessError as er:
			logging.exception("Error while retrieving table.html : "+er.message)
			sys.exit("table.html cannot be found")
			
		###create new views end
		
		
		### Making menu
		try:
			logging.info("Trying to recover backup of menu")
			if os.name =="nt":
				subprocess.check_call(["copy","/Y","%cd%"+"\..\\applications\\TEMPLATE\\models\\backup_menu.py","%cd%"+"\..\\applications\\TEMPLATE\\models\\menu.py"],shell=True)
			else:
				subprocess.check_call(["cp","-v","../applications/TEMPLATE/models/backup_menu.py","../applications/TEMPLATE/models/menu.py"])
			
			logging.info("Successfully recover backup of menu")
		except subprocess.CalledProcessError as er:
			logging.exception("Error while retrieving backup_menu : "+er.message)
			sys.exit("menu_backup cannot be found")
			
			
		
		listmenu=[]
		allviews = os.listdir('../applications/TEMPLATE/views')
		for view in allviews:
			if ((os.path.isdir('../applications/TEMPLATE/views/'+view)) and ('default' not in view)):
				allhtml = os.listdir('../applications/TEMPLATE/views/'+view)
				submenus = []
				submenus.append(str(view))
				#for some reason, list dir display files in the chronological order in reverse on Linux
				
				if os.name !="nt":
					allhtml=reversed(allhtml)
				
				for html in allhtml:
					#to make sure it is a view
					if html.endswith('.html'):
						submenus.append(str(html.split('.')[0]))
				listmenu.append(submenus)
				
		
		## Shortcuts
		with open("../applications/TEMPLATE/models/menu.py","a") as f:
			logging.info("Writing menu shortcuts")
			f.write("def _():\n    app = request.application\n    ctr = request.controller")
			f.write("\n    response.menu += [")
			s = ""
			for menu in listmenu:
				s += "\n        (T('"+menu[0]+"'), False, None, ["
				go=False
				for submenu in menu:
					if go:
						s +="\n            (T('"+submenu+"'), False, URL('"+menu[0]+"', '"+submenu+"')),"
					else:
						go=True
				s=s[:-1]
				s += "\n        ])"
				s += ","
			s = s[:-1]
			s+=("\n    ]\n_()")
			f.write(s)
            
			logging.info("Menu done")
			
		### Making menu end
			
		###launch web2py
		
		try:
			logging.info("Trying to launch web2py")
			if os.name =="nt": 
				subprocess.check_call(["%cd%\..\\web2py.exe"],shell=True)
			else:
				subprocess.check_call(["python", "../web2py.py"])
		except subprocess.CalledProcessError as er:
			logging.exception("Error while executing web2py : " + er.message)
			sys.exit("Error: python is no present on this computer or web2py could not be reached")
		
		###launch web2py end

	else:
		sys.exit("Error : no file selected")



#!usr/bin/env/python
# -*- coding: utf-8 -*-

#NB:Called from TEMPLATE/controllers/default.py

#Ultimate goals:
#Check the excel file and the data
#Create Controllers,Models and Views from the data inside the TEMPLATE application
#Update the menu
#Define functions and forms to generate plots
#Define functions to help displaying data from other sheets
#Log important informations

try:
	import sys, os, time, errno
	import os.path
	import sqlite3
	import logging
	#lib read excel files
	import xlrd
	import subprocess
	#not needed here, just to test its presence
	import matplotlib

except ImportError as er:
	sys.exit("Error: "+er.message)

#Retrieve path of storage.sqlite to help executing queries
#I:None
#O:Absolute path of storage.sqlite
def getStoragePath():
	storagePath = os.path.abspath(os.path.dirname(__file__))+"/../applications/TEMPLATE/databases/storage.sqlite"
	if os.name == "nt":
		return storagePath.decode('latin-1')
	return storagePath
	
#Retrieve local time to generate logs
#I:None
#O:Local time h:m:s
def getTimeH():
	localtime = time.localtime(time.time()) #heure machine
	timeh =  str(localtime[3])+'_'+str(localtime[4])+'_'+str(localtime[5])
	return timeh
	
#Generate Log file 
#I: path of Log folder
#O:Return path of newly generated log file
def createLogs(zepath):
	localtime = time.localtime(time.time()) #heure machine
	timeh =  getTimeH()
	logpath = str(zepath)+"Log_"+timeh+".log"	
	return logpath
#Create folder of Logs
#I:None
#O:Return path of newly generated folder
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
#Done by web2py
#Test if name file pass criteria(no spaces,ascii only)
#I:path of file
#O:None
def fileWellFormatted(pathFile):
	path=str( createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	
	if(" " in pathFile):
		logging.error("File's name has spaces.")
		sys.exit("Error: file's name has spaces.")
	
	try:
		pathFile.encode('ascii')
	
	except (UnicodeError):
		logging.exception("File's name couldn't be encoded in ascii")
		sys.exit("Error : File's name couldn't be encoded in ascii")


#Try to open file as a workbook
#I:path of file
#O:return workbook
def tryOpenWorkbookFile(pathFile):
	path=str( createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	try:
		#workbook doesn't need to be explicitly closed
		wb = xlrd.open_workbook(pathFile)
		return wb
	except(IOError):
		logging.exception("File couldn't be opened.")
		sys.exit("Error: File couldn't be opened.")
		
#Test if name pass criteria(no spaces,ascii only,alpha only)
#I:string to test
#O:None
def isNametATableName(name):
	path=str( createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	
	if(" " in name):
		logging.error("Name has spaces "+name.encode('utf8'))
		sys.exit("Error: Name has spaces "+name.encode('utf8'))
	
	try:
		name.encode('ascii')
	
	except UnicodeError as er:
		logging.exception("Name couldn't be encoded in ascii "+name.encode('utf8')+" "+er.message)
		sys.exit("Error: A column's name couldn't be encoded in ascii, don't use accents or special characters. "+name.encode('utf8'))
	
	for i in name.split("_"):
		if not i.isalpha():
			logging.exception("Name has special characters or numbers: "+ name.encode('utf8'))
			sys.exit("Error: Name has special characters or numbers: "+ name.encode('utf8') )
		
#Execute a Drop table sql query
#I:string name of the table, the cursor which executes queries
#O:None
def dropTable (nameTable):
	path=str( createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	drop = False
	logging.info("DROP TABLE "+str(nameTable))
	while not drop :
		
		try:
			logging.info("Trying to access database")
			conn = sqlite3.connect(getStoragePath(),timeout=10)
			c = conn.cursor()
		except:
			logging.exception("Database couldn't be reached"+getStoragePath())
			sys.exit("Error: Database couldn't be reached")
		
		logging.info("Success: connected to database")
		
		
		try:
			c.execute("DROP TABLE "+str(nameTable))
			drop = True
			# Save (commit) the changes
			conn.commit()
			# We can also close the connection if we are done with it.
			# Just be sure any changes have been committed or they will be lost.
			conn.close()
			c.close()
			logging.info("Done deleting files and dropping")

		except  sqlite3.Error as er:
			print("Drop:Smth went wrong")
			logging.warning( str(nameTable))
			logging.warning( er.message)
			
			
		
#return a list of each column's name (first line of a sheet has it)
#I:A sheet
#O:list namecols
def getColumns(sheet,allshnames):
	path=str( createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	# get names of columns (1st row value)
	namecols = []

	for colnum in range(sheet.ncols):
		nc = sheet.col_values(colnum)[0].split('|')
		# first line of that column	
		#necessary or else db attributes will look funny 			
		isNametATableName(nc[0])
		namecols.append(nc)
		for item in nc:
			if "reference=" in item:
				nvref = item.split("=")
				if len(nvref) > 1 :
					referenceSheet = False
					for nameSheet in allshnames:
						if nvref[1] == nameSheet:
							referenceSheet = True
					if not referenceSheet:
						logging.error("Reference without a sheet's name "+nvref[0].encode('utf8'))
						sys.exit("Error: A reference had no name corresponding to a sheet "+nvref[0].encode('utf8'))
				else:
					logging.error("Reference with no name "+nvref[0].encode('utf8'))
					sys.exit("Error: A reference had no name attached "+nvref[0].encode('utf8'))
			
	return namecols

#Write in a file the function boo + name of file parsed which will execute a sql query on the ids of a referenced table for each element in order to generate a table in the sqlform.grid of the view
#Multiple boo are needed to ensure multiple references
#I:the referenced table string,the column's name,the path of the file and the reference nuber (number of time createDict was called)
#O:None
def createDict(mainName,col,ref,filePath,numRef):
	#ref: name of table referenced
	#filePath: file's path which will be modified
	#numRef : reference number in case of multiple references in 'sheet'
	path=str(createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	
	with open(filePath,"a") as f:
		##Defining reference dict
				
		# boo links to dict for sqlform.grid
		# it will return a table with the first line containing the name of columns (listAttr) 
		# and the data of the table referenced (listValAttr) for each value separated by pipe contained in a list (listOfRefs)
		f.write('\ndef boo'+str(mainName)+str(numRef)+'(value,row,db):')
		f.write('\n    listOfRefs = []')
		f.write('\n    listAttr=[]')
		f.write('\n    rowvals = row.'+col+'.split("|")')
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
		f.write('\n                        RepresentedElement = row[attr]')
		f.write('\n                        if ".png" or  ".jpg" in row[attr]:')
		f.write('\n                            RepresentedElement=(doo'+str(mainName)+'(row[attr],None,db))')
		f.write('\n                        if "http" in row[attr]:')
		f.write('\n                            RepresentedElement=(A(row[attr],_href=row[attr]))')
		f.write('\n                        listValAttr.append(RepresentedElement)')
		f.write('\n        listOfRefs.append(listValAttr)')
		#comment the line under to stop displaying name columns in grid
		f.write('\n    listOfRefs.insert(0,listAttr)')
		f.write('\n    t=["w2p_odd odd","w2p_even even"]')
		f.write('\n    return TABLE(*[TR(r, _class=t[idx%2]) for idx,r in enumerate(listOfRefs)])')

#Much like createDict but focuses on displaying images from db.UploadedImages and the folder in static
#I:filePath string
#O:None
def linkingPics(mainName,filePath):
	#filePath: file's path which will be modified
	path=str(createFolder())
	logpath = str( createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	
	with open(filePath,"a") as f:
		##Defining reference dict
				
		# doo links to dict for sqlform.grid
		# pipe separates values 
		f.write('\ndef doo'+str(mainName)+'(value,row,db):')
		f.write('\n    listOfImgs = []')
		f.write('\n    for namePic in value.split("|"):')
		f.write('\n        if(( namePic != "" )and (len(db(namePic == db.UploadedImages.imageoname).select()) > 0)):')
		f.write('\n            listOfImgs.append(IMG(_src=URL("static","UploadedImages/"+str(db(namePic == db.UploadedImages.imageoname).select().first().Image)),_alt=namePic))') 
		f.write('\n        else:')
		f.write('\n            listOfImgs.append(namePic)')
		f.write('\n    return listOfImgs')	

# Defining tables in the model and return references
#I:path of the file,all sheets'name, all columns'name
#O:list tabReferences
def createTables(mainName,allshnames,allcolumns):           
	tabReferences = [] #used also to write represent attr in default controller
	with open("../applications/TEMPLATE/models/db_"+mainName+".py","a") as f:
		logging.info("Successfully opened db")
		logging.info("Creating tables")
		##Defining sheet table
		cptC = 0
		for nameSheet in allshnames:
			pk = []
			f.write('')
			f.write('\ndb.define_table("'+str(nameSheet).encode('utf-8')+'"')
			for c in allcolumns[cptC]:
				
				#nameColumn should always be first element
				s=""
				for item in c[+1:]:
					if item == "primarykey":
						pk.append(c[0])
					elif item ==  "idthis":
						s+=',"id"'
					elif "reference=" in item:
						nvref = item.split("=")
						tabReferences.append(nameSheet+"/"+nvref[1])
					elif (("type='integer'" == item) or ("type='float'" == item) or ("type='string'" == item)) :
							s+=","+item.encode('utf-8')
				f.write(',\nField("'+c[0].encode('utf-8')+'"'+s+')')
						
			cptC += 1
			if len(pk) > 0:
				f.write(',\nprimarykey=["'+pk[0].encode('utf-8')+'"')
				for pki in pk[+1:]:
					f.write(',"'+pki.encode('utf-8')+'"')
				f.write(']')
			f.write(')')

		##Defining some heplful functions
		#getDb -> called from default.py to get the same db as db.py
		f.write('\ndef getDb():\n    from os import path\n    module_path=os.path.abspath(os.path.dirname(__file__))\n    dbpath = module_path + "/../databases"\n    db_name = "storage.sqlite"\n    db = DAL("sqlite://"+ db_name ,folder=dbpath, auto_import=True)\n    return db')
		
		return tabReferences
#Determine if a table has already been defined in the past
#I:allfiles list of files, all sheets'name
#O:tableHere, the name of a table present in the database
def isTableAlreadyThere(allfiles,allshnames):		

	#allow to know if tables should be dropped
	tableFile = False
	tableHere = ""
	##Test if table's name is a file in TEMPLATE
	for i in allshnames:
		if not tableFile:
			for f in allfiles:
				if not tableFile:
					if str(i)+'.table' in f:
						tableFile = True
						tableHere = i
	return tableHere
#Execute dropTable and delete views on user's agreement as it deletes everything from those tables
#I:the name of the table already defined,allfiles list of files, all sheets'name
#O:None
def requestDrop(tableHere,allshnames,allfiles):
	##Warning user : delete possible
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
			
			drop = True
			
			for s in allshnames:
				delTable= ""
				for f in allfiles:
					#7 is the last digit of the hashkey of the files table
					if "7_"+str(s)+'.table' in f:
						
						dropTable(s)
						delTable = f
						
				if delTable is not "":		
					try:
						logging.info("Trying delete file")
						if os.name =="nt":
							subprocess.check_call(["DEL","/Q","..\\applications\\TEMPLATE\\databases\\"+str(delTable)],shell=True)
						else:
							subprocess.check_call(["rm","-rfv","../applications/TEMPLATE/databases/"+str(delTable)])
						
						logging.info("Successfully deleted file")
					except subprocess.CalledProcessError as er:
						logging.exception("Error while deleting "+str(f)+" : "+er.message )
						sys.exit("Error: Cannot erase file")
			
		
		elif answer == "n":
			logging.info("Stopping script on user's demand")
			print "Stopping script"
			exit()
			
#Create controllers in web2py, define represent which calls boo functions and define forms to create plots
#I:all list containing all sheets'name,tabReferences is a list of relation of references between tables/sheets ("A/B"),workbook created from the file in arg, the file's name minus path and extension,the path of storage.sqlite,the path of the file
#O:None
def createControllers(allshnames,tabReferences,wb,mainName,script_path,pathFile):
	#used for calling scriptInit once page has loaded
	with open("../applications/TEMPLATE/controllers/"+mainName+".py","a") as f:
		logging.info("Successfully opened "+mainName+".py")
			
		# then, we define all links to views from this file
		for nameTable in allshnames: 
			f.write('\ndef '+nameTable+'():')
			f.write('\n    db = getDb()')
			f.write('\n    table = db.'+nameTable)
			# necessary to differentiate to prevent dal errors
			#for each reference
			for idx,r in enumerate(tabReferences):
				listR=r.split("/")
				#listR[1] = table referenced
				#for each column of the table
				for c in getColumns(wb.sheet_by_name(nameTable),allshnames):
					for item in c: 
						if 'reference' in item :
						#s1 is what is referenced c0 is the name of the column which references item1
							if ((listR[1] == item.split('=')[1])) :
								f.write('\n    db.'+listR[0]+'.'+c[0]+'.represent = lambda val,row:boo'+mainName+str(idx)+'(val,row,db)')
							
			for idx,c in enumerate(getColumns(wb.sheet_by_name(nameTable),allshnames)):
				for item in c:
					#used to display img
					if 'dlimage' in item :
						f.write('\n    db.'+nameTable+'.'+c[0]+'.represent = lambda val,row:doo'+mainName+'(val,row,db)')						#used to display html links
					elif 'webaddr' in item :
						f.write('\n    db.'+nameTable+'.'+c[0]+'.represent = lambda val,row:A(val,_href=val)')


					
			'''
			f.write('\n    rows = db(table).select()')
			f.write('\n    if (len(rows) == 0):')
			f.write('\n        initData()')
			'''
			#create a form with columns, declared as integer or float, as options plus the type of plot and will call makePlot only if at least one column fulfil this condition
			f.write('\n    rows = db(table).select()')
			s="\n    form = DIV(FORM("
			atLeastOne = False
			for c in getColumns(wb.sheet_by_name(nameTable),allshnames):
				if (("type='integer'" in c) or( "type='float'" in c)):
					atLeastOne = True
					s+="\nDIV(LABEL('"+c[0]+"'),INPUT(_name='"+c[0]+"',_type='checkbox'),_class='row'),"
			s+="\nDIV(LABEL('Simple plot'),INPUT(_type='radio',_name='plot',_value='plot' ,value='plot'),\nLABEL('3D Poly'),INPUT(_type='radio',_name='plot',_value='3dpoly'),\nLABEL('Subplots'),INPUT(_type='radio',_name='plot',_value='sub'),_class='row'),"
			s+="\nINPUT(_type='submit',_class='btn btn-primary',_name='makeplot'),_class='form-horizontal',_action='',_method='post')"
			s+=',_class="jumbotron")'
			if atLeastOne:
				f.write(s)
			else:
				f.write("\n    form=''")
				
			#create a form with columns, declared as integer or float, as options for X,Y,Z axes
			s="\n    form2 = DIV(FORM("
			select="SELECT("
			cptFields = 0
			for c in getColumns(wb.sheet_by_name(nameTable),allshnames):
				if (("type='integer'" in c) or( "type='float'" in c)):
					select+='"'+c[0]+'",'
					cptFields+=1
			for axe in ['X','Y','Z']:
				s+="LABEL('"+axe+"'),"+select+'_name="'+axe+'"),\n'
			s+="INPUT(_type='submit',_class='btn btn-primary',_name='makeplotuser'),_class='form-horizontal',_action='',_method='post')"
			s+=',_class="jumbotron")'
			
			if cptFields<3:
				f.write("\n    form2=''")
			else:
				f.write(s)
				
			#display an image by calling makePlot and stating the type of plot, the fiels, the name of the table and the file to change
			f.write("\n    plot=DIV('')")
			f.write('\n    if len(request.post_vars)>0 and ("makeplot" in request.post_vars or "makeplotuser" in request.post_vars): ')
			f.write("\n        nameTable ='"+nameTable+"'")
			f.write("\n        foo = os.path.abspath(os.path.dirname(__file__))")
			f.write("\n        foo = foo + '/../static/foo.png' ")
			f.write("\n        vars = request.post_vars.keys()")
			f.write('\n        fields=""')
			f.write("\n        typeplot=''")  
			f.write('\n        if "makeplot" in request.post_vars and len(request.post_vars)>2:')
			f.write("\n            vars.remove('makeplot')") 
			f.write("\n            for v in vars :")
			f.write("\n                if v == 'plot' :")
			f.write("\n                    typeplot = request.post_vars.plot")
			f.write("\n                else :")
			f.write("\n                    fields+=str(v)+','")
			f.write("\n            fields=fields[:-1]")
			f.write("\n            makePlot(typeplot,fields,nameTable,foo)")
			f.write("\n            plot=IMG(_src=URL('static','foo.png'),_alt='plot')")
			f.write('\n        elif "makeplotuser" in request.post_vars:')
			f.write('\n            typeplot="3daxes"')
			f.write("\n            vars.remove('makeplotuser')")
			f.write("\n            for v in vars :")
			f.write("\n                fields+=request.post_vars[v]+','")
			f.write("\n            fields=fields[:-1]")
			f.write("\n            makePlot(typeplot,fields,nameTable,foo)")
			f.write("\n            plot=IMG(_src=URL('static','foo.png'),_alt='plot')")
			f.write('\n    records=SQLFORM.grid(table,paginate=10,maxtextlength=256,showbuttontext=False)')
			f.write("\n    if form != '' or form2 != '':")
			f.write("\n        caption=H2(T('Select columns to create a plot'))")
			f.write("\n    else:")
			f.write("\n        caption=''")			
			f.write('\n    return dict(caption=caption, form=form, form2=form2, plot=plot, records=records)')

		'''	
		# used in case main table is empty	
		f.write('\ndef initData():')
		f.write('\n    from subprocess import check_call')
		f.write('\n    try:\n        subprocess.check_call(["python",'+'"'+str(script_path).replace("\\","/")+"/scriptInit.py"+'","'+pathFile.replace("\\","/")+'"'+"])")
		f.write('\n    except subprocess.CalledProcessError:\n        sys.exit("Error : scriptInit.py could not be reached")')
		'''
		#used to create plot
		f.write('\ndef makePlot(typeplot,fields,nameTable,whereToSave):')
		f.write('\n    from subprocess import check_call')
		f.write('\n    try:')
		f.write('\n        subprocess.check_call(["python",'+'"'+str(script_path).replace("\\","/")+"/scriptPlot.py"+'",typeplot,fields,nameTable,whereToSave])')
		f.write('\n    except subprocess.CalledProcessError:')
		f.write('\n        sys.exit("Error : scriptPlot.py could not be reached")')					

#Return a list of string from view folder to generate a menu
#I:None
#O:list of menu and submenus		
def createListeMenu():
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
	return listmenu
#Recreate the menu of menu.py
#I:list of menu and submenus
#O:None
def createMenu(listmenu):	
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

### Main execution of the code

#prevent execution on import from scriptInit
if __name__ == '__main__':
	script_path=os.path.abspath(os.path.dirname(__file__))
	path=str(createFolder())
	logpath = str(createLogs(path))
	print ("Consult log file at "+logpath)
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	logging.info('Log created at :'+getTimeH())
	logging.info("script.py is executed")
	logging.info("Looking for the file in argument")
	#if there is at least an argument, the script is launched
	if( len(sys.argv)>1 ):
		logging.info("File found")
		#changing dir to excel2web2py
		try:
			logging.info("Trying to look for excel2web2py folder")
			os.chdir(script_path)
			logging.info("excel2web2py* folder found")
		except os.error as er:
			logging.exception("Error while looking for excel2web2py folder: " + er.message)
			sys.exit("Error: Cannot find excel2web2py folder")
			
		try:
			logging.info("Trying to look for database")
			os.path.isfile(getStoragePath())
			logging.info("database found")
		except os.error as er:
			logging.exception("Error while looking for database: " + er.message)
			sys.exit("Error: Cannot find database")
			
		
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

		mainName = sys.argv[2].split('.')[0]
		
		allfiles = os.listdir('../applications/TEMPLATE/databases')
		
		tableHere = isTableAlreadyThere(allfiles,allshnames)
		if str(tableHere) != "":
			logging.error("A table has already this name : "+tableHere)
			sys.exit("Error: A sheet has a name already defined in the database "+tableHere)
		
		
		
		for nameSheet in allsheets:
			allcolumns.append(getColumns(nameSheet,allshnames))
		for sheet in allcolumns:
			for element in sheet:
				nameColumn=element[0]
				cptC=0
				for element in sheet:
					if element[0]==nameColumn:
						cptC+=1
				if cptC > 1:
					logging.error("Column with same name "+nameColumn)
					sys.exit("Error: Column with same name "+nameColumn)
		logging.info("Successfully retrieved the name of the columns")
	
		try:
			logging.info("Trying to recover backup of db")
			if os.name =="nt":
				subprocess.check_call(["copy","/Y",'..\\applications\\TEMPLATE\\models\\db_backup.py','..\\applications\\TEMPLATE\\models\\db_'+mainName+'.py'],shell=True)
			else:
				subprocess.check_call(["cp","-v","../applications/TEMPLATE/models/db_backup.py","../applications/TEMPLATE/models/db_"+mainName+".py"])	
			logging.info("Successfully recover backup of db")
		except subprocess.CalledProcessError as er:
			logging.exception("Error while retrieving db_backup: " + er.message)
			sys.exit("Error: Cannot access db_backup")
		
		tabReferences = createTables(mainName,allshnames,allcolumns)
		

		#requestDrop(tableHere,allshnames,allfiles)

		#actualize allfiles in case of delete
		#allfiles = os.listdir('../applications/TEMPLATE/databases')
				
		logging.info("Writing in db finished")
		logging.info("Closing file")
			

		
		### Insert Rows
		try:
			logging.info("Trying to recover backup of default")
			if os.name =="nt":
				subprocess.check_call(["copy","/Y","..\\applications\\TEMPLATE\\controllers\\default_backup.py","..\\applications\\TEMPLATE\\controllers\\"+mainName+".py"],shell=True)
			else:
				subprocess.check_call(["cp","-v","../applications/TEMPLATE/controllers/default_backup.py","../applications/TEMPLATE/controllers/"+mainName+".py"])
			
			
			logging.info("Successfully recover backup of default")
		except subprocess.CalledProcessError as er:
			logging.exception("Error while retrieving default_backup : " + er.message)
			sys.exit("Error: default_backup cannot be found")

		###Dicts and Images
		#we need to define 'boo' functions before the views functions, they will be used to call referenced records
		logging.info("Creating dicts")

		for namesheet in allshnames:		
				for idx,r in enumerate(tabReferences):
				#column|reference=OtherSheet
				#r = sheet/OtherSheet
					if namesheet == r.split('/')[0]:
						columnRef = ""
						for c in getColumns(wb.sheet_by_name(namesheet),allshnames):
						#c = [name,keyword,keyword,...]
							idxc = 0
							while columnRef == "" and idxc < len(c):
								item = c[idxc]
								if 'reference' in item and r.split('/')[1] in item :
									columnRef = c[0]
								idxc+=1
						if columnRef != "":
							createDict(mainName,columnRef,r.split('/')[1],"../applications/TEMPLATE/controllers/"+mainName+".py",idx)
                linkingPics(mainName,"../applications/TEMPLATE/controllers/"+mainName+".py")

		logging.info("Dicts written")

		#Create Controllers
		createControllers(allshnames,tabReferences,wb,mainName,script_path,sys.argv[1])

			
		logging.info("Writing in controller "+mainName+" finished")
		logging.info("Closing file")
		
		###create new views
		#Delete old folder
		try:
				if os.name =="nt":
					subprocess.call(["RD","/S","/Q","..\\applications\\TEMPLATE\\views\\"+mainName],shell=True)
				else:
					subprocess.call(["rm","-rfv","../applications/TEMPLATE/views/"+mainName+"/"])
					
				logging.info("Successfully deleted folder :"+mainName)
		except subprocess.CalledProcessError as er:
			print er.message
		try:
			if os.name =="nt":
				subprocess.call(["mkdir","..\\applications\\TEMPLATE\\views\\"+mainName],shell=True)
			else:
				subprocess.call(["mkdir","-v","../applications/TEMPLATE/views/"+mainName+"/"])
			logging.info("Successfully created view folder :"+mainName)
		except subprocess.CalledProcessError as er:
			logging.exception("Error while creating view folder: "+er.message)
			sys.exit("Error: Error happened when creating the view folder"+mainName.encode('utf8'))
		
		try:
			logging.info("Trying to create views")
			for nameTable in allshnames:
				if os.name =="nt":
					subprocess.check_call(["copy","/Y","..\\applications\\TEMPLATE\\views\\default\\table.html","..\\applications\\TEMPLATE\\views\\"+mainName+"\\"+nameTable+".html"],shell=True)
				else:
					subprocess.check_call(["cp","-v","../applications/TEMPLATE/views/default/table.html","../applications/TEMPLATE/views/"+mainName+"/"+nameTable+".html"])
			
				logging.info("Successfully created view :"+nameTable)
		except subprocess.CalledProcessError as er:
			logging.exception("Error while creating views files : "+er.message)
			sys.exit("Error: Error happened when creating views")
			
		###create new views end
		
		
		### Making menu
		try:
			logging.info("Trying to recover backup of menu")
			if os.name =="nt":
				subprocess.check_call(["copy","/Y","..\\applications\\TEMPLATE\\models\\backup_menu.py","..\\applications\\TEMPLATE\\models\\menu.py"],shell=True)
			else:
				subprocess.check_call(["cp","-v","../applications/TEMPLATE/models/backup_menu.py","../applications/TEMPLATE/models/menu.py"])
			
			logging.info("Successfully recover backup of menu")
		except subprocess.CalledProcessError as er:
			logging.exception("Error while retrieving backup_menu : "+er.message)
			sys.exit("Error: menu_backup cannot be found")
			
		listmenu = createListeMenu()	
		#Shortcuts
		createMenu(listmenu)

			
		### Making menu end
			
		###launch web2py
		'''
		try:
			logging.info("Trying to launch web2py")
			if os.name =="nt": 
				subprocess.check_call(["%cd%..\\web2py.exe"],shell=True)
			else:
				subprocess.check_call(["python", "../web2py.py"])
		except subprocess.CalledProcessError as er:
			logging.exception("Error while executing web2py : " + er.message)
			sys.exit("Error: python is no present on this computer or web2py could not be reached")
		
		launch web2py end
		'''
	else:
		sys.exit("Error : no file selected")
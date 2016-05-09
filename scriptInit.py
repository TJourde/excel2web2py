#!usr/bin/env/python
# -*- coding: utf-8 -*-
import sys, os, time, errno
import os.path
import sqlite3
import logging
#lib read excel files
import xlrd
import script

#execute sql request to insert data
def insertRowsData(nameTable,sheet,cursor):
	path=str( script.createFolder())
	logpath = str( script.createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	query = ""
	idcpt = 0
	firstline=True
	isThereId = False
	##insert data of sheets
	for rownum in range(sheet.nrows):
		if(not firstline):
			query = "INSERT INTO "+nameTable+" VALUES ("
			vals = ""
			if not isThereId:
				vals += str(idcpt)+","
			for idx,rowval in enumerate(sheet.row_values(rownum)):
				#for null value
				if rowval is "":
					if (('integer' in sheet.col_values(idx)[0]) or ('float' in sheet.col_values(idx)[0])):
						vals += '"0",'
					else:
						vals += '"",'
				else:
				#for int/float value
					try:
						vals+='"'+rowval+'"'+','
					except:
						vals+='"'+str(rowval)+'"'+','
			vals=vals[:-1]
			query+=vals
			query+=')'

			if vals.strip(',""') == str(idcpt):
				query=""
			else:
				idcpt+=1
		else:
			if any("idthis" in s for s in sheet.row_values(rownum)):
				isThereId = True
			firstline=False
		try:
			logging.info(query)
			cursor.execute(query)
		except sqlite3.Error as er:
			print("Ins:Smth went wrong")
			logging.warning( er.message)
			pass			
			#sys.exit("Erreur insertion")
	


if len(sys.argv) > 1:
	path=str(script.createFolder())
	logpath = str(script.createLogs(path))
	logging.basicConfig(filename=logpath,level=logging.DEBUG)
	logging.info("scriptInit.py is executed")
	logging.info("Trying to open file")
	wb = script.tryOpenWorkbookFile(sys.argv[1])
	logging.info("Successfully opened the file")
	logging.info("Trying to get sheets")
	allsheets = wb.sheets()
	allshnames = wb.sheet_names()
	allcolumns = []
	for i in allsheets:
		allcolumns.append(script.getColumns(i))
	logging.info("Successfully opened the sheets")
	logging.info("Connecting to the database")
	# Insert rows of data
	conn = sqlite3.connect(script.getStoragePath())
	c = conn.cursor()
	logging.info("Successfully connected")
	logging.info("Insert requests")
	for s in allsheets:
		insertRowsData(s.name,s,c)
		
	# Save (commit) the changes
	conn.commit()
	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()
	logging.info("Requests over")

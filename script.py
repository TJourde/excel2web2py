#!usr/bin/env/python
# -*- coding: utf-8 -*-
import sys, os
import os.path
import sqlite3
#lib read excel files
import xlrd


if( len(sys.argv)>1 ):
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
	if(os.path.isdir("tmp")):
		if(os.path.isfile("tmp/"+sys.argv[1].split('.')[0]+".db")):
			os.remove("tmp/"+sys.argv[1].split('.')[0]+".db")
	else:
		os.mkdir("tmp")


	#db
	conn = sqlite3.connect("tmp/"+sys.argv[1].split('.')[0]+".db")
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

else:
	print("Erreur : pas de fichier sélectionné")

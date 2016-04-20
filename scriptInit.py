#!usr/bin/env/python
# -*- coding: utf-8 -*-
import sys, os, time, errno
import os.path
import sqlite3
import logging
#lib read excel files
import xlrd
import logging
import subprocess
import script

print "hi"
path=str(script.createFolder())
logpath = str(script.createLogs(path))
logging.basicConfig(filename=logpath,level=logging.DEBUG)
logging.info("scriptInit.py is executed")
logging.info("Trying to open file")
wb = script.tryOpenWorkbookFile(sys.argv[1])
logging.info("Successfully opened the file")
logging.info("Trying to get sheets")
allsheets = wb.sheets()
logging.info("Successfully opened the sheets")
logging.info("Connecting to the database")
# Insert rows of data
conn = sqlite3.connect(script.getStoragePath())
c = conn.cursor()
logging.info("Successfully connected")
logging.info("Insert requests")
for s in allsheets:
	script.insertRowsData(s.name,s,c)
# Save (commit) the changes
conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
logging.info("Requests over")


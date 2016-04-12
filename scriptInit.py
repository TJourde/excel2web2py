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


path=str(script.createFolder())
logpath = str(script.createLogs(path))
logging.basicConfig(filename=logpath,level=logging.DEBUG)
logging.info("scriptInit.py is executed")
logging.info("Trying to open file")
wb = script.tryOpenWorkbookFile(sys.argv[1])
logging.info("Successfully opened the file")
logging.info("Trying to get sheet")
sh = script.getSheet(wb)
logging.info("Successfully opened the sheet")
logging.info("Trying to the name of the sheet")
shname = script.getNameFirstSheetAsTableName(wb)
logging.info("Successfully retrived the name of the sheet")
logging.info("Trying to the names of the columns")
namecols= script.getColumnsNames(sh,shname)
logging.info("Successfully retrieved the name of the columns")

# Insert rows of data
conn = sqlite3.connect(script.getStoragePath())
c = conn.cursor()
script.insertRowsData(shname,sh,c)
# Save (commit) the changes
conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()


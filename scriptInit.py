#!usr/bin/env/python
# -*- coding: utf-8 -*-
import sys, os, time, errno
import os.path
import sqlite3
import logging
#lib read excel files
import xlrd
import subprocess
import script
wb = script.tryOpenWorkbookFile(sys.argv[1])
sh = script.getSheet(wb)
shname = script.getNameFirstSheetAsTableName(wb)
namecols= script.getColumnsNames(sh,shname)
# Insert rows of data
conn = sqlite3.connect("/home/tanguyl/Documents/projetPython/web2py/applications/TEMPLATE/databases/storage.sqlite")
c = conn.cursor()
script.insertRowsData(shname,sh,c)
# Save (commit) the changes
conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()


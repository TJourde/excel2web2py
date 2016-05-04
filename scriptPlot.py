#!usr/bin/env/python
# -*- coding: utf-8 -*-
import sys, os, time, errno
import matplotlib.pyplot as plt
import sqlite3
import script
if len(sys.argv) > 3:
	conn = sqlite3.connect(script.getStoragePath())
	c = conn.cursor()
	typeplot = sys.argv[1]
	fields = sys.argv[2]
	nameTable = sys.argv[3]
	whereToSave = sys.argv[4]
	if typeplot == 'hist' :
		c.execute("Select "+fields+" from "+nameTable)
		plt.hist(c.fetchall())
		plt.xlabel('Value')
		plt.ylabel('Number')
	elif typeplot == 'sub' :
		for idx,item in enumerate(fields.split(',')) :
			plt.subplot(len(fields.split(',')),1,idx+1)
			c.execute("Select "+item+" from "+nameTable)
			plt.plot(c.fetchall())
			plt.ylabel(item+' (Value)')
		plt.xlabel('Number')
	else :
		c.execute("Select "+fields+" from "+nameTable)
		plt.plot(c.fetchall())
		plt.xlabel('Number')
		plt.ylabel('Value')
	conn.close()
	plt.title('Plot of A with '+fields)
	plt.savefig(whereToSave)
	plt.clf()
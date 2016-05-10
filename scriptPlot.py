#!usr/bin/env/python
# -*- coding: utf-8 -*-
import sys
import matplotlib.pyplot as plt
import sqlite3
import script
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np

#Color Converter from matplotlib
#I:letter
#O:Color
def cc(arg):
    return colorConverter.to_rgba(arg, alpha=0.6)

if len(sys.argv) > 3:
	conn = sqlite3.connect(script.getStoragePath())
	c = conn.cursor()
	typeplot = sys.argv[1]
	fields = sys.argv[2]
	nameTable = sys.argv[3]
	whereToSave = sys.argv[4]
	colors = ['r','b','g','y','c','m','k','w']
	if ((typeplot == '3dpoly') and (len(fields.split(','))<len(colors))):
		c.execute("Select "+fields+" from "+nameTable)
		res = c.fetchall()
		fig = plt.figure()
		ax = fig.gca(projection='3d')

		xs = np.arange(0, 10, 0.4)
		verts = []
		zs = [1.0*i for i in range(0,len(fields.split(',')))]
		nres = []
		zmin = 0
		zmax = 0
		for idx in range(0,len(fields.split(','))):
			r=[0]
			for item in res:
				if item[idx] < zmin:
					zmin = item[idx]
				if item[idx] > zmax:
					zmax = item[idx]
				r.append(item[idx])
			length_data=len(r)-1
			r.append(0)
			zipr=zip([(i-1)*1.0 for i in range(0,len(r))],r)
			for idx,item in enumerate(zipr):
				if item[0] < 0.0:
					zipr[idx]=(0.0,0.0)
				#minus 1 because 0 is the first element
				if item[0] == length_data:
					zipr[idx]=((length_data-1)*1.0,0.0)
			nres.append(list(zipr))
		poly = PolyCollection(nres, facecolors=[cc(letter) for idx,letter in enumerate(colors) if idx < len(fields.split(','))])
		poly.set_alpha(0.7)
		ax.add_collection3d(poly, zs=zs, zdir='y')
		ax.set_xlabel('Number')
		#minus 1 because we add an element at the same X that the last element but with Y=0.0 at the end
		ax.set_xlim3d(0, len(res)-1)
		label = "\n"*len(fields.split(','))
		for idx,f in enumerate(fields.split(',')):
			label+=f+" is "+colors[idx]+"\n"
		ax.set_ylabel(label)
		ax.set_ylim3d(-1, len(fields.split(',')))
		ax.set_zlabel('Value')
		ax.set_zlim3d(zmin, zmax)
	elif typeplot == 'sub' :
		for idx,item in enumerate(fields.split(',')) :
			plt.subplot(len(fields.split(',')),1,idx+1)
			c.execute("Select "+item+" from "+nameTable)
			plt.plot(c.fetchall(),marker='o')
			plt.ylabel(item+' (Value)')
		plt.xlabel('Number')
	else :
		c.execute("Select "+fields+" from "+nameTable)
		res = c.fetchall()
		#res is a list of tuple
		cpt=0

		while cpt < len(res[0]):
			tab=[]
			for item in res:
				tab.append(item[cpt])
			plt.plot(tab,marker='o',label=fields.split(',')[cpt])
			cpt+=1
		plt.xlabel('Number')
		plt.ylabel('Value')
		
	plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1,ncol=len(fields.split(',')), mode="expand", borderaxespad=0.)
	conn.close()
	plt.title('Plot of '+nameTable)
	plt.savefig(whereToSave)
	plt.clf()
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
	#8 columns at once max
	if ((typeplot == '3dpoly') and (len(fields.split(','))<len(colors))):
		c.execute("Select "+fields+" from "+nameTable)
		res = c.fetchall()
		#res is a list of tuples [(line1.elt1,line2.elt1,line3.elt1),(line1.elt2,line2.elt2,line3.elt2)...]
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		zs = [1.0*i for i in range(0,len(fields.split(',')))]
		#nres will contain the sorted lists [(line1.elt1,line1.elt2,...),(...)...]
		nres = []
		zmin = 0
		zmax = 0
		# number of lines == len(fields.split(',')
		for idx in range(0,len(fields.split(','))):
			line=[0]
			for item in res:
				if item[idx] < zmin:
					zmin = item[idx]
				if item[idx] > zmax:
					zmax = item[idx]
				line.append(item[idx])
			#number of dots
			length_data=len(line)-1
			line.append(0)
			zipr=zip([(i-1)*1.0 for i in range(0,len(line))],line)
			
			#create a point at y = 0.0 on the first and last elt
			zipr[0]=(0.0,0.0)
			#minus 1 because 0 is the first element
			zipr[-1]=((length_data-1)*1.0,0.0)
			
			nres.append(list(zipr))
		
		#create the polys	
		poly = PolyCollection(nres, facecolors=[cc(letter) for idx,letter in enumerate(colors) if idx < len(fields.split(','))])
		#transparency
		poly.set_alpha(0.7)
		#create the plot
		ax.add_collection3d(poly, zs=zs, zdir='y')
		ax.set_xlabel('Number')
		#minus 1 because we add an element (0.0,0.0) at the end of each poly
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
			plt.subplot(len(fields.split(',')),1,idx+1,label=str(idx+1))
			c.execute("Select "+item+" from "+nameTable)
			plt.plot(c.fetchall(),marker='o')
			plt.ylabel(item+' (Value)')
		plt.xlabel('Number')
	elif typeplot == '3daxes' :
		c.execute("Select "+fields+" from "+nameTable+" Order by "+fields.split(',')[0])
		res = c.fetchall()
		#res is a list of tuples [(line1.elt1,line2.elt1,line3.elt1),(line1.elt2,line2.elt2,line3.elt2)...]
		fig = plt.figure()
		ax = fig.gca(projection='3d')
		x = np.array([item[0] for item in res])
		y = np.array([item[1] for item in res])
		z = np.array([item[2] for item in res])
		#create the plot
		ax.scatter(x,y,z,label="xyz")
		ax.set_xlabel('X : '+fields.split(',')[0])
		ax.set_ylabel('Y : '+fields.split(',')[1])
		ax.set_zlabel('Z : '+fields.split(',')[2])
		
		
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
		
	conn.close()
	plt.title('Plot of '+nameTable)
	plt.savefig(whereToSave)
	plt.clf()

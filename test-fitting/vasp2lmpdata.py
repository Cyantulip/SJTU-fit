import os
import numpy as np

def xdatcar2xyz(xdatcar: str, datapart2:str, xyz: str):
	with open(xdatcar, 'r') as xdatcar, open(xyz, 'w') as xyz:
		system = xdatcar.readline()
		scale = float(xdatcar.readline().rstrip('\n'))

#get lattice vectors
		a1 = np.array([ float(s)*scale for s in xdatcar.readline().rstrip('\n').split() ])
		a2 = np.array([ float(s)*scale for s in xdatcar.readline().rstrip('\n').split() ])
		a3 = np.array([ float(s)*scale for s in xdatcar.readline().rstrip('\n').split() ])

#read xdatcar

		element_names = xdatcar.readline().rstrip('\n').split()
		element_dict = {}
		element_numbers = xdatcar.readline().rstrip('\n').split()

		Natom = 0
		Ntype = len(element_names)
		Nname = []
		for t in range(Ntype):
			Natom += int(element_numbers[t])
			for i in range(int(element_numbers[t])):
				Nname.append(element_names[t])

		direct = np.zeros([Natom,3])
		cart = np.zeros([Natom,3])

		#while True:
		line = xdatcar.readline()
		#	if len(line) == 0:
		#		break
		xyz.write('Atoms' + '\n' + '   ' + '\n')

		for atom in range(Natom):
			c = xdatcar.readline().rstrip('\n').split()
			direct[atom,:] = np.array([ float(s) for s in c ])
			cart[atom,:] = direct[atom,0]*a1 + direct[atom,1]*a2 + direct[atom,2]*a3

		i=-1
		lines = open(datapart2, 'r').readlines()
		for line in lines[ 2:Natom+2 ]:
			i +=1
			s =line.split()
			xyz.write('%3d %3d %3d  %.5f  %.5f  %.5f  %.5f  %1s  %5s\n' %(int(s[0]), int(s[1]), int(s[2]), float(s[3]), cart[i,0], cart[i,1], cart[i,2], str(s[7]), str(s[8])))
		xyz.write('\n')


def generate_datafiles(filename: str):
	output1 = filename + '-part1'
	output2 = filename + '-part2'
	output3 = filename + '-part3'
	i=0
	M=0
	with open(filename, 'r') as f:
		for line in f.readlines():
			i += 1
			if line.startswith('Atoms'):
				M = i

	i=0
	N=0
	with open(filename, 'r') as f:
		for line in f.readlines():
			i += 1
			if line.startswith('Bonds'):
				N = i

	with open(filename, 'r') as f, open(output1, 'w') as o1:
		for line in f.readlines()[0:M-1]:
			o1.write(line)
			
	with open(filename, 'r') as f, open(output2, 'w') as o2:
		for line in f.readlines()[M-1:N-1]:
			o2.write(line)
			
	with open(filename, 'r') as f, open(output3, 'w') as o3:
		for line in f.readlines()[N-1:]:
			o3.write(line)
	return(int(N-M-3))


import numpy as np
#from copy import deepcopy

xdatcar = open('XDATCAR', 'r')
xyz = open('XDATCAR.xyz', 'w')

system = xdatcar.readline()
scale = float(xdatcar.readline().rstrip('\n'))
print(scale)

#get lattice vectors
a1 = np.array([ float(s)*scale for s in xdatcar.readline().rstrip('\n').split() ])
a2 = np.array([ float(s)*scale for s in xdatcar.readline().rstrip('\n').split() ])
a3 = np.array([ float(s)*scale for s in xdatcar.readline().rstrip('\n').split() ])

comment = 'Lattice=\"' + str(a1[0]) + ' ' + str(a1[1]) + ' ' + str(a1[2])
comment = comment + str(a2[0]) + ' ' + str(a2[1]) + ' ' + str(a2[2])
comment = comment + str(a3[0]) + ' ' + str(a3[1]) + ' ' + str(a3[2]) + '\"'

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

print(Ntype, Natom)

direct = np.zeros([Natom,3])
#cart = np.zeros([Natom,3])

while True:
	line = xdatcar.readline()
	if len(line) == 0:
		break
	xyz.write('Atoms' + '\n' + '   ' + '\n')

	for atom in range(Natom):
		c = xdatcar.readline().rstrip('\n').split()
		direct[atom,:] = np.array([ float(s) for s in c ])
		cart = direct[atom,0]*a1 + direct[atom,1]*a2 + direct[atom,2]*a3
		#xyz.write(Nname[atom] + ' ' + str(cart[0]) + ' ' + str(cart[1]) + ' ' + str(cart[2]) + '\n')
		xyz.write(Nname[atom] + '  %.6f   %.6f   %.6f' %(cart[0], cart[1], cart[2]) + '\n')

xdatcar.close()
xyz.close()

import os

def generate_datafiles(filename: str):
	i=0
	N=0
	output1 = filename + '-part1'
	output2 = filename + '-part2'

	with open(filename, 'r') as f, open(output1, 'w') as o1:
		for line in f.readlines():
			if line.startswith('Atoms'):
				break
			o1.write(line)

	with open(filename, 'r') as f:
		for line in f.readlines():
			i += 1
			if line.startswith('Bonds'):
				N = i

	with open(filename, 'r') as f, open(output2, 'w') as o2:
		for line in f.readlines()[N-1:]:
			o2.write(line)
			

generate_datafiles('paa-11.data')

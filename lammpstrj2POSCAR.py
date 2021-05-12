import os


class Atom:
    def __init__(self, type, x, y, z):
        for typename in ['Ti', 'O', 'C', 'H']:
            if type.startswith(typename):
                self.type = typename
                break
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)


def write_poscar(filename, atoms):
    with open(filename, 'w') as f:
        f.write('Transfer by qvasp\n')
        f.write('    1.0\n')
        f.write('    8.906000    0.000000    0.000000\n')
        f.write('    0.000000    13.146600    0.000000\n')
        f.write('    0.000000    0.000000    24.138600\n')
        keys = atoms.keys()
        N = list(map(lambda x: str(len(atoms[x])), keys))
        f.write('  %s\n' % '  '.join(keys))
        f.write('  %s\n' % '  '.join(N))
        f.write('Cartesian\n')
        for key in keys:
            for atom in atoms[key]:
                f.write('     %.9f         %.9f         %.9f\n' %
                        (atom.x, atom.y, atom.z))


lines = open('trj.nvt').readlines()
line_per_frame = lines.index('ITEM: TIMESTEP\n', 1) - \
                 lines.index('ITEM: TIMESTEP\n', 0)
N = int(len(lines) / line_per_frame)
assert N * line_per_frame == len(lines)
for i in range(N):
    if not os.path.exists('VASP-%d' % i):
        os.mkdir('VASP-%d' % i)
    atoms = {'Ti': [], 'C': [], 'O': [], 'H': []}
    for line in lines[i*line_per_frame + 9:(i+1)*line_per_frame]:
        _, type, _, x, y, z = line.split()
        atom = Atom(type, x, y, z)
        atoms[atom.type].append(atom)
    write_poscar('VASP-%d/POSCAR' % i, atoms)
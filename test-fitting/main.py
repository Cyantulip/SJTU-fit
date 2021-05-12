#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from hyperopt import fmin, hp, tpe
from typing import Dict, Union, List
from utils import get_qm_energy, generate_lammps_input_slab, generate_lammps_input_bin, get_lammps_energy, run_lammps
from utils import generate_lammps_input_in, get_qm_force, get_lammps_force
from sklearn.metrics import mean_squared_error, r2_score
import os, sys
import re
import subprocess
from lammps import PyLammps
from vasp2lmpdata import generate_datafiles, xdatcar2xyz

def main():
    E_qm = []
    F_qm = []
    #for i in range(7,15):
    for i in [7,8,9]:
        E_qm.append(get_qm_energy('/share/workspace/zhaolingci/task-BASF-May2021/VASP-%d/OUTCAR' % i))
        F_qm.append(get_qm_force('/share/workspace/zhaolingci/task-BASF-May2021/VASP-%d/OUTCAR' % i))
    
    E_target = [j * 23.06 for j in E_qm]
    E_target_scale = [j / 1.0 for j in E_target]
    F_target = F_qm

    op = open('output.log', 'w')

    def objective(params: Dict[str, float]):
        E_lammps = []
        F_lammps = []
        mol_paa = -6.3903
        #subprocess.run('bash checkCHG.sh %f' % params['chg'] ,shell=True, cwd='/lustre/home/acct-nishsun/nishsun/trash/old/workspace/zhaolingci/hyperopt/test+force/paa1-14')
        #for i in range(7,15):
        for i in [7,8,9]:
            generate_lammps_input_slab('/share/workspace/zhaolingci/task-BASF-May2021/test-fitting/rutile110/rut-slabC.data', 'slab.data', params)
            run_lammps('rut-slab.in', 'slab')
            Natoms = generate_datafiles('mini6.data')
            xdatcar2xyz('/share/workspace/zhaolingci/task-BASF-May2021/VASP-%d/CONTCAR' % i, 'mini6.data-part2', 'newpart2')
            os.system('cat mini6.data-part1 newpart2 mini6.data-part3 > paa-%d.data' %i)
            generate_lammps_input_bin('/share/workspace/zhaolingci/task-BASF-May2021/test-fitting/paa-%d.data' % i, 'bin-%d.data' % i, params)
            generate_lammps_input_in('rut-paa.in', 'paa-%d.in' % i, 'bin-%d.data' % i)
            run_lammps('paa-%d.in' % i, 'binary')
            energy = get_lammps_energy('binary') - get_lammps_energy('slab') - mol_paa
            E_lammps.append(energy)
            F_lammps.append(get_lammps_force('forces'))
        op.write(' E_MSE:   ')
        op.write(str(mean_squared_error(E_target, E_lammps)))
        op.write(' E_R_square:   ')
        op.write(str(r2_score(E_target, E_lammps)))
        op.write(' lmp_ads_ene:   ')
        op.write(str(E_lammps))
        op.write(' params:   ')
        op.write(str(params)+ '\n')
        op.write('#########'+'\n')
        op.write(' F_MSE:   ')
        op.write(str(mean_squared_error(F_target, F_lammps)))
        op.write(' lmp_ads_force:   ')
        op.write(str(F_lammps))
        op.write(' params:   ')
        op.write(str(params)+ '\n')
        op.write('#########'+'\n')
        #print(F_lammps)
        return mean_squared_error(E_target, E_lammps)
        #return -r2_score(E_target, E_lammps)
        #return mean_squared_error(F_target, F_lammps) + mean_squared_error(E_target, E_lammps)
        #E_lammps_scale = [ j / 1.0 for j in E_lammps]
        #return mean_squared_error(F_target, F_lammps) + mean_squared_error(E_target_scale, E_lammps_scale)

    SPACE = {
        #'sigma_1': 2.75,
        #'eps_1': 0.24,
        #'sigma_2': 3.25,
        #'eps_2': 0.12,
        #'sigma_3': 2.55,
        #'eps_3': 0.016,
        #'sigma_4': 3.95,
        #'eps_4': 0.028,
        'sigma_1': hp.quniform('sigma_1', low=2.75, high=3.5, q=0.05),
        'eps_1': hp.quniform('eps_1', low=0.12, high=0.25, q=0.01),
        'sigma_2': hp.quniform('sigma_2', low=2.75, high=3.5, q=0.05),
        'eps_2': hp.quniform('eps_2', low=0.04, high=0.12, q=0.01),
        'sigma_3': hp.quniform('sigma_3', low=2.1, high=3.0, q=0.05),
        'eps_3': hp.quniform('eps_3', low=0.01, high=0.03, q=0.002),
        'sigma_4': hp.quniform('sigma_4', low=2.7, high=4.0, q=0.05),
        'eps_4': hp.quniform('eps_4', low=0.01, high=0.03, q=0.002),
        #'chg': hp.quniform('chg', low=1.0, high=1.5, q=0.02)
        'chg': 1.32
    }
    seed = 6
    best = fmin(objective, SPACE, algo=tpe.suggest, max_evals=2,
         rstate=np.random.RandomState(seed))

    print(best)
    print(E_target)
    #print(F_target)
    op.close()

if __name__ == '__main__':
    main()

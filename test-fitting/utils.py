#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from hyperopt import fmin, hp, tpe
from typing import Dict, Union, List
from subprocess import Popen, PIPE
import re
from lammps import PyLammps
from ase.io import read as readvasp

def get_qm_energy(filename: str):
    __Emol = -1005.93
    #__Emol = -1011.67
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line.startswith('  energy  without entropy'):
                value = line.strip().split()[6]
                Eqm = float(value) - __Emol
    energy = Eqm
    return energy


def generate_lammps_input_bin(lammps_in: str, lammps_out: str,
                          params: Dict[str, float]):
    with open(lammps_in, "r") as f1, open(lammps_out, "w") as f2:
        for line in f1:
            if line.startswith('           7      0.1700      3.1199'):
                line = re.sub('0.1700      3.1199','%.4f      %.4f' %(params['eps_1'], params['sigma_1']), line)
            if line.startswith('           9      0.0880      2.8812'):
                line = re.sub('0.0880      2.8812','%.4f      %.4f' %(params['eps_2'], params['sigma_2']), line)
            if line.startswith('          10      0.0170      2.8286'):
                line = re.sub('0.0170      2.8286','%.4f      %.4f' %(params['eps_3'], params['sigma_3']), line)
            if line.startswith('          11      0.0170      2.8286'):
                line = re.sub('0.0170      2.8286','%.4f      %.4f' %(params['eps_4'], params['sigma_4']), line)
            f2.write(line)

def generate_lammps_input_slab(lammps_in: str, lammps_out: str,
                          params: Dict[str, float]):
    with open(lammps_in, "r") as f1, open(lammps_out, "w") as f2:
        for line in f1:
            if line.startswith('           1      0.1700      3.1199'):
                line = re.sub('0.1700      3.1199','%.4f      %.4f' %(params['eps_1'], params['sigma_1']), line)
            if line.startswith('           2      0.0880      2.8812'):
                line = re.sub('0.0880      2.8812','%.4f      %.4f' %(params['eps_2'], params['sigma_2']), line)
            if line.startswith('           3      0.0170      2.8286'):
                line = re.sub('0.0170      2.8286','%.4f      %.4f' %(params['eps_3'], params['sigma_3']), line)
            if line.startswith('           4      0.0170      2.8286'):
                line = re.sub('0.0170      2.8286','%.4f      %.4f' %(params['eps_4'], params['sigma_4']), line)
            f2.write(line)



def run_lammps(lammps_in: str, output: str):
    Lbin = PyLammps(cmdargs=["-l", output])
    Lbin.file(lammps_in)


def get_lammps_energy(lammps_log: str):
    with open(lammps_log, 'r') as files:
        results = []
        line = files.readline()
        while line:
            results.append(line)
            if line.startswith('Loop time of'):
                #value = results[-2].split()[3]
                value = results[-3].split()[3]
            line = files.readline()
    return float(value)
#    with open(lammps_log, 'r') as f:
#        line = f.readline()
#        while line:
#            if line.startswith('  Energy initial,'):
#                line = f.readline()
#                value = line.strip().split()[2]
#            line = f.readline()
#    return float(value)


def run_command(cmd):
    sp = Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = sp.communicate()

def generate_lammps_input_in(infile: str, output: str, datafile: str):
    with open(infile, 'r') as f, open(output, 'w') as o:
        for line in f:
            if line.startswith('read_data'):
                line = 'read_data' + "  " + datafile + '\n'
            o.write(line)

def get_lammps_bond(lammps_log: str):
    with open(lammps_log, 'r') as files:
        results = []
        line = files.readline()
        while line:
            results.append(line)
            if line.startswith('Loop time of'):
                value = results[-2].split()[6]
            line = files.readline()
    return float(value)
#    with open(lammps_log, 'r') as f:
#        line = f.readline()
#        while line:
#            if line.startswith('Step Temp'):
#                line = f.readline()
#                value = line.strip().split()[6]
#            line = f.readline()
#    return float(value)

def get_qm_bond(filename: str):
#    a = readvasp('/lustre/home/acct-nishsun/nishsun/trash/old/workspace/zhaolingci/Parameter/ruitle/sample-PAA-fft/1/CONTCAR', format='vasp')
    a = readvasp(filename, format='vasp')
    TiO = a.get_distance(26, 109, mic=True)
    OO = a.get_distance(77, 108, mic=True)
    return TiO

def get_qm_force(outcar: str):
    f = [[0.0]*3 for i in range(1)]
    l = []
    with open(outcar, 'r') as files:
        results = []
        line = files.readline()
        while line:
            results.append(line)
            if line.startswith('    total drift:'):
                for i in range(0,1):
                    f[i][0] = float(results[-13 + i].split()[3])*23.06
                    f[i][1] = float(results[-13 + i].split()[4])*23.06
                    f[i][2] = float(results[-13 + i].split()[5])*23.06
            line = files.readline()
    for i in range(len(f)):
        for j in range(len(f[i])):
            l.append(f[i][j])
    return l


def get_lammps_force(lammps_log: str):
    f = [[0.0]*3 for i in range(1)]
    l = []
    with open(lammps_log, 'r') as files:
        results = []
        line = files.readline()
        while line:
            results.append(line)
            line = files.readline()
             
        for i in range(0,1):
            f[i][0] = float(results[-11 + i].split()[5])
            f[i][1] = float(results[-11 + i].split()[6])
            f[i][2] = float(results[-11 + i].split()[7])
    for i in range(len(f)):
        for j in range(len(f[i])):
            l.append(f[i][j])
    return l

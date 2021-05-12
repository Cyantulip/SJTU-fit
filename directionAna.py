#!/usr/bin/env python
# coding: utf-8



import numpy as np

import MDAnalysis as mda
import sys

import matplotlib.pyplot as plt
import argparse

class trajAna:

    def __init__(self, gro, trr, res='', donor='', acceptor=''):
        self.u = mda.Universe(gro, trr)

        self.donor = [int(i)-1 for i in donor.split(',')]   #list of donor atoms
        self.acceptor = [int(i)-1 for i in acceptor.split(',')]   #list of acceptor atoms
        self.all_res = self.u.select_atoms('resname ' + res)
        print('Donor atoms are:')
        print(self.all_res.residues[0].atoms[self.donor])
        print('Acceptor atoms are:')
        print(self.all_res.residues[0].atoms[self.acceptor])
        if len(self.all_res.residues) > 0:
            print('{:d} {:s} detected'.format(len(self.all_res.residues),res))
        else:
            print('Error!!! no residue named {:s} in the system'.format(res))
            sys.exit()



    def unit_vector(self, vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

    def angle_between(self, v1, v2):
        """ Returns the angle in radians between vectors 'v1' and 'v2'::"""
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def res_angle(self, residue):
        """calculate angle betwenn residue tmd(defined by donor and acceptor) and z axis"""
        tdm = residue.atoms[self.acceptor].centroid() - residue.atoms[self.donor].centroid()
        tdm = np.array(tdm)
        znorm = np.array([0,0,1])
        angle = self.angle_between(tdm, znorm)
        angle =  np.rad2deg(angle)
        length = np.linalg.norm(tdm)
        if angle > 90:
            angle = 180-angle
        return angle,length

    def angle_pos(self, res):
        """collect angle and pos traj of one residue"""
        allangles = []
        center_pos = []
        traj_time = []
        alllength = []
        for ts in self.u.trajectory:
            a,l = self.res_angle(res)
            alllength.append(l)
            allangles.append(a)
            traj_time.append(self.u.trajectory.time)
            center_pos.append(res.centroid())
        tt = np.array(traj_time)
        aa = np.array(allangles)
        al = np.array(alllength)
        cp = np.array(center_pos)
        return (tt,aa,al,cp)

    def all_angles(self):
        angles = []
        lengths = []
        for i in list(self.all_res.residues):
            print(i)
            res = i.atoms
            tt,aa,al,cp = self.angle_pos(res)
            angles.append(aa)
            lengths.append(al)
            #ax.plot(tt,aa,'r-',lw=2,label='angle')
        #ax.set_xlabel("time (ps)")
        #ax.set_ylabel(r"angle")
        self.angles = np.mean(np.array(angles),axis=1)
        #print(np.mean(np.array(lengths),axis=1))
        for a in self.angles:
            print(a)
        #print(np.std(np.array(angles),axis=1))

# u = mda.Universe('MCN84-PDP-350K.gro','MCN84-PDP-350K.trr')




# def unit_vector(vector):
#     """ Returns the unit vector of the vector.  """
#     return vector / np.linalg.norm(vector)

# def angle_between(v1, v2):
#     """ Returns the angle in radians between vectors 'v1' and 'v2'::"""
#     v1_u = unit_vector(v1)
#     v2_u = unit_vector(v2)
#     return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


# def res_angle(residue):
#     tdm = residue.atoms[acceptor].centroid() - residue.atoms[donor].centroid()
#     tdm = np.array(tdm)
#     znorm = np.array([0,0,1])
#     angle = angle_between(tdm, znorm)
#     angle =  np.rad2deg(angle)
#     length = np.linalg.norm(tdm)
#     if angle > 90:
#         angle = 180-angle
#     return angle,length

# NDM1 = u.select_atoms('resname PDP')
# acceptor = [28,27,14] #PDP
# donor = [22, 54, 55] #PDP
# #acceptor = [71, 72, 4] #NDM
# #donor = [0, 28, 29] #NDM

# def angle_pos(u, res):
#     allangles = []
#     center_pos = []
#     traj_time = []
#     alllength = []
#     for ts in u.trajectory:
#         a,l = res_angle(res)
#         alllength.append(l)
#         allangles.append(a)
#         traj_time.append(u.trajectory.time)
#         center_pos.append(res.centroid())
#     tt = np.array(traj_time)
#     aa = np.array(allangles)
#     al = np.array(alllength)
#     cp = np.array(center_pos)
#     return (tt,aa,al,cp)

# ax = plt.subplot(111)
# angles = []
# lengths = []
# for i in list(NDM1.residues):
#     #resid = 257+i*20
#     #NDM =  u.select_atoms('resid '+str(resid))
#     NDM = i.atoms
#     tt,aa,al,cp = angle_pos(u,NDM)
#     angles.append(aa)
#     lengths.append(al)
#     ax.plot(tt,aa,'r-',lw=2,label='angle')
# ax.set_xlabel("time (ps)")
# ax.set_ylabel(r"angle")
# print(np.mean(np.array(lengths),axis=1))
# print(np.mean(np.array(angles),axis=1))
# print(np.mean(np.array(angles)))
# print(np.std(np.array(angles),axis=1))
# print(np.std(np.array(angles)))

parser=argparse.ArgumentParser(description='Analysis relative direction of a molecule. Gromacs trr and gro are needed.')
parser.add_argument('-m', '--molecule', help='Set the resname of the molecule to measure the direction')
parser.add_argument('-d', '--dindex', help='Set the several atom index (start from 1) to define donor center,. Seperate multiple index by comma.')
parser.add_argument('-a', '--aindex', help='Set the several atom index (start from 1) to define acceptor center. Seperate multiple index by comma.')
parser.add_argument('inputfile', nargs='+', help='The input structures are gro and trr')
args = parser.parse_args()
gro_file = args.inputfile[0]
trr_file = args.inputfile[1]
ta = trajAna(args.inputfile[0], args.inputfile[1],
             res=args.molecule, donor=args.dindex, acceptor=args.aindex)
ta.all_angles()
print('Average angle is: {:.6f}'.format(np.mean(ta.angles)))
print('Std.dev is: {:.6f}'.format(np.std(ta.angles)))

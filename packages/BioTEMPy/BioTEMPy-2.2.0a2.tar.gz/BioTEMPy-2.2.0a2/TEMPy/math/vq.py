# =============================================================================
#     This file is part of TEMPy.
#
#     TEMPy is a software designed to help the user in the manipulation
#     and analyses of macromolecular assemblies using 3D electron microscopy
#     maps.
#
#     Copyright 2010-2014 TEMPy Inventors and Birkbeck College University of
#     London.
#     The TEMPy Inventors are: Maya Topf, Daven Vasishtan,
#     Arun Prasad Pandurangan, Irene Farabella, Agnel-Praveen Joseph,
#     Harpal Sahota
#
#     TEMPy is available under Public Licence.
#
#     Please cite your use of TEMPy in published work:
#
#     Vasishtan D, Topf M. (2011) J Struct Biol 174:333-343. Scoring functions
#     for cryoEM density fitting.
#     Pandurangan AP, Vasishtan D, Topf M. (2015) Structure 23:2365-2376.
#     GAMMA-TEMPy: Simultaneous fitting of components in 3D-EM Maps of their
#     assembly using genetic algorithm.
# =============================================================================

import numpy as np

from TEMPy.math.vector import Vector
# from TEMPy.math.vector import *


def VQ(D, n, epochs, alpha0=0.5, lam0=False):
    """Clusters a set of vectors (D) into a number (n) of codebook vectors"""
    if not lam0:
        lam0 = n / 2.
    dlen, dim = D.shape
    neurons = (np.random.rand(n, dim - 1) - 0.5) * 0.2
    train_len = epochs * dlen
    den_sum = sum(D[:, 3])
    den_culm = D[:, 3].cumsum()
    for i in range(train_len):
        den_rand = den_sum * np.random.rand()
        nz_min_index = np.nonzero(den_rand < den_culm)[0][0]
        x = D[nz_min_index, :3].astype(int)
        known = ~np.isnan(x)
        X = np.repeat([x], n, axis=0)
        X = np.array(X[:, known], dtype='i')

        Dx = np.array(neurons[:, known] - X)
        ranking = np.argsort(np.power(Dx, 2) @ known)

        lam = lam0 * (0.01 / lam0) ** (i / float(train_len))
        h = np.exp(-ranking / lam)
        H = np.repeat([h], len(known), axis=0).T
        alpha = alpha0 * (0.005 / alpha0) ** (i / float(train_len))
        neurons += (alpha * H) * (X - neurons[:, known])
    return [Vector(neuron[0], neuron[1], neuron[2]) for neuron in neurons]


def map_points(emmap, threshold):
    emvec = np.nonzero(emmap.fullMap > threshold)
    apix = emmap.apix
    x_o = emmap.x_origin()
    y_o = emmap.y_origin()
    z_o = emmap.z_origin()
    emv = []
    for v in range(len(emvec[0])):
        x = emvec[2][v] * apix[0] + x_o
        y = emvec[1][v] * apix[1] + y_o
        z = emvec[0][v] * apix[2] + z_o
        dens = emmap[emvec[0][v], emvec[1][v], emvec[2][v]]
        emv.append([x, y, z, dens])
    return np.array(emv)


def write_to_pdb(vq, output_file=None):
    f = open(output_file+'_vq.pdb', 'w')
    record_name = 'ATOM'
    serial = 1
    atom_name = 'CA'
    alt_loc = ' '
    chain = 'A'
    res_no = 1
    res = 'GLY'
    icode = ''
    occ = 1.0
    temp_fac = 1.0
    elem = 'C'
    charge = ''
    for v in vq:
        line = ''
        line += record_name.ljust(6)
        line += str(serial).rjust(5) + ' '
        line += atom_name.center(4)
        line += alt_loc.ljust(1)
        line += res.ljust(3) + ' '
        line += chain.ljust(1)
        line += str(res_no).rjust(4)
        line += str(icode).ljust(1) + '   '
        x = '%.3f' % v.x
        y = '%.3f' % v.y
        z = '%.3f' % v.z
        line += x.rjust(8)
        line += y.rjust(8)
        line += z.rjust(8)
        occ = '%.2f' % float(occ)
        temp_fac = '%.2f' % float(temp_fac)
        line += occ.rjust(6)
        line += temp_fac.rjust(6) + '          '
        line += elem.strip().rjust(2)
        line += charge.strip().ljust(2)
        line = line + '\n'
        f.write(line)
        serial += 1
        res_no += 1
    f.close()


def get_VQ_points(
        emmap,
        threshold,
        noOfPoints,
        epochs,
        output_file=None,
        lap_fil=True,
):
    """
       emmap :
           Map (to be clustered) instance.
       threshold :
           voxels with density above this value are used in the VQ run.
       noOfPoints :
           num of VQ points to output.
       epochs :
           num of iterations to run the algorithm
       output_file :
           file to output to. In PDB format
       lap_fil :
           True if you want to Laplacian filter the map first, False
           otherwise. Note that filtering the map will change the density
           values of the map, which is relevant for the threshold
           parameter.
    """
    if lap_fil:
        emmap = emmap.laplace_filtered()
        emmap = emmap.normalise()
    D = map_points(emmap, threshold)
    vq = VQ(D, noOfPoints, epochs)
    if output_file:
        write_to_pdb(vq, output_file)
    return vq

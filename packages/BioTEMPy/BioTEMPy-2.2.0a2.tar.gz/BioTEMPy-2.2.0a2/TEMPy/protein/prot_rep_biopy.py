# =============================================================================
#     This file is part of TEMPy.
#
#     TEMPy is a software designed to help the user in the manipulation
#     and analyses of macromolecular assemblies using 3D electron microscopy
#     maps.
#
#     Copyright  2015 Birkbeck College University of London.
#
#     Authors: Maya Topf, Daven Vasishtan, Arun Prasad Pandurangan,
#     Irene Farabella, Agnel-Praveen Joseph, Harpal Sahota
#
#     This software is made available under GPL V3 license
#     http://www.gnu.org/licenses/gpl-3.0.html
#
#
#     Please cite your use of TEMPy in published work:
#
#     Farabella, I., Vasishtan, D., Joseph, A.P., Pandurangan, A.P., Sahota, H.
#     & Topf, M. (2015). J. Appl. Cryst. 48.
#
# =============================================================================

import copy
import math
import random
import sys
import collections

import numpy as np
import gemmi

from TEMPy.protein.mmcif import mmcif_writer
from TEMPy.math.quaternion import Quaternion
import TEMPy.math.vector as Vector


# Useful global constants
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz"
ATOMIC_MASSES = {"H": 1, "C": 12, "N": 14, "O": 16, "S": 32}
# Taken from http://www.ccdc.cam.ac.uk/products/csd/radii/table.php4
VDW_RADII = {
    "H": 1.09,
    "C": 1.7,
    "N": 1.55,
    "O": 1.52,
    "S": 1.8,
    "P": 1.8,
    "Cl": 1.75,
    "CL": 1.75,
    "Cu": 1.4,
    "CU": 1.4,
}
SEQUENCE_CONSTS = {
    "GLY": "G",
    "ALA": "A",
    "VAL": "V",
    "LEU": "L",
    "ILE": "I",
    "MET": "M",
    "PHE": "F",
    "TRP": "W",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "CYS": "C",
    "TYR": "Y",
    "ASN": "N",
    "GLN": "Q",
    "ASP": "D",
    "GLU": "E",
    "LYS": "K",
    "ARG": "R",
    "HIS": "H",
}
ROOT_2_PI = (2 * math.pi) ** 0.5
AA_MASS = {
    "A": 71.0788,
    "R": 156.1875,
    "N": 114.1038,
    "D": 115.0886,
    "C": 103.1388,
    "E": 129.1155,
    "Q": 128.1307,
    "G": 57.0519,
    "H": 137.1411,
    "I": 113.1594,
    "L": 113.1594,
    "K": 128.1741,
    "M": 131.1926,
    "F": 147.1766,
    "P": 97.1167,
    "S": 87.0782,
    "T": 101.1051,
    "W": 186.2132,
    "Y": 163.1760,
    "V": 99.1326,
}


class Atom:
    """
    A generic atomic class.  Subclass should ensure desired fields are set.
    """

    def __init__(
        self,
        atom_name,
        coords,
        record_name="ATOM",
        serial=None,
        temp_factor=None,
        alt_loc=None,
        icode="",
        charge="",
        element="",
        occ=None,
        res=None,
        model=None,
        chain=None,
        res_no=None,
    ):
        # Set atomic information
        self.atom_name = atom_name
        self.mass = ATOMIC_MASSES.get(atom_name[0], 1.0)
        self.vdw = VDW_RADII.get(atom_name[0], 1.7)
        self.elem = element
        self.charge = charge
        self.temp_fac = temp_factor

        self.alt_loc = alt_loc
        self.icode = icode
        self.occ = occ
        self.serial = serial

        # Set atomic coordinates
        x, y, z = coords
        self.init_x = self.x = float(x)
        self.init_y = self.y = float(y)
        self.init_z = self.z = float(z)

        # Set topological information
        self.res = res
        self.res_no = res_no
        self.chain = chain
        self.model = model

        self.record_name = record_name

    def __repr__(self):
        return (
            f"({self.get_res()} {self.res_no} {self.chain}: "
            + f"{self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
        )

    def copy(self):
        """
        Return:
            Copy of the Atom instance.
        """
        return copy.deepcopy(self)

    def get_mass(self):
        """
        Return:
            Atom mass.
        """
        return self.mass

    def distance_from_init_position(self):
        """
        Return:
            Distance from initial position.
        """
        return (
            (self.x - self.init_x) ** 2
            + (self.y - self.init_y) ** 2
            + (self.z - self.init_z) ** 2
        ) ** 0.5

    def distance_from_atom(self, atom):
        """
        Return:
            Distance from another atom.
        """
        return (
            (self.x - atom.x) ** 2 + (self.y - atom.y) ** 2 + (self.z - atom.z) ** 2
        ) ** 0.5

    def reset_position(self):
        """
        Translate atom back in its initial position.

        Return:
            initial position co-ordinates of atom.
        """
        self.x = self.init_x
        self.y = self.init_y
        self.z = self.init_z

    def change_init_position(self):
        """
        Change initial position co-ordinates of atom to current position.

        Return:
            new initial position co-ordinates of atom.
        """
        self.init_x = self.x
        self.init_y = self.y
        self.init_z = self.z

    def translate(self, x, y, z):
        """
        Translate the atom.

        Arguments:
            *x, y, z*
                distance in Angstroms in respective directions to move atom.

        Return:
            Translate atom object.
        """
        self.x += x
        self.y += y
        self.z += z

    def map_grid_position(self, densMap, index=True):
        """
        Arguments:
            *densMap*
                EM map object consisting the 3D grid of density values.
            *index*
                Boolean to return co-ordinates of grid as integer index.
                If false co-ordinates are returned as floats.
                Default: True

        Return:
              The co-ordinates and density value of the grid point in a density
              map closest to this atom.
              Return 0 if atom is outside of map.
        """
        x_origin = densMap.x_origin()
        y_origin = densMap.y_origin()
        z_origin = densMap.z_origin()
        apix = densMap.apix
        x_size = densMap.x_size()
        y_size = densMap.y_size()
        z_size = densMap.z_size()
        if index:
            x_pos = int(round((self.get_x() - x_origin) / apix[0], 0))
            y_pos = int(round((self.get_y() - y_origin) / apix[1], 0))
            z_pos = int(round((self.get_z() - z_origin) / apix[2], 0))
        else:
            x_pos = (self.get_x() - x_origin) / apix[0]
            y_pos = (self.get_y() - y_origin) / apix[1]
            z_pos = (self.get_z() - z_origin) / apix[2]
        if (x_size > x_pos >= 0) and (y_size > y_pos >= 0) and (z_size > z_pos >= 0):
            return x_pos, y_pos, z_pos, self.mass
        else:
            return 0

    def matrix_transform(self, rot_mat):
        """
        Transform atom using a 3x3 matrix

        Arguments:
            *rot_mat*
                a 3x3 matrix instance.

        Return:
            Transformed position of atom object
        """
        atom_mat = np.array([self.x, self.y, self.z])
        new_pos = rot_mat @ atom_mat
        self.x = float(new_pos[0])
        self.y = float(new_pos[1])
        self.z = float(new_pos[2])

    def get_pos_vector(self):
        """
        Return:
            Vector instance containing 3D coordinates of the atom.
        """
        return Vector.Vector(self.x, self.y, self.z)

    def get_pos_mass(self):
        """
        Return:
            An array containing Vector instances containing 3D coordinates of
            the atom and and its corresponding mass.
        """
        return [self.x, self.y, self.z, self.mass]

    def get_x(self):
        """
        Return:
            x co-ordinate of atom.
        """
        return float(self.x)

    def get_y(self):
        """
        Return:
            y co-ordinate of atom.
        """
        return float(self.y)

    def get_z(self):
        """
        Return:
            z co-ordinate of atom.
        """
        return float(self.z)

    def set_x(self, mod):
        """
        Change the x co-ordinate of an atom based on the argument.

        Arguments:
            *mod*
                float value
        Return:
            new x co-ordinate
        """
        self.x = mod

    def set_y(self, mod):
        """
        Change the y co-ordinate of an atom based on the argument.

        Arguments:
            *mod*
                float value
        Return:
            new y co-ordinate
        """
        self.y = mod

    def set_z(self, mod):
        """

        Change the z co-ordinate of an atom based on the argument.

        Arguments:
            *mod*
                float value
        Return:
            new x co-ordinate
        """
        self.z = mod

    def get_name(self):
        """
        atom name (ie. 'CA' or 'O')

        Return:
            atom name.
        """
        return self.atom_name

    def get_res(self):
        """

        Return:
            three letter residue code corresponding to the atom (i.e 'ARG').
        """
        return self.res

    def get_res_no(self):
        """
        Return:
            residue number corresponding to the atom.
        """
        return self.res_no

    def get_id_no(self):
        """
        Return:
            string of atom serial number.
        """
        return self.serial

    def _writeTerm(self):
        line = ""
        line += "TER".ljust(6)
        line += str(self.serial + 1).rjust(5) + " "
        line += "".center(4)
        line += self.alt_loc.ljust(1)
        line += self.res.ljust(4)
        line += self.chain.ljust(1)
        line += str(self.res_no).rjust(4)
        return line

    def write_to_PDB(self):
        """
        Writes a PDB ATOM record based in the atom attributes to a file.
        """
        line = ""
        line += self.record_name.ljust(6)
        line += str(self.serial).rjust(5) + " "
        line += self.atom_name.center(4)
        if self.alt_loc == ".":
            line += " "
        else:
            line += self.alt_loc.ljust(1)
        line += self.res.ljust(3) + " "
        line += self.chain.ljust(1)
        line += str(self.res_no).rjust(4)
        if self.icode == "?":
            line += " " + "   "
        else:
            line += str(self.icode).ljust(1) + "   "
        x = "%.3f" % self.x
        y = "%.3f" % self.y
        z = "%.3f" % self.z
        line += x.rjust(8)
        line += y.rjust(8)
        line += z.rjust(8)
        occ = "%.2f" % float(self.occ)
        temp_fac = "%.2f" % float(self.temp_fac)
        line += occ.rjust(6)
        line += temp_fac.rjust(6) + "          "
        line += self.elem.strip().rjust(2)
        line += str(self.charge).strip().rjust(2)
        return line + "\n"

    def rotate_by_quaternion(self, q_param):
        l = [0.0, self.x, self.y, self.z]  # noqa:E741
        atom_quat = Quaternion(l)
        q = Quaternion(q_param)
        q_conjugate = q.conjugate(q)
        resultant_quat = q.multiply_3(atom_quat, q_conjugate, q)
        w, x, y, z = resultant_quat.param
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    # added by Scott(SWH)
    def gridpoints_around_atom(self, densmap, radius=0.0, dx=0, dy=0, dz=0):
        """
        Get the x,y,z box boundaries of a set radius around an atom
        If radius is set, dx, dy, and dz will be calculated using radius,
        if not dx, dy, and dz given will be used.
        Arguments:
            *densmap*
                Map instance containing the grid
            *radius*
                Cutoff radius around atom (Angstroms)
            *dx*
                gridpoint distance along x (in integers)
            *dy*
                gridpoint distance along y (in integers)
            *dz*
                gridpoint distance along z (in integers)
        Return:
            Minimum and maximum grid index along each direction of x, y, z
            e.g. [minx, maxx, miny, maxy, minz, maxz]
        """
        xyz = self.map_grid_position(densmap)
        if not isinstance(xyz, int):
            x, y, z = xyz[:3]
        else:
            raise ValueError("Atom map grid position is out of box boundary.")
        if radius > 0.0:
            dx = int(np.ceil(radius / densmap.apix[0]))
            dy = int(np.ceil(radius / densmap.apix[1]))
            dz = int(np.ceil(radius / densmap.apix[2]))
        if dx == 0 and dy == 0 and dz == 0:
            print("Gridpoint distances are 0 along dx, dy and dz.")
            print("Please set the radius or dx, dy, dz to more than 0.")
            return [0, 0, 0, 0, 0, 0]
        minx = x - dx
        miny = y - dy
        minz = z - dz
        maxx = x + dx
        maxy = y + dy
        maxz = z + dz
        minx = min(max(minx, 0), densmap.x_size() - 1)
        miny = min(max(miny, 0), densmap.y_size() - 1)
        minz = min(max(minz, 0), densmap.z_size() - 1)
        maxx = max(min(maxx, densmap.x_size()), 0)
        maxy = max(min(maxy, densmap.y_size()), 0)
        maxz = max(min(maxz, densmap.z_size()), 0)

        return [minx, maxx, miny, maxy, minz, maxz]


class gemmiAtom(Atom):
    """
    Class representing an atom as read from a PDB/mmCIF file using gemmi

    gemmi docs here: https://gemmi.readthedocs.io/
    """

    def __init__(
        self,
        chain,
        entity,
        residue,
        atom,
    ):

        # "fixing" some gemmi flags to be writable
        if residue.het_flag == "H":
            record_name = "HETATM"
        else:
            record_name = "ATOM"
        if atom.has_altloc():
            pass
        else:
            atom.altloc = "."
        if residue.seqid.icode == " ":
            icode = "?"
        else:
            icode = residue.seqid.icode

        super().__init__(
            atom.name,
            (atom.pos.x, atom.pos.y, atom.pos.z),
            record_name=record_name,
            serial=atom.serial,
            temp_factor=atom.b_iso,
            alt_loc=atom.altloc,
            icode=icode,
            charge=atom.charge,
            element=atom.element.name,
            occ=atom.occ,
            res=residue.name,
            model=entity.name,
            chain=chain.name,
            res_no=residue.seqid.num,
        )

        # grab some extra variables for writing cif files
        self.asym_id = residue.subchain
        self.model = entity.name
        self.seq_id = residue.label_seq
        self.res_flag = residue.flag
        self.entity_type = residue.entity_type
        self.segment = residue.segment
        self.calc_flag = atom.calc_flag
        self.atom_flag = atom.flag
        self.tls_group_id = atom.tls_group_id
        self.polymer_type = entity.polymer_type
        self.seqid_icode = residue.seqid.icode

    def get_atom_vals(self):
        """returns list ready for parsing by gemmi for file writing"""
        atom_block = [
            self.record_name,
            self.serial,
            self.elem,
            self.atom_name,
            self.alt_loc,
            self.res,
            self.asym_id,
            self.model,
            self.seq_id,
            self.icode,
            self.x,
            self.y,
            self.z,
            self.occ,
            self.temp_fac,
            self.charge,
            self.res_no,
            self.chain,
        ]
        return atom_block

    def get_str_atom_vals(self):
        """returns list ready for parsing by gemmi for file writing"""
        atom_block = [
            str(self.record_name),
            str(self.serial),
            str(self.elem),
            str(self.atom_name),
            str(self.alt_loc),
            str(self.res),
            str(self.asym_id),
            str(self.model),
            str(self.seq_id),
            str(self.icode),
            str(round(self.x, 3)),
            str(round(self.y, 3)),
            str(round(self.z, 3)),
            str(self.occ),
            "%.2f" % self.temp_fac,
            str(self.charge),
            str(self.res_no),
            str(self.chain),
        ]
        return atom_block

    def get_col_labels(self):
        """returns list ready for parsing by gemmi for file writing"""
        col_ids = [
            "group_PDB",
            "id",
            "type_symbol",
            "label_atom_id",
            "label_alt_id",
            "label_comp_id",
            "label_asym_id",
            "label_entity_id",
            "label_seq_id",
            "pdbx_PDB_ins_code",
            "Cartn_x",
            "Cartn_y",
            "Cartn_z",
            "occupancy",
            "B_iso_or_equiv",
            "pdbx_formal_charge",
            "auth_seq_id",
            "auth_asym_id",
        ]
        return col_ids

    def set_tempy_score(self, score_name, score_value):
        self.tempy_scores[score_name] = score_value

    def get_tempy_score(self, score_name):
        return self.tempy_score[score_name]


class BioPy_Structure:
    """
    A class representing a Structure object.
    """

    def __init__(self, atomList, filename="Unknown", header="", footer=""):
        """
        Initialise using a string of the relevant pdb file name or a numpy
        array of Atom objects.

        Arguments:
            *pdbFileOrList*
                String of pdb file name or array of Atom objects
        """
        self.header = header
        self.footer = footer
        self.filename = filename
        if type(atomList) == np.ndarray:
            self.atomList = atomList[:]
        if type(atomList) == list:
            self.atomList = np.array(atomList)
        self.CoM = self.calculate_centre_of_mass()
        self.initCoM = self.CoM.copy()

    def __getitem__(self, index):
        return self.atomList[index]

    def __len__(self):
        return len(self.atomList)

    def __repr__(self):
        if not self.filename == "Unknown":
            s = "Filename: " + self.filename + "\n"
        else:
            s = ""
        s += "No Of Atoms: " + str(len(self)) + "\n"
        s += "First Atom: " + str(self.atomList[0]) + "\n"
        s += "Last Atom: " + str(self.atomList[-1]) + "\n"
        return s

    def get_pdb_id(self):
        return self.pdb_id

    def write_to_PDB(self, filename, hetatom=False):
        """
        Write Structure instance to PDB file.

        Arguments:
            *filename*
                output filename.
        """
        self.footer = ""

        if filename[-4:] == ".pdb":
            g = open(filename, "w")
        else:
            g = open(filename + ".pdb", "w")
        header = """EXPDTA    MODEL GENERATE WITH TEMPY
REMARK    MODEL GENERATE WITH TEMPY
MODEL      1
"""
        g.write(header)
        structList = self.split_into_chains()
        hetatmlist = []
        chainlisttot = []
        last_prot_num = 0
        for chain in range(len(structList)):
            chainlist = []
            for x in structList[chain].atomList:
                if x.record_name == "HETATM":
                    hetatmlist.append(x.copy())
                else:
                    chainlist.append(x.copy())
            chainlisttot.append(BioPy_Structure(chainlist))
        for strchain in range(len(chainlisttot)):
            if strchain == 0:
                chainlisttot[strchain].renumber_atoms()
            else:
                start_num = chainlisttot[strchain - 1].atomList[-1].serial
                chainlisttot[strchain].renumber_atoms(start_num=start_num + 2)
            for x in chainlisttot[strchain].atomList:
                g.write(x.write_to_PDB())
                last_prot_num += 1
            line = chainlisttot[strchain].atomList[-1]._writeTerm() + "\n"
            g.write(line)
        if hetatom is True:
            hetstr = BioPy_Structure(hetatmlist)
            hetchain = hetstr.split_into_chains()
            for chain in range(len(hetchain)):
                if chain == 0:
                    hetchain[chain].renumber_atoms(start_num=last_prot_num + 2)
                else:
                    start_num = hetchain[chain - 1].atomList[-1].serial
                    hetchain[chain].renumber_atoms(start_num=start_num + 2)
                for xhet in hetchain[chain].atomList:
                    g.write(xhet.write_to_PDB())
                line = hetchain[chain].atomList[-1]._writeTerm() + "\n"
                g.write(line)
        lineend = ""
        lineend += "ENDMDL".ljust(6) + "\n"
        g.write(lineend)
        g.write(self.footer)
        g.close()

    def copy(self):
        """
        Return:
            Copy of Structure instance.
        """
        newAtomList = []
        for atom in self.atomList:
            newAtomList.append(atom.copy())
        return BioPy_Structure(newAtomList)

    def get_number_of_atoms(self):
        self.no_of_atoms = len(self)
        return self.no_of_atoms

    def get_model_atoms(self, model_ID):

        return [i for i in self.atomList if i.model == model_ID]

    def calculate_centre_of_mass(self):
        """
        Return:
            Center of mass of structure as a Vector instance.
        """
        x_CoM = 0.0
        y_CoM = 0.0
        z_CoM = 0.0
        massTotal = 0.0
        for atom in self.atomList:
            x = atom.get_x()
            y = atom.get_y()
            z = atom.get_z()
            m = atom.get_mass()
            x_CoM += x * m
            y_CoM += y * m
            z_CoM += z * m
            massTotal += m
        x_CoM /= massTotal
        y_CoM /= massTotal
        z_CoM /= massTotal
        return Vector.Vector(x_CoM, y_CoM, z_CoM)

    def translate(self, x, y, z):
        """
        Translate the structure.

        Arguments:
            *x, y, z*
                distance in Angstroms in respective directions to move
                structure.
        Return:
            Translated Structure instance
        """
        for atom in self.atomList:
            atom.translate(x, y, z)
        self.CoM = self.CoM.translate(x, y, z)

    def rotate_by_axis_angle(
        self,
        x,
        y,
        z,
        turn,
        x_trans=0,
        y_trans=0,
        z_trans=0,
        rad=False,
        com=False,
    ):
        """
        Rotate the Structure instance around its centre.

        Arguments:
            *turn*
                angle (in radians if rad == True, else in degrees) to rotate
                map.
            *x,y,z*
                axis to rotate about, ie. x,y,z =  0,0,1 rotates the structure
                round the xy-plane.
            *x_trans, y_trans, z_trans*
                extra translational movement if required.
            *com*
                centre of mass around which to rotate the structure. If False,
                rotates around centre of mass of structure.
        """
        mat = Vector.axis_angle_to_matrix(x, y, z, turn, rad)

        if not com:
            com = self.CoM.copy()

        newcom = com.matrix_transform(mat)
        offset = com - newcom
        self.matrix_transform(mat)
        self.translate(
            x_trans + offset.x,
            y_trans + offset.y,
            z_trans + offset.z,
        )

    def rotate_by_euler(
        self,
        x_turn,
        y_turn,
        z_turn,
        x_trans=0,
        y_trans=0,
        z_trans=0,
        rad=False,
        com=False,
    ):
        """
        Rotate this Structure instance around its centre.

        Arguments:
            *x_turn,y_turn,z_turn*
                Euler angles (in radians if rad == True, else in degrees) used
                to rotate structure, in order XYZ.
            *x_trans, y_trans, z_trans*
                extra translational movement if required.
            *com*
                centre of mass around which to rotate the structure. If False,
                rotates around centre of mass of structure.
        """
        mat = Vector.euler_to_matrix(x_turn, y_turn, z_turn, rad)

        if not com:
            com = self.CoM.copy()

        newcom = com.matrix_transform(mat)
        offset = com - newcom
        self.matrix_transform(mat)
        self.translate(x_trans + offset.x, y_trans + offset.y, z_trans + offset.z)

    def rotate_by_quaternion(self, q, com=False):
        if not com:
            com = self.CoM.copy()
        self.translate(-com.x, -com.y, -com.z)
        for atom in self.atomList:
            atom.rotate_by_quaternion(q)
        self.translate(com.x, com.y, com.z)

    def randomise_position(
        self, max_trans, max_rot, v_grain=30, rad=False, verbose=False
    ):
        """
        Randomise the position of the Structure instance using random rotations
        and translations.

        Arguments:
            *max_trans*
                Maximum translation permitted
            *max_rot*
                Maximum rotation permitted (in degree if rad=False)
            *v_grain*
                Graning Level for the generation of random vetors (default=30)
        Return:
            Transformed position of Structure object
        """
        t_v = Vector.random_vector(-v_grain, v_grain).unit()
        r_v = Vector.random_vector(-v_grain, v_grain).unit()

        if max_trans <= 0:
            t_dist = 0
        else:
            t_dist = random.randrange(max_trans)

        if max_rot <= 0:
            r_ang = 0
        else:
            r_ang = random.randrange(max_rot)
        t_v = t_v.times(t_dist)
        self.rotate_by_axis_angle(
            r_v.x, r_v.y, r_v.z, r_ang, t_v.x, t_v.y, t_v.z, rad=rad
        )
        if verbose:
            print(r_v.x, r_v.y, r_v.z, r_ang, t_v.x, t_v.y, t_v.z)
        return r_v.x, r_v.y, r_v.z, r_ang, t_v.x, t_v.y, t_v.z

    def matrix_transform(self, matrix):
        """
        Transform Structure using a 3x3 transformation matrix

        Arguments:
            *rot_mat*
                a 3x3 matrix instance.

        Return:
            Transformed position of Structure object
        """
        for atom in self.atomList:
            atom.matrix_transform(matrix)
        self.CoM = self.CoM.matrix_transform(matrix)

    def reorder_residues(self):
        """
        Order residues in atom list by residue number.
        (NOTE: Does not check for chain information - split by chain first).
        """
        self.atomList = list(self.atomList)
        self.atomList.sort(cmp=lambda x, y: int(x.res_no) - int(y.res_no))
        self.atomList = np.array(self.atomList)

    def get_residue_indexes(self):
        """Get the atom indexes for each residues from atomList in the
        structure

        Returns:
            residue_indexes: a dictionary containing the index positions
            for all atoms from each residue in the structure.
            Items have format: [list, of, atom, indexes, as, ints]
            Keys have format: (str(chain_label), int(residue_number))
        """

        # as of python 3.7 all dictionaries should preserve insertion order
        residue_indexes = dict()

        for n, atom in enumerate(self.atomList):
            try:
                residue_indexes[atom.chain, atom.res_no].append(n)
            except KeyError:
                residue_indexes[atom.chain, atom.res_no] = [n]

        return residue_indexes

    def number_of_residues(self):
        """Return the number of residues (and/or nucleotide bases) in the
        model"""
        prev = None
        num_residues = 0

        for atom in self.atomList:
            if (atom.res_no, atom.chain) == prev:
                continue
            else:
                prev = (atom.res_no, atom.chain)
                num_residues += 1

        return num_residues

    def renumber_residues(self, startRes=1, missingRes=[]):
        """
        Renumber the structure starting from startRes.
        Missing number list to add.

        Arguments:
            *startRes*
                Starting residue number for renumbering
            *missingRes*
                A list of missing residue numbers to add
        """
        resNo = startRes
        currentRes = self.atomList[0].res_no
        for x in self.atomList:
            if x.res_no == currentRes:
                x.res_no = resNo
            else:
                currentRes = x.res_no
                resNo += 1
                while resNo in missingRes:
                    resNo += 1
                x.res_no = resNo

    def renumber_atoms(self, start_num=1):
        """
        Renumber the atoms in the structure.
        After renumbering the starting atom number will be 1 unless start_num
        """
        for x in range(len(self.atomList)):
            if (x + 1) < 99999:
                self.atomList[x].serial = x + start_num
            else:
                self.atomList[x].serial = "*****"

    def regroup_chains(self):

        chain_indexes = self.get_atoms_in_chains()

        reordered_atoms = []
        for chain_id in chain_indexes.keys():
            for atom in self.atomList[chain_indexes[chain_id]]:
                reordered_atoms.append(atom)

        self.atomList = np.array(reordered_atoms)

    def get_atoms_in_chains(self):
        """
        TODO - reformat for BioPy_Structure
        """
        chains = collections.OrderedDict()

        for atom_no, atom in enumerate(self.atomList):
            try:
                chains[atom.chain].append(atom_no)
            except KeyError:
                chains[atom.chain] = [atom_no]

        return chains

    def iter_asym_id(self, asym_id):
        """
        Function to increase the chain "numbering" by one e.g. from D -> E or
        from HA -> IA.
        Uses the chr() and ord() functions to convert between int and ASCII str
        One should run rename_chains before to ensure all chain_ids are letters

        Input: capital letter from A -> Z
        Output: Next letter in alphabet e.g. from A -> B. For input Z, ouput is
                AA, for input ZZ output is AAA etc..
        """
        index = 0
        new_id = [i for i in asym_id]
        chain_int = ord(asym_id[0])

        if chain_int == 90:
            new_id[0] = "A"
            while True:
                index += 1
                try:
                    chain_int = ord(asym_id[index])
                except IndexError:
                    new_id.append("A")
                    break
                if chain_int == 90:
                    new_id[index] = "A"
                    continue
                else:
                    new_id[index] = chr(chain_int + 1)
                    break
        else:
            new_id[0] = chr(chain_int + 1)

        return "".join(new_id)

    def get_next_chain_id(self, chain_id, chain_list=False):
        """
        Renames chains based on mmCIF convention i.e. A -> B, Z -> 0 or g -> h
        See the ALPHABET list for standard sequence, however any string can be
        used for chain labelling.

        For structures with more than 62 chains, the labels are increased in
        length, i.e. z -> AA, zz -> AAA, AAA -> BBB

        Input: chain_id -> old chain id
        Output: new_chain_id
        """

        if not chain_list:
            chain_list = ALPHABET

        try:
            index = int(chain_list.index(chain_id[0]) + 1) + (
                (len(chain_id) - 1) * len(chain_list)
            )
        except ValueError:
            index = 0

        try:
            new_chain_label = chain_list[index]
        except IndexError:
            n = 1
            while index >= len(chain_list):
                n += 1
                index = index - len(chain_list)

            new_chain_label = chain_list[index] * n

        return new_chain_label

    def rename_chains(self, chain_list=False):
        """
        TODO - reformat for BioPy_Structure
        """
        if not chain_list:
            chain_list = ALPHABET
        else:
            noc = self.no_of_chains()
            if len(chain_list) != self.no_of_chains():
                print("No. of chains in structure = " + str(noc))
                print("Length of chain list = " + str(len(chain_list)))
                print("Chains not changed.")
                return

        ch = self.atomList[0].chain
        renum = 0
        for atom in self.atomList:
            if atom.chain == ch:
                atom.chain = chain_list[renum]
            else:
                renum += 1
                ch = atom.chain[:]
                atom.chain = chain_list[renum]

    def split_into_chains(self):
        """
        Split the structure into separate chains and returns the list of
        Structure instance for each chain.
        """
        structList = []
        currentChain = self.atomList[0].chain
        currentStruct = []
        for x in self.atomList:
            if x.chain == currentChain:
                currentStruct.append(x.copy())
            else:
                currentChain = x.chain
                structList.append(BioPy_Structure(currentStruct))
                currentStruct = [x.copy()]
        structList.append(BioPy_Structure(currentStruct))
        return structList

    def no_of_chains(self):
        """
        Return:
            the number of chains in the Structure object
        """
        a = self.split_into_chains()
        return len(a)

    def reset_position(self):
        """
        Translate structure back into initial position.
        """
        for x in self.atomList:
            x.reset_position()
        self.CoM = self.initCoM.copy()

    def change_init_position(self):
        """
        Change initial position of structure to current position.
        """
        for atom in self.atomList:
            atom.change_init_position()
        self.init_CoM = self.CoM.copy()

    def RMSD_from_init_position(self, CA=False):
        """
        Return RMSD of structure from initial position after translation.

        Arguments:
            *CA*
                True will consider only CA atoms.
                False will consider all atoms.
        Return:
            RMSD in angstrom
        """
        dists = []
        for x in self.atomList:
            if CA:
                if x.atom_name == "CA":
                    dists.append(x.distance_from_init_position())
            else:
                dists.append(x.distance_from_init_position())
        dists = np.array(dists)
        return dists.mean()

    def RMSD_from_same_structure(self, otherStruct, CA=False, write=True):
        """
        Return the RMSD between two structure instances.

        Arguments:
            *otherStruct*
                Structure instance to compare, containing the same number of
                atoms as the target instance.
            *CA*
                True will consider only CA atoms.
                False will consider all atoms.
        Return:
            RMSD in angstrom
        """
        dists = []
        for a in range(len(self.atomList)):
            if CA:
                if self.atomList[a].atom_name == "CA":
                    if otherStruct.atomList[a].atom_name == "CA":
                        dists.append(
                            self.atomList[a].distance_from_atom(otherStruct.atomList[a])
                        )
                        print(
                            self.atomList[a].atom_name,
                            otherStruct.atomList[a].atom_name,
                            self.atomList[a].res_no,
                            otherStruct.atomList[a].res_no,
                        )
                    else:
                        pass
            else:
                dists.append(
                    self.atomList[a].distance_from_atom(otherStruct.atomList[a])
                )
        dists = np.array(dists)
        return dists.mean()

    def get_vector_list(self):
        """
        Return:
            Array containing 3D Vector instances of positions of all atoms.
        """
        v = []
        for atom in self.atomList:
            v.append(atom.get_pos_vector())
        return np.array(v)

    def get_pos_mass_list(self):
        """
        Return:
            Array containing Vector instances of positions of all atoms and
            mass.
        """
        v = []
        for atom in self.atomList:
            v.append(atom.get_pos_mass())
        return np.array(v)

    def get_extreme_values(self):
        """
        Return:
            A 6-tuple containing the minimum and maximum of x, y and z
            co-ordinates of the structure.
            Given in order (min_x, max_x, min_y, max_y, min_z, max_z).
        """
        min_x = self.atomList[0].get_x()
        max_x = self.atomList[0].get_x()
        min_y = self.atomList[0].get_y()
        max_y = self.atomList[0].get_y()
        min_z = self.atomList[0].get_z()
        max_z = self.atomList[0].get_z()
        for atom in self.atomList[1:]:
            if atom.get_x() < min_x:
                min_x = atom.get_x()
            if atom.get_x() > max_x:
                max_x = atom.get_x()
            if atom.get_y() < min_y:
                min_y = atom.get_y()
            if atom.get_y() > max_y:
                max_y = atom.get_y()
            if atom.get_z() < min_z:
                min_z = atom.get_z()
            if atom.get_z() > max_z:
                max_z = atom.get_z()
        return min_x, max_x, min_y, max_y, min_z, max_z

    def get_atom_list(self):
        """
        Return:
            An array containing Atom instances of positions of all atoms as:
            [(RES 1 A: x,y,z), ... ,(RES2 1 A: x1,y1,z1)].
        """
        alist = []
        for x in self.atomList:
            alist.append(x.copy())
        return alist

    def find_same_atom(self, atom_index, otherStruct):
        """
        Find if an atom exists in the compared structure, based on atom index.

        Arguments:
            *atom_index*
                atom number
            *otherStruct*
                a structure object to compare

        Return:
            If a match is found, it returns the atom object; else it returns a
            string reporting the mismatch.
        """
        atom = self.atomList[atom_index]
        for x in otherStruct.atomList:
            if (
                x.res_no == atom.res_no
                and x.atom_name == atom.atom_name
                and atom.res == atom.res
                and x.chain == atom.chain
            ):
                return x
        return "No match of atom index %s in structure %s" % (
            atom_index,
            otherStruct,
        )

    def get_chain_list(self):
        """
        Return:
            A list of chain ID.
        """
        chain_list = []
        for x in self.atomList:
            if x.chain not in chain_list:
                chain_list.append(x.chain)
        return chain_list

    def get_chain(self, chainID):
        """
        Return:
            New Structure instance with only the requested chain.
        """
        newAtomList = []
        for x in self.atomList:
            if x.chain == chainID:
                newAtomList.append(x.copy())
        if len(newAtomList) != 0:
            return BioPy_Structure(newAtomList)
        else:
            print("Warning no chain %s found" % chainID)

    def get_dict_str(self):
        dict_ch = {}
        list_res = []
        currentChain = self.atomList[0].chain
        for x in self.atomList:
            if not x.chain == currentChain:
                dict_ch[currentChain] = list_res[:]
                currentChain = x.chain
                list_res = []
            cur_chain = x.chain
            list_res.append(x.get_res_no())
        if cur_chain not in dict_ch:
            dict_ch[cur_chain] = list_res[:]
        return dict_ch

    def get_selection(self, startRes, finishRes, chain=""):
        """
        Get a new Structure instance for the selected residues range without
        considering residues chain.

        Arguments:
            *startRes*
                Start residue number
            *finishRes*
                End residue number

        Return:
            New Structure instance
        """
        newAtomList = []
        for x in self.atomList:
            cur_chain = x.chain
            if chain:
                if not cur_chain == chain:
                    continue
            if x.get_res_no() >= int(startRes) and x.get_res_no() <= int(finishRes):
                newAtomList.append(x.copy())
        return BioPy_Structure(newAtomList)

    def break_into_segments(self, rigid_list, chain=""):
        """
        Return a list of Structure instance based on the rigid body list.

        Arguments:
            *rigid list*
                list of rigid body defined as:
                    [[riA,rfA],..,[riB,rfB]]

                where:
                    riA is the starting residues number of segment A.
                    rfA is the final residues number of segment A.
        Return:
            List of TEMPy Structure instance
        """
        structList = []
        for r in rigid_list:
            fstStruct = self.get_selection(r[0], r[1], chain)
            nxtStructs = []
            for x in range(2, len(r), 2):
                nxtStructs.append(self.get_selection(r[x], r[x + 1], chain))
            if len(nxtStructs) != 0:
                structList.append(fstStruct.combine_structures(nxtStructs))
            else:
                structList.append(fstStruct)
        if len(structList) == 0:
            print("Error: Residues not in PDB.")
            sys.exit()
        else:
            return structList

    def get_chain_ca(self, chainID):
        newAtomList = []
        for x in self.atomList:
            if x.chain == chainID and x.atom_name == "CA":
                newAtomList.append(x.copy())
        if len(newAtomList) != 0:
            return BioPy_Structure(newAtomList)
        else:
            print('Warning no chain %s found"%chainID')

    def get_rgyration(self):
        vc = self.calculate_centre_of_mass()
        num = 0.0
        den = 0.0
        for x in self.atomList:
            vx = x.get_pos_vector()
            dist = vx.dist(vc)
            num = num + x.get_mass() * (dist * dist)
            den = den + x.get_mass()
        rg = np.sqrt(num / den)
        return rg

    def get_atom_zyx_map_indexes(self, map):

        zyx_coordinates = []
        for atom in self.atomList:
            x = int(round((atom.x - map.origin[0]) / map.apix[0], 0))
            y = int(round((atom.y - map.origin[1]) / map.apix[1], 0))
            z = int(round((atom.z - map.origin[2]) / map.apix[2], 0))
            zyx_coordinates.append([z, y, x])

        return np.array(zyx_coordinates)

    def calculate_centroid(self):
        """
        Return centre of mass of structure as a Vector instance.
        """
        x_Total = 0.0
        y_Total = 0.0
        z_Total = 0.0
        natom = 0.0
        for atom in self.atomList:
            x = atom.get_x()
            y = atom.get_y()
            z = atom.get_z()
            x_Total += x
            y_Total += y
            z_Total += z
            natom += 1
            x_CoM = x_Total / natom
            y_CoM = y_Total / natom
            z_CoM = z_Total / natom
        return Vector.Vector(x_CoM, y_CoM, z_CoM)

    def combine_structures(self, structList):
        """
        Add a list of Structure instance to the existing structure.

        Arguments:
            *structList*
                list of Structure instance
        Return:
            New Structure Instance
        """
        atomList = self.atomList.copy()
        for s in structList:
            atomList = np.append(atomList, s.atomList)
        return BioPy_Structure(atomList)

    def combine_SSE_structures(self, structList):
        """
        Combine a list of Structure instance into one and return a new
        Structure instance.

        Arguments:
            *structList*
                list of Structure instance
        Return:
            New Structure Instance
        """
        atomList = []
        for s in structList:
            atomList = np.append(atomList, s.atomList)
        return BioPy_Structure(atomList)

    def get_selection_more_than(self, startRes):
        """
        Get a Structure instance comprising all residues with their residue
        numbers greater than startRes.

        Arguments:
            *startRes*
                a residue number

        Return:
            A Structure instance
        """
        newAtomList = []
        for x in self.atomList:
            if x.get_res_no() >= int(startRes):
                newAtomList.append(x.copy())
        return BioPy_Structure(newAtomList)

    def get_selection_less_than(self, endRes):
        """
        Get a Structure instance comprising all residues with their residue
        numbers less than endRes.

        Arguments:
            *endRes*
                a residue number

        Return:
            A Structure instance
        """
        newAtomList = []
        for x in self.atomList:
            if x.get_res_no() <= endRes:
                newAtomList.append(x.copy())
        return BioPy_Structure(newAtomList)

    def get_residue(self, resNo):
        """
        Get the residue corresponding to the residue number.

        Arguments:
            *resNo*
                Residues number
        Return:
            Returns a Residues instance.
        """
        return BioPy_Structure(
            [x.copy() for x in self.atomList if x.get_res_no() == int(resNo)]
        )

    def get_atom(self, index):
        """
        Return specific atom in Structure instance.

        Arguments:
            *index*
                Index of the atom
        Return:
            Returns an Atom instance.
        """
        return self.atomList[int(index)]

    def get_backbone(self):
        """
        Return:
            Structure instance with only the backbone atoms in structure.
        """
        backboneList = []
        for atom in self.atomList:
            if (
                atom.get_name() == "CA"
                or atom.get_name() == "N"
                or atom.get_name() == "C"
            ):
                backboneList.append(atom.copy())
        return BioPy_Structure(backboneList[:])

    def get_CAonly(self):
        """
        Return:
            Structure instance with only the backbone atoms in structure.
        """
        backboneList = []
        for atom in self.atomList:
            if atom.get_name() == "CA":
                backboneList.append(atom.copy())
            else:
                pass
        return BioPy_Structure(backboneList)

    def vectorise(self):
        vectorList = []
        vList = []
        for x in self.atomList:
            vectorList.append(x.get_pos_vector())
        for y in range(len(vectorList) - 1):
            vList.append(vectorList[y] - (vectorList[y + 1]))
        return vList

    def get_torsion_angles(self):
        """
        Return:
            List of torsion angles in Structure instance.
        """
        vectorList = self.vectorise()
        angles = []
        for v in range(len(vectorList) - 2):
            angles.append(
                Vector.altTorsion(
                    vectorList[v], vectorList[v + 1].reverse(), vectorList[v + 2]
                )
            )
        return angles

    def get_prot_mass_from_res(self, Termini=False):
        """
        # ADD by IF 22-4-2013
        #from Harpal  code calculation of mass from seq.
        Calculates Mass (kDa) of the Structure instance, from average mass
        #based on http://web.expasy.org/findmod/findmod_masses.html
        """
        aa = {
            "ARG": "R",
            "HIS": "H",
            "LYS": "K",
            "ASP": "D",
            "GLU": "E",
            "SER": "S",
            "THR": "T",
            "ASN": "N",
            "GLN": "Q",
            "CYS": "C",
            "SEC": "U",
            "GLY": "G",
            "PRO": "P",
            "ALA": "A",
            "ILE": "I",
            "LEU": "L",
            "MET": "M",
            "PHE": "F",
            "TRP": "W",
            "TYR": "Y",
            "VAL": "V",
        }
        mass_tot = 0
        str = self.copy()
        seq_string = ""
        for chain in str.split_into_chains():
            seq_list_resno = []
            for x in chain.atomList:
                if x.res in aa.keys():
                    if x.res_no not in seq_list_resno:
                        seq_list_resno.append(x.res_no)
                        if x.res not in aa.keys():
                            seq_string += "x"
                        res_singleletter = aa[x.res]
                        seq_string += "%s" % res_singleletter
                        mass_tot += AA_MASS[res_singleletter]
                else:
                    pass
        if Termini:
            mass_tot += 17.992
        return float(mass_tot / 1000)

    def get_prot_mass_from_atoms(self):
        """
        Calculates Mass (kDa) of the Structure instance, from average mass.
        Atoms based use get_prot_mass_from_res is more accurate.
        """
        mass_tot = 0
        for x in self.atomList:
            mass_tot += x.get_mass()
        return float(mass_tot / 1000)


class gemmi_Structure(BioPy_Structure):
    """
    Class for representing a protein structure.

    Extends BioPy_Structure to deal with additional mmCif labels for dividing
    atoms into entities, asym units and chains.


    """

    def __init__(
        self,
        atomList,
        gemmi_structure,
        filename="Unknown",
        header="",
        tempy_scores=[],
    ):
        """
        Initialise using a string of the relevant pdb file name or a numpy
        array of Atom objects.

        Arguments:
            *atomList*
                String of pdb file name or array of Atom objects
            *gemmi_structure*
                An instance of a gemmi structure object generated from an mmcif
                or pdb file
        """
        super().__init__(atomList)

        self.header = header
        self.pdb_id = gemmi_structure.name
        self.filename = filename

        self.chain_indexes = dict()
        self.asym_id_indexes = dict()
        self.entity_id_indexes = dict()
        self.set_chains_asymids_entities()

        self.local_scores = collections.OrderedDict()
        self.local_score_labels = {}
        self.global_scores = collections.OrderedDict()
        self.read_tempy_scores(tempy_scores)

    def __getitem__(self, index):
        return self.atomList[index]

    def __len__(self):
        return len(self.atomList)

    def __repr__(self):
        s = "Gemmi_Structure: %s \n" % (self.pdb_id)
        if not self.filename == "Unknown":
            s += ", Filename: " + self.filename + "\n"
        else:
            pass
        s += "No Of Atoms: " + str(len(self)) + "\n"
        s += "First Atom: " + str(self.atomList[0]) + "\n"
        s += "Last Atom: " + str(self.atomList[-1])
        return s

    def get_pdb_id(self):
        return self.pdb_id

    def copy(self):
        return copy.deepcopy(self)

    def get_chain_indexes(self):
        chain_indexes = collections.OrderedDict()

        for n, atom in enumerate(self.atomList):
            try:
                chain_indexes[atom.chain].append(n)
            except KeyError:
                chain_indexes[atom.chain] = [n]

        self.chain_indexes = chain_indexes

    def get_asym_indexes(self):
        asym_indexes = collections.OrderedDict()

        for n, atom in enumerate(self.atomList):
            try:
                asym_indexes[atom.asym_id].append(n)
            except KeyError:
                asym_indexes[atom.asym_id] = [n]

        self.asym_id_indexes = asym_indexes

    def get_entity_indexes(self):
        entity_indexes = collections.OrderedDict()

        for n, atom in enumerate(self.atomList):
            try:
                entity_indexes[atom.model].append(n)
            except KeyError:
                entity_indexes[atom.model] = [n]

        self.entity_id_indexes = entity_indexes

    def set_chains_asymids_entities(self):
        chains = {}
        asym_ids = {}
        entities = {}

        for ind, atom in enumerate(self.atomList):
            try:
                chains[atom.chain].append(ind)
            except KeyError:
                chains[atom.chain] = [ind]

            try:
                asym_ids[atom.asym_id].append(ind)
            except KeyError:
                asym_ids[atom.asym_id] = [ind]

            try:
                entities[atom.model].append(ind)
            except KeyError:
                entities[atom.model] = [ind]

        self.chain_indexes = chains
        self.asym_id_indexes = asym_ids
        self.entity_id_indexes = entities

    def get_asym_id_atoms(self, asym_id):

        return self.atomList[self.asym_id_indexes[asym_id]]

    def get_chain_atoms(self, chain_id):

        return self.atomList[self.chain_indexes[chain_id]]

    def get_entity_atoms(self, entity_id):

        return self.atomList[self.entity_id_indexes[entity_id]]

    def get_next_entity_id(self, entity_id):

        try:
            old_entity_id = int(entity_id)
        except ValueError:
            old_entity_id = 0

        return str(old_entity_id + 1)

    def reorder_atoms(self):
        new_atom_list = []
        serial = 1

        for chain, indexes in self.chain_indexes.items():
            atoms_from_chain = self.atomList[indexes]
            for atom in atoms_from_chain:
                atom.serial = serial
                new_atom_list.append(atom)
                serial += 1

        self.atomList = np.array(new_atom_list)
        self.set_chains_asymids_entities()

    def set_atom_labels(self):
        """
        Sets chain, asym_id and entity_id labels for the atoms in atomList

        Important to run this before file writing
        """

        for chain_label, indexes in self.chain_indexes.items():
            for atom in self.atomList[indexes]:
                atom.chain = chain_label

        for asym_label, indexes in self.asym_id_indexes.items():
            for atom in self.atomList[indexes]:
                atom.asym_id = asym_label

        for entity_id, indexes in self.entity_id_indexes.items():
            for atom in self.atomList[indexes]:
                atom.model = str(entity_id)

    def split_into_chains(self):
        """
        Overrides BioPy_Structure method

        Split the structure into separate chains and returns the list of
        Structure instance for each chain.
        """
        new_structure = self.copy()
        structList = []
        for chain_name in self.chain_indexes.keys():
            structList.append(new_structure.get_chain(chain_name))

        return structList

    def get_chain(self, chainID):
        """
        Return:
            New Structure instance with only the requested chain.
        """
        new_atom_list = self.atomList[self.chain_indexes[chainID]]

        struct = gemmi.Structure()
        struct.name = self.pdb_id + "chain%s" % (chainID)

        return gemmi_Structure(new_atom_list, struct)

    def add_structure_instance(
        self,
        new_structure,
        integrate=False,
    ):
        """Add a seperate structure instance to self

        **Arguements:**
            *new_structure*
                the new structure instance which will be incorpoated into self
        **Optional Arguments:**
            *integrate*
                If True, atoms from the new_structure will be incorporated into
                chains with the same name in self.

        """

        target_struct = new_structure.copy()

        # set up stuff
        if not self.chain_indexes:
            self.set_chains_asymids_entities()
        available_chain_labels = [char for char in ALPHABET]

        for key in self.chain_indexes.keys():
            try:
                available_chain_labels.pop(available_chain_labels.index(key))
            except ValueError:  # occurs if chains have label not in ALPHABET
                continue

        # get lists of current labels
        existing_chains = self.chain_indexes.keys()
        existing_asym = self.asym_id_indexes.keys()
        existing_entities = self.entity_id_indexes.keys()

        # prep new labels in case they are needed
        new_chain_id = self.get_next_chain_id(
            self.atomList[-1].chain,
            chain_list=available_chain_labels,
        )
        new_asym_id = self.iter_asym_id(self.atomList[-1].asym_id)
        while new_asym_id in existing_asym:
            new_asym_id = self.iter_asym_id(new_asym_id)
        new_entity_id = self.get_next_entity_id(self.atomList[-1].model)
        while new_entity_id in existing_entities:
            new_entity_id = self.get_next_entity_id(new_entity_id)

        # get lists of current labels
        existing_chains = list(self.chain_indexes.keys())
        existing_asym = list(self.asym_id_indexes.keys())
        existing_entities = list(self.entity_id_indexes.keys())

        if not integrate:
            for new_chain, indexes in target_struct.chain_indexes.items():
                if new_chain in existing_chains:
                    for ind in indexes:
                        target_struct[ind].chain = new_chain_id
                    new_chain_id = self.get_next_chain_id(
                        new_chain_id,
                        chain_list=available_chain_labels,
                    )
                if target_struct[indexes[0]].asym_id in existing_asym:
                    existing_asym.append(new_asym_id)
                    for ind in indexes:
                        target_struct[ind].asym_id = new_asym_id
                    while new_asym_id in existing_asym:
                        new_asym_id = self.iter_asym_id(new_asym_id)

                if target_struct[indexes[0]].model in existing_entities:
                    existing_entities.append(new_entity_id)
                    for ind in indexes:
                        target_struct[ind].model = new_entity_id
                    while new_entity_id in existing_entities:
                        new_entity_id = self.get_next_entity_id(new_entity_id)

                new_atoms = target_struct.atomList[indexes]
                self.atomList = np.append(self.atomList, new_atoms)
            self.set_chains_asymids_entities()
        else:
            target_struct.set_chains_asymids_entities()
            for chain, indexes in target_struct.chain_indexes.items():
                new_atoms = target_struct.atomList[indexes]
                self.atomList = np.append(self.atomList, new_atoms)

            self.set_chains_asymids_entities()
            self.reorder_atoms()

    def add_structure(
        self,
        filename,
        integrate=False,
        hetatm=False,
        water=False,
    ):
        """
        Add structure from file
        """

        import TEMPy.protein.structure_parser as parser

        if filename.endswith(".cif"):
            new_structure = parser.mmCIFParser.read_mmCIF_file(
                filename,
                hetatm=hetatm,
                water=water,
            )
        elif filename.endswith(".pdb"):
            new_structure = parser.PDBParser.read_PDB_file(
                filename, hetatm=hetatm, water=water
            )
        else:
            raise TypeError("Unrecognised file type for file merging")
        self.add_structure_instance(
            new_structure,
            integrate=integrate,
        )
        del new_structure

    def combine_structures(self, structList):
        """Combine a list of structure instances with self and returns the new
        structure as a seperate instance.

        Note: this function does not mutate self.

        **Arguments:**
            *structList*
                List of Structure instances
        **Returns:**
            *combined_struct*
                New gemmi_Structure instance
        """
        combined_struct = self.copy()
        for s in structList:
            combined_struct.add_structure_instance(s)
        return combined_struct

    def write_to_mmcif(
        self,
        filename,
        hetatom=False,
        save_all_metadata=False,
    ):
        """Write Structure instance to new mmCif file.

        Arguments:
            *filename*
                output filename.
        """
        cif_instance = mmcif_writer(
            self,
            filename,
            save_all_metadata=save_all_metadata,
        )

        if filename[-4:] == ".cif":
            pass
        else:
            filename += ".cif"

        self.header = mmcif_writer.clean_header(cif_instance.header)

        f = open(filename, "w")
        f.write("data_" + self.get_pdb_id() + "\n#\n")

        # add header info into gemmi block
        if self.header:
            header_tags = self.header["tags"]
            for tag in header_tags:

                if mmcif_writer.is_pair(self.header[tag]):
                    for line in mmcif_writer.get_pairs_str_list(tag, self.header[tag]):
                        f.write(line + "\n")
                else:
                    for line in mmcif_writer.get_table_str_list(tag, self.header[tag]):
                        f.write(line + "\n")
                f.write("#\n")

        for line in mmcif_writer.get_atoms_str_list(self.atomList):
            f.write(line + "\n")
        f.write("#\n")

        if self.local_scores:
            mmcif_writer.write_tempy_localscores(
                f, self.local_scores, self.local_score_labels
            )
            f.write("#\n")

        if self.global_scores:
            global_scores = mmcif_writer.get_global_score_pairs(self.global_scores)

            for line in global_scores:
                f.write(line + "\n")
            f.write("#\n")

        f.close()
        print("Protein structure saved as %s" % (filename))

    def get_model_atoms(self, model_ID):
        """ """
        return self.atomList[self.entity_id_indexes[model_ID]]

    def rename_asym_labels(self, label_list=False, starting_val=False):
        """Renames asym_id for each atom in alphabetical order

        For structures with more than 26 models the ids switch to doulbe
        lettering (i.e. from Z -> AA and from ZZZ -> AAAA)
        """
        if not starting_val:
            if label_list:
                new_asym_id = label_list[0]
            else:
                new_asym_id = "A"
        else:
            new_asym_id = starting_val
        new_asym_id_indexes = collections.OrderedDict()

        for old_asym_id, indexes in self.asym_id_indexes.items():
            new_asym_id_indexes[new_asym_id] = indexes
            for atom in self.atomList[indexes]:
                atom.asym_id = new_asym_id
            if label_list:
                new_asym_id = self.get_next_chain_id(new_asym_id, label_list)
            else:
                new_asym_id = self.iter_asym_id(new_asym_id)

        self.asym_id_indexes = new_asym_id_indexes

    def rename_entity_labels(self, starting_val=1):
        """
        Renames asym_id for each atom in alphabetical order - for structures
        with more than 26 models the ids switch to doulbe lettering (i.e. from
        Z -> AA and from ZZZ -> AAAA)
        """
        new_entity_id = int(starting_val)

        new_entity_id_indexes = collections.OrderedDict()

        for old_entity_id, indexes in self.entity_id_indexes.items():
            new_entity_id_indexes[str(new_entity_id)] = indexes
            for atom in self.atomList[indexes]:
                atom.model = str(new_entity_id)
            new_entity_id += 1

        self.entity_id_indexes = new_entity_id_indexes

    def rename_chains(self, chain_list=False, starting_val=False):
        """Rename chain labels based on the list of new chain names

        **Optional Arguments:**
             *chain_list*
                 List of chain names
                 If False rename in alphabetical order.
        """
        if not chain_list:
            chain_list = ALPHABET
        else:
            if len(chain_list) == 0:
                print("Length of chain list = " + str(len(chain_list)))
                print("Chains not changed.")
                return

        if starting_val:
            new_chain = starting_val
        else:
            new_chain = chain_list[0]
        new_chains_dict = collections.OrderedDict()

        for old_chain_label, indexes in self.chain_indexes.items():
            new_chains_dict[new_chain] = indexes
            for atom in self.atomList[indexes]:
                atom.chain = new_chain
            new_chain = self.get_next_chain_id(
                new_chain,
                chain_list=chain_list,
            )
        self.chain_indexes = new_chains_dict

    def no_of_chains(self):
        """
        Return:
            the number of chains in the Structure object
        """
        return len(self.chain_indexes.keys())

    def set_local_score(self, score_name, scores, verbose=False):
        """
        Function to incorporate local scores into structure instance, so that
        these values can be written into new cif files

        This would be efficiently handled using a pandas library
        """
        if not self.local_scores:
            self.local_scores = collections.OrderedDict()
            for chain in scores:
                for res_no in scores[chain]:
                    self.local_scores[(chain, res_no)] = [scores[chain][res_no]]
                    self.local_score_labels[score_name] = 0
        else:
            # for updating existing entries
            try:
                self.local_score_labels[score_name]
                if verbose:
                    print("Updating values for %s score" % (score_name))
                for chain in scores:
                    for res_no in scores[chain]:
                        self.local_scores[(chain, res_no)] = [scores[chain][res_no]]
            # if score entry doesn't exist make a new one
            except KeyError:
                for chain in scores:
                    for res_no in scores[chain]:
                        self.local_scores[(chain, res_no)].append(scores[chain][res_no])
                        self.local_score_labels[score_name] = (
                            len(self.local_scores[(chain, res_no)]) + 1
                        )

    def get_aa_local_score(self, score_name, chain, aa_no):
        index = self.local_score_labels[score_name]
        return self.local_scores[(chain, aa_no)][index]

    def set_global_score(self, score_name, score):
        """
        Function to incorporate global scores into the structure instance so
        these values can be written into the cif file as label-value pairs
        """

        self.global_scores[score_name] = score

    def get_global_score(self, score_name):
        """
        return global score
        """

        try:
            return self.global_scores[score_name]
        except KeyError:
            raise KeyError("The global score %s does not exist" % (score_name))

    def read_tempy_scores(self, tempy_scores):

        for tag in tempy_scores:
            if tag.endswith("local_score."):

                scoring_block = tempy_scores[tag]
                scoring_values = [scoring_block[key] for key in scoring_block]

                for n, label in enumerate(scoring_block.keys()):
                    if n < 2:
                        continue
                    self.local_score_labels[label] = n - 2

                for i in range(len(scoring_values[0])):
                    chain = scoring_values[0][i]
                    aa_no = int(scoring_values[1][i])
                    for n in range(2, len(scoring_block.keys())):
                        score_value = float(scoring_values[n][i])
                        try:
                            self.local_scores[chain, aa_no].append(score_value)
                        except KeyError:
                            self.local_scores[chain, aa_no] = [score_value]

            elif tag.endswith("global_score."):
                for n, label in enumerate(tempy_scores[tag].keys()):
                    self.global_score[label] = tempy_scores[tag]

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
#     Please cite your use of TEMPy in published work:
#
#     Farabella, I., Vasishtan, D., Joseph, A.P., Pandurangan, A.P., Sahota, H.
#     & Topf, M. (2015). J. Appl. Cryst. 48.
#
# =============================================================================
import os
import subprocess
import urllib
import collections

from numpy import append

from TEMPy.protein.prot_rep_biopy import (
    BioPy_Structure,
    gemmiAtom,
    gemmi_Structure,
)
import TEMPy.math.vector as Vector

try:
    from gemmi import cif
    import gemmi
except ImportError:
    raise ImportError(
        'GEMMI library needs to be installed to use TEMPy\'s mmCIF and PDB'
        'parsers Gemmi can be installed using command: pip install gemmi'
        )

AAs = {
    'GLY': 'G',
    'ALA': 'A',
    'VAL': 'V',
    'LEU': 'L',
    'ILE': 'I',
    'MET': 'M',
    'PHE': 'F',
    'TRP': 'W',
    'PRO': 'P',
    'SER': 'S',
    'THR': 'T',
    'CYS': 'C',
    'TYR': 'Y',
    'ASN': 'N',
    'GLN': 'Q',
    'ASP': 'D',
    'GLU': 'E',
    'LYS': 'K',
    'ARG': 'R',
    'HIS': 'H',
}


class mmCIFParser:

    """ Class for parsing mmCIF files using the GEMMI library.

    All functions contained in the mmCIFParser class are "staticmethods",
    meaning an object does not need to initiated before using the methods, as
    shown in the :ref:`code examples<Model Parsing Code Example>`.
    """

    def __init__(self, filename):
        self.compressed = False
        self.acol_widths = []

        self._is_file_compressed(filename)

    def _is_file_compressed(self, filename):
        if filename[-2:] == 'gz':
            self.compressed = True
        else:
            self.compressed = False

    @staticmethod
    def _convertGEMMItoTEMPy(
                            data_block,
                            structure,
                            filename,
                            water=False,
                            hetatm=False
                            ):
        """
        Private function: converts the gemmi parsed info from a cif file
        into TEMPy conventions - mostly focusses on _atom_site. information
        which is used to initialise gemmiAtom instances

        Args:
            data_block: A data block from a cif file, typically accessed using
                .sole_block gemmi instance method
            filename: Input filename
            hetatm: If True, HETATM atoms are included in the
                :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`
                returned after parsing. If False, HETATM atoms are ignored.
            water: If True, HETATM, water atoms are included in the
                :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`
                instance returned after parsing. If False, HETATM atoms are
                ignored.
        Returns:
            :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`:
                Parsed structure.
        """
        # remove waters and hetatms if required
        if not water:
            structure.remove_waters()
        if not hetatm:
            structure.remove_ligands_and_waters()

        structure.remove_empty_chains()  # deleting hetatms empties some chains
        atomList = []

        for model in structure:
            for chain in model:
                for entity in structure.entities:
                    for subchain in entity.subchains:
                        for residue in chain.get_subchain(subchain):
                            for atom in residue:
                                atomList.append(gemmiAtom(
                                                        chain,
                                                        entity,
                                                        residue,
                                                        atom))

        # grab the remaining metadata
        header = {}
        header_tags = []
        tempy_scores = collections.OrderedDict()
        tempy_headers = []

        for tag in data_block.get_mmcif_category_names():
            if tag != '_atom_site.':
                header_tags.append(tag)
                header[tag] = data_block.get_mmcif_category(tag, raw=True)
            if tag.startswith('_TEMPy'):
                tempy_headers.append(tag)
                tempy_scores[tag] = data_block.get_mmcif_category(
                                                                tag,
                                                                raw=True)

        header['tags'] = tuple(header_tags)

        return gemmi_Structure(
            atomList,
            structure,
            filename=filename,
            header=header,
            tempy_scores=tempy_scores,
            )

    @staticmethod
    def read_mmCIF_file(filename, hetatm=False, water=False):
        """Read an mmCIF file to generate a Structure instance.

        Uses the `Gemmi <https://gemmi.readthedocs.io/en/latest/index.html>`_
        library to parse the input PDB file.

        Args:
            filename: Path to the input file
            hetatm: If True, HETATM atoms are included in the
                :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`
                returned after parsing. If False, HETATM atoms are ignored.
            water: If True, HETATM, water atoms are included in the
                :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`
                instance returned after parsing. If False, HETATM atoms are
                ignored.
        Returns:
            :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`:
                Parsed structure.

        """

        cif_data_block = cif.read(filename).sole_block()
        structure = gemmi.make_structure_from_block(cif_data_block)

        return mmCIFParser._convertGEMMItoTEMPy(
                                                cif_data_block,
                                                structure,
                                                filename,
                                                hetatm=hetatm,
                                                water=water)

    @staticmethod
    def fetch_mmCIF(
                    structure_id,
                    local_filename,
                    hetatm=False,
                    water=False,
                    ):
        """Fetch an mmCIF file from the Protein Data Bank, and use it to
        generate a Structure instance.

        Uses the `Gemmi <https://gemmi.readthedocs.io/en/latest/index.html>`_
        library to parse the input PDB file.

        Args:
            structure_id: structure_id code of pdb file, e.g. 3agy
            local_filename: Filename for locally saved the fetched mmCIF file
            hetatm: If True, HETATM atoms are included in the
                :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`
                returned after parsing. If False, HETATM atoms are ignored.
            water: If True, HETATM, water atoms are included in the
                :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`
                instance returned after parsing. If False, HETATM atoms are
                ignored.
        Returns:
            :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`:
                Parsed structure.

        """

        url = 'http://www.rcsb.org/pdb/files/%s.cif' % structure_id
        new_file, someinfo = urllib.request.urlretrieve(
                                                    url,
                                                    filename=local_filename)

        return mmCIFParser.read_mmCIF_file(
                                            new_file,
                                            hetatm=hetatm,
                                            water=water)


class PDBParser:
    """
    A class to read PDB files either directly from the pdb or a structure
    instance from Biopython
    """
    def __init__(self):
        pass

    @staticmethod
    def read_PDB_file(
            structure_id,
            filename,
            hetatm=False,
            water=False,
            chain=None,
    ):
        """ Read PDB file and create Structure instance.

        Uses the `Gemmi <https://gemmi.readthedocs.io/en/latest/index.html>`_
        library to parse the input PDB file.

        Args:
            structure_id: structure_id code of pdb file
            filename: Filename (path) of pdb file
            hetatm: If True, HETATM atoms are included in the
                :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`
                returned after parsing. If False, HETATM atoms are ignored.
            water: If True, HETATM, water atoms are included in the
                :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`
                instance returned after parsing. If False, HETATM atoms are
                ignored.
        Returns:
            :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`:
                Parsed structure.
        """

        # Necessary to read pdb file and transform it to Gemmi cif format
        structure = gemmi.read_pdb(filename)

        # pdb files created by some software can have blank/empty chain names
        if not structure[0][0].name:
            structure = gemmi_helper_fns.name_nameless_chains(structure)

        structure.remove_empty_chains()
        structure.setup_entities()
        structure.assign_label_seq_id()
        data_block = structure.make_mmcif_document().sole_block()

        return mmCIFParser._convertGEMMItoTEMPy(
                                            data_block,
                                            structure,
                                            filename,
                                            water=water,
                                            hetatm=hetatm,
                                            )

    @staticmethod
    def fetch_PDB(
            structure_id,
            local_filename,
            hetatm=False,
            water=False,
    ):
        """ Fetch PDB file from the PDB and create Structure instance based
        upon it.

        Uses the `Gemmi <https://gemmi.readthedocs.io/en/latest/index.html>`_
        library to parse the input PDB file.

        Args:
            structure_id: structure_id code of pdb file
            local_filename: Filename for locally saved the fetched pdb file
            hetatm: If True, HETATM atoms are included in the
                :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`
                returned after parsing. If False, HETATM atoms are ignored.
            water: If True, HETATM, water atoms are included in the
                :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`
                instance returned after parsing. If False, HETATM atoms are
                ignored.
        Returns:
            :class:`Structure instance <TEMPy.protein.prot_rep_biopy.gemmi_Structure>`:
                Parsed structure.
        """
        url = 'http://www.rcsb.org/pdb/files/%s.pdb' % structure_id
        new_file, someinfo = urllib.request.urlretrieve(
                                                    url,
                                                    filename=local_filename)

        return PDBParser.read_PDB_file(structure_id, new_file)

    @staticmethod
    def _bio_strcuture_to_TEMpy(
            filename,
            structure,
            pdb_id,
            hetatm=False,
            water=False,
    ):
        """
        PRIVATE FUNCTION to convert to Structure Instance
        filename = name of mmCIF file
        hetatm = Boolean representing whether to add hetatm to the
        structure.Default and Raccomanded is False.
        water = Boolean representing whether to add water to the
        structure.Default and Raccomanded is False.
        """
        atomList = []
        hetatomList = []
        wateratomList = []
        footer = ''
        header = ''
        residues = structure.get_residues()
        for res in residues:
            hetfield = res.get_id()[0]
            if hetfield[0] == "H":
                for atom in res:
                    # BioPyAtom(atom)
                    hetatomList.append(gemmiAtom(atom))
            elif hetfield[0] == "W":
                for atom in res:
                    # BioPyAtom(atom)
                    wateratomList.append(gemmiAtom(atom))
            else:
                for atom in res:
                    # BioPyAtom(atom)
                    atomList.append(gemmiAtom(atom))
        if hetatm:
            atomList = append(atomList, hetatomList)
        if water:
            atomList = append(atomList, wateratomList)

        return BioPy_Structure(
            atomList,
            filename=filename,
            header=header,
            footer=footer,
            pdb_id=pdb_id
        )

    @staticmethod
    def calc_SA(self, pdbfile, rsa=True, outsafile=None):
        assert os.path.isfile(pdbfile)
        if outsafile is None:
            outsafile = os.path.basename(pdbfile) + '_sa.out'
        cmd = (
                "~/data/packages/freesasa/freesasa-1.1/src/freesasa %s "
                "--rsa_file=%s --no-log --radii=naccess" %
                (pdbfile, outsafile)
        )
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        p.communicate()

    @staticmethod
    def write_sasd_to_txt(sasds, pdb):
        """Write solvent accessible distances to a text (.txt) file.


        The output text file has the default name
        :code:`"./Jwalk_results/{pdb_code}_crosslinks.pdb"`, where pdb_code
        is, for example, 3agy for PDB file with name 3agy.pdb.

        Args:
            sasds: Dictionary of sasds
            pdb: PDB file sasds were calculated on

        """
        if not os.path.exists('./Jwalk_results'):
            os.makedirs('./Jwalk_results')

        with open(
                './Jwalk_results/%s_crosslink_list.txt' % pdb[:-4],
                'w'
        ) as outf:
            outf.write(
                ' '.join('{0:<13}'.format(col) for col in [
                    'Index',
                    'Model',
                    'Atom1',
                    'Atom2',
                    'SASD',
                    'Euclidean Distance',
                ])
            )
            outf.write('\n')
            index = 1
            for xl in sasds:
                (aa1, chain1, res1) = xl[0]
                (aa2, chain2, res2) = xl[1]
                atom1 = ('%s-%d-%s-CA' % (res1, aa1, chain1))
                atom2 = ('%s-%d-%s-CA' % (res2, aa2, chain2))
                sasd = xl[2]
                ed = xl[3]
                outf.write(
                    ' '.join('{0:<13}'.format(col) for col in [
                        index,
                        pdb,
                        atom1,
                        atom2,
                        sasd,
                        ed,
                    ])
                )
                outf.write('\n')
                index += 1

    @staticmethod
    def write_sasd_to_pdb(dens_map, sasds, pdb):
        """Write solvent accessible distances to a PDB file.

        The output text file has the default name
        :code:`"./Jwalk_results/{pdb_code}_crosslinks.pdb"`, where pdb_code
        is, for example, 3agy for PDB file with name 3agy.pdb.

        Args:
            dens_map: Solvent accessible surface on masked array
            sasds: Dictionary of sasds
            pdb: pdb file sasds were calculated on
        """
        if not os.path.exists('./Jwalk_results'):
            os.makedirs('./Jwalk_results')

        apix = dens_map.apix
        origin = dens_map.origin
        path_coord = {}

        for xl in sasds:
            a = []
            for (x, y, z) in sasds[xl]:
                a.append(
                    [
                        (x * apix) + origin[0],
                        (y * apix) + origin[1],
                        (z * apix) + origin[2]
                    ]
                )
            path_coord[xl] = a

        with open('./Jwalk_results/%s_crosslinks.pdb' % pdb[:-4], 'w') as pdb:
            m_count = 1
            for xl in path_coord:
                (aa1, chain1, res1) = xl[0]
                (aa2, chain2, res2) = xl[1]
                count = 1
                pdb.write(
                    'MODEL %d %s%d%s-%s%d%s\n' % (
                        m_count,
                        res1,
                        aa1,
                        chain1,
                        res2,
                        aa2,
                        chain2,
                    )
                )
                m_count = m_count+1
                for (x, y, z) in path_coord[xl]:
                    p = Vector.Vector(x, y, z)
                    a = p.to_atom()
                    a.record_name = 'ATOM'
                    a.serial = count
                    a.atom_name = 'C'
                    a.alt_loc = ''
                    a.res = 'GLY'
                    a.chain = 'A'
                    a.res_no = count
                    a.icode = ''
                    a.occ = 1
                    a.temp_fac = 0
                    a.elem = 'C'
                    a.charge = ''
                    pdb.write(a.write_to_PDB())
                    count += 1
                pdb.write('END\n')


class gemmi_helper_fns:

    @staticmethod
    def name_nameless_chains(g_structure):
        """
        Function to give names to chains in gemmi Structure objects that have
        blank names. Occurs due to pdb files with no chain label. In such
        files, all residues and atoms will be placed into one chain with no
        name.

        Input: Gemmi Structure instance (with blank chain names)

        Output: Gemmi Structure instance with chains named A, B, C ....
                (in most/all cases will be one chain named A)
        """
        for model in g_structure:
            for n, chain in enumerate(model):
                if not chain.name:
                    # check ASCII table - will give chain 0 name 'A'
                    chain.name = chr(n+65)
        return g_structure

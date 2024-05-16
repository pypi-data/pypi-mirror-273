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

from collections import OrderedDict
import gemmi

TEMPY_CITATION_ID = 'TEMPy'

TEMPY_CITATION = OrderedDict([
    ('id', TEMPY_CITATION_ID),
    ('title', 'TEMPy: a Python library for assessment of three-dimensional electron microscopy density fits.'),  # noqa: E501
    ('journal_abbrev', ' J. Appl. Cryst.'),
    ('journal_volume', '48'),
    ('year', '2015'),
    ('page_first', '1314'),
    ('page_last', '1323'),
    ('pdbx_database_id_DOI', '10.1107/S1600576715010092')
 ])

# not sure if this is correct or not really
TEMPy_audit_conform = (
    "audit_conform",
    (
        "dict_name",
        "dict_version",
        "dict_location",
    ), (
        "mmcif_pdbx.dic",
        "4.007",
        "http://mmcif.pdb.org/dictionaries/ascii/mmcif_pdbx.dic",
    )
)

TEMPY_AUTHORS = (
    'I. Farabella',
    'D. Vasishtan',
    'A. P. Joseph',
    'A. P. Pandurangan',
    'H. Sahota'
    'M. Topf'
)


class mmcif_writer:
    """
    A batch of functions for formatting the gemmi blocks and TEMPy atom objects
    for mmcif file writing
    """

    def __init__(
                self,
                structure,
                new_filename,
                save_all_metadata=False,
                ):

        self.tempy_structure = structure
        self.new_filename = new_filename
        self.header = structure.header
        self.gemmi_structure = self.make_gemmi_structure()
        self.save_all_metadata = save_all_metadata

        self.gemmi_structure.remove_empty_chains()
        self.update_header()

    def make_gemmi_structure(self):
        '''
        Build a gemmi Structure object using the info from the tempy structure
        and atom objects
        '''

        try:
            cif_data_block = gemmi.cif.read(
                                            self.tempy_structure.filename
                                            ).sole_block()
            gstructure = gemmi.make_structure_from_block(cif_data_block)
            del gstructure[0]
        except ValueError: #RuntimeError:  # filename couldn't be found
            gstructure = gemmi.Structure()
            gstructure.name = self.tempy_structure.pdb_id

        model = gemmi.Model('1')

        for chain_name, indexes in self.tempy_structure.chain_indexes.items():
            chain = (gemmi.Chain(chain_name))
            atoms_from_chain = self.tempy_structure.atomList[indexes]
            atom_index = 0

            while atom_index < len(indexes):
                residue = gemmi.Residue()
                atom = atoms_from_chain[atom_index]
                residue.entity_type = atom.entity_type
                residue.flag = atom.res_flag
                residue.het_flag = atom.record_name[0]
                residue.label_seq = atom.seq_id
                residue.name = atom.res
                residue.segment = atom.segment
                residue.seqid.icode = atom.seqid_icode
                residue.seqid.num = atom.res_no
                residue.subchain = atom.asym_id
                old_res_id = res_id = atom.res_no

                while res_id == old_res_id:
                    atom = atoms_from_chain[atom_index]
                    gatom = gemmi.Atom()
                    gatom.altloc = atom.alt_loc
                    gatom.b_iso = atom.temp_fac
                    gatom.calc_flag = atom.calc_flag
                    gatom.charge = atom.charge
                    gatom.element = gemmi.Element(atom.elem)
                    gatom.flag = atom.atom_flag
                    gatom.name = atom.atom_name
                    gatom.occ = atom.occ
                    gatom.pos.x = atom.x
                    gatom.pos.y = atom.y
                    gatom.pos.z = atom.z
                    gatom.serial = atom.serial
                    gatom.tls_group_id = atom.tls_group_id
                    residue.add_atom(gatom)
                    atom_index += 1
                    try:
                        res_id = atoms_from_chain[atom_index].res_no
                    except IndexError:
                        break
                chain.add_residue(residue)
            model.add_chain(chain)
        gstructure.add_model(model)

        entity_list = gemmi.EntityList()
        for entity_name, indexes in \
                self.tempy_structure.entity_id_indexes.items():
            new_entity = gemmi.Entity(str(entity_name))
            entity_atoms = self.tempy_structure.atomList[indexes]
            new_entity.entity_type = entity_atoms[0].entity_type
            new_entity.polymer_type = entity_atoms[0].polymer_type
            subchains = set(entity_atoms[0].asym_id)
            label = entity_atoms[0].seq_id
            seq = [entity_atoms[0].res]

            for atom in entity_atoms:
                subchains.add(atom.asym_id)
                if atom.seq_id == label:
                    continue
                else:
                    label = atom.seq_id
                    seq.append(atom.res)

            new_entity.full_sequence = seq
            new_entity.subchains = sorted(list(subchains))
            entity_list.append(new_entity)
        gstructure.entities = entity_list

        return gstructure

    def update_header(self):

        groups = gemmi.MmcifOutputGroups(True)
        groups.exptl = False
        groups.diffrn = False
        groups.refine = False
        groups.software = False

        if self.save_all_metadata:
            block = self.gemmi_structure.make_mmcif_document().sole_block()
            self.gemmi_structure.update_mmcif_block(block, groups)
            tag_names = list(self.header['tags'])
        else:
            doc = gemmi.cif.Document()
            block = doc.add_new_block(self.tempy_structure.pdb_id)
            self.gemmi_structure.update_mmcif_block(block, groups)
            self.header = {}
            tag_names = []

        for tag in block.get_mmcif_category_names():
            if tag == '_atom_site.':
                continue
            data_block = block.get_mmcif_category(tag, raw=True)

            try:
                # Tries to update metadata
                self.header[tag]
                for column_id in data_block.keys():
                    self.header[tag][column_id] = data_block[column_id]
            except KeyError:
                # Creates metadata if it doesn't exist
                self.header[tag] = data_block

            if tag not in tag_names:
                tag_names.append(tag)

        self.header['tags'] = tuple(tag_names)

    @staticmethod
    def clean_header(header):
        """
        Function to search through the header and footer parsed by Gemmi and
        remove entries that are incorrectly formatted
        This is done because converting pdb files to mmcif format is not error
        free in gemmi

        Inputs: header and footer
        Output: header and footer with dodgy entries removed
        """
        new_header_tags = []
        for tag in header['tags']:
            header_is_okay = True
            table_or_pair = header[tag]

            for key, column in table_or_pair.items():
                if not column or len(column) == 0 or column[0] == '':
                    header_is_okay = False
                    break

            if header_is_okay:
                new_header_tags.append(tag)
            else:
                header.pop(tag)
        header['tags'] = tuple(new_header_tags)

        return header

    @staticmethod
    def get_atm_ljust(atom_ljust, atom_vals):
        for n, i in enumerate(atom_vals):
            if len(i) > atom_ljust[n]:
                atom_ljust[n] = len(i)
        return atom_ljust

    @staticmethod
    def get_atoms_str_list(atomList):
        """
        Function that returns a list where each entry is a line of the
        _atom_site information which is corrently indented for writing into a
        new mmcif file

        It is not very efficient currently as all the data is iterated over
        twice; once to calculate the width of each column and again to assemble
        the output list

        Input: atomList from BioPy_Structure instance
        Output: atoms list of data in string format
        """

        atom_ljust = [0] * len(atomList[0].get_str_atom_vals())

        atoms = ['loop_']
        atoms_temp = []
        for tag in atomList[0].get_col_labels():
            atoms.append('_atom_site.' + tag)

        for atom in atomList:
            atom_lst = []
            atom_vals = atom.get_str_atom_vals()
            atom_ljust = mmcif_writer.get_atm_ljust(atom_ljust, atom_vals)
            atoms_temp.append(atom_vals)

        for atom_s in atoms_temp:
            atom_lst = []
            for n, entry in enumerate(atom_s):
                atom_lst.append(entry.ljust(atom_ljust[n] + 1))
            atom_str = ''.join(atom_lst)
            atoms.append(atom_str)

        return atoms

    @staticmethod
    def _find_longest_col_entry(column):
        """
        Finds the longest string entry in a column of data from a cif file

        Ignores entries with ';' as these are typically very long entries e.g.
        protein sequences
        """
        longest = 0

        for i in column:
            if i.startswith(';'):
                continue
            else:
                if len(i) > longest:
                    longest = len(i)
        return longest

    @staticmethod
    def get_table_str_list(title, table):
        """
        Reformat a gemmi table object so that each column is left justified and
        ready for writing into a new cif file
        """
        col_widths = []
        table_str_list = ['loop_']

        # likely to be expensive for long tables
        for n, key in enumerate(table.keys()):
            max_len = mmcif_writer._find_longest_col_entry(table[key])
            col_widths.append(max_len+1)
            table_str_list.append(title + key)

        # construct list taking into account long entries e.g. protein seqs
        for row in range(len(list(table.values())[0])):
            row_list = []
            found_long_line = False
            for n, key in enumerate(table.keys()):
                entry = table[key][row]

                if entry.startswith(';'):
                    if not found_long_line:
                        fixed_row = '\n' + entry + '\n'
                    else:
                        fixed_row = entry + '\n'
                    row_list.append(fixed_row)
                    found_long_line = True
                else:
                    found_long_line = False
                    row_list.append(entry.ljust(col_widths[n]))

            table_str_list.append(''.join(row_list))

        return table_str_list

    @staticmethod
    def get_pairs_str_list(title, pairs):
        """
        Reformat a gemmi pair object so that all entries are left justified
        with respect to the longest pair label
        """
        pair_str_list = []
        max_tag_len = len(max(pairs.keys(), key=len)) + len(title)

        for n, key in enumerate(pairs.keys()):
            entry = pairs[key][0]

            name = title + key
            if entry.startswith(';'):
                pair = [name.ljust(max_tag_len+3), '\n' + entry]
            else:
                pair = [name.ljust(max_tag_len+3), entry]
            pair_str = ''.join(pair)
            pair_str_list.append(pair_str)

        return pair_str_list

    @staticmethod
    def is_pair(table_or_pair):
        """
        Function that checks whether an gemmi category is a table or pair
        format
        """
        for key in table_or_pair.keys():
            if len(table_or_pair[key]) == 1:
                return True
            else:
                return False

    @staticmethod
    def get_global_score_pairs(global_scores):
        max_len = 0
        pairs_list = []
        prefix = '_TEMPy_global.'

        for label, value in global_scores:
            if len(label) > max_len:
                max_len = len(label)

        ljust_len = max_len + len(prefix) + 3

        for label, value in global_scores:
            pair_title = prefix + label
            pairs_list.append([pair_title.ljust(ljust_len) + str(value)])

        return pairs_list

    @staticmethod
    def write_tempy_localscores(file_ins, local_scores, score_labels):

        # if file_ins is not isinstance(file_ins): raise InputError
        file_ins.write('loop_\n')
        file_ins.write('_TEMPy_local_score.chain \n')
        file_ins.write('_TEMPy_local_score.label_seq_id \n')

        score_num = 0
        for label, i in score_labels.items():
            file_ins.write('_TEMPy_local_score.' + label + '\n')
            score_num += 1

        # find ljust width for each column
        chain_ljust = 0
        seqno_ljust = 0
        scores_ljust = [0] * score_num

        for chain_seqno, scores in local_scores.items():
            if len(chain_seqno[0]) > chain_ljust:
                chain_ljust = len(chain_seqno[0])

            if len(str(chain_seqno[1])) > seqno_ljust:
                seqno_ljust = len(str(chain_seqno[1]))

            for n, score in enumerate(scores):
                if len(str(score)) > scores_ljust[n]:
                    scores_ljust[n] = len(str(score))

        # write into file
        for chain_seqno, scores in local_scores.items():
            score_list = []
            for n, i in enumerate(scores):
                score_list.append(str(scores[n]).ljust(scores_ljust[n] + 1))
            scores_str = ''.join(score_list)

            file_ins.write(
                            chain_seqno[0].ljust(chain_ljust + 1) +
                            str(chain_seqno[1]).ljust(seqno_ljust + 1) +
                            scores_str
                            + '\n'
                            )

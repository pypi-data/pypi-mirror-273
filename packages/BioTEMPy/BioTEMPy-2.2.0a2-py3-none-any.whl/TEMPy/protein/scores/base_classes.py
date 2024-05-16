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

import numpy as np


class SlidingResidueWindow:
    def __init__(self, accumulator):
        self.accumulator = accumulator

    def scores(self, residue_atoms_list, size):
        self.accumulator.zero()

        half_window = int((size - 1) / 2)

        scores = []
        for head in range(0, len(residue_atoms_list) + half_window):
            tail = head - size

            # While the head is with in the allowed range, use all the voxels
            # associated with the residues atoms.
            if head < len(residue_atoms_list):
                for atom in residue_atoms_list[head]:
                    self.accumulator.add_atom(atom)

            # Drop the tail if it within the range of residues.
            if tail >= 0:
                for atom in residue_atoms_list[tail]:
                    self.accumulator.del_atom(atom)

            # Extract the SMOC score
            if head - half_window >= 0:
                scores.append(self.accumulator.get_val())

        return scores


class _AbstractSlidingScore:
    def __init__(self, struct, accumulator):
        mapping = {}
        for a in struct.atomList:
            if mapping.get(a.chain) is None:
                mapping[a.chain] = {}
            if mapping[a.chain].get(a.res_no) is None:
                mapping[a.chain][a.res_no] = []
            mapping[a.chain][a.res_no].append(a)
        self.mapping = mapping
        self.slider = SlidingResidueWindow(accumulator)

    def _get_contigs(self, chain):
        contigs = [[]]
        for res_num in self.mapping[chain]:
            last = contigs[-1]
            if len(last) == 0:
                last.append(res_num)
            else:
                if last[-1] + 1 == res_num:
                    last.append(res_num)
                else:
                    contigs.append([res_num])
        return contigs

    def score_chain_contig(self, chain, size):
        """Generate sliding window scores where windows do not span chain breaks."

        This method computes sliding windows over each contiguous region of the chain.

        Args:
           chain (str): The chain name to generate window scores.
           size (int): The size of the window. Should be an odd number.
        Returns:
           A dictionary mapping each residue to its score.
        """

        scores = {}

        res_mapping = self.mapping[chain]
        contigs = self._get_contigs(chain)

        for contig in contigs:
            residue_atoms_list = [res_mapping[r] for r in contig]
            contig_scores = self.slider.scores(residue_atoms_list, size)
            for k, v in zip(contig, contig_scores):
                scores[k] = v

        return scores

    def score_chain_span(self, chain, size):
        """Generate sliding window scores where windows do span chain breaks.

        This method ignores any breaks in the chain, so windows may include distant residues.

        Args:
           chain (str): The chain name to generate window scores.
           size (int): The size of the window. Should be an odd number.
        Returns:
           A dictionary mapping each residue to its score.
        """
        residue_mapping = self.mapping[chain]
        residue_atoms_list = list(residue_mapping.values())
        numbers = residue_mapping.keys()
        scores = self.slider.scores(residue_atoms_list, size)

        return {k: v for k, v in zip(numbers, scores)}


class _Accumulator:
    """An accumulator computes a score over a sliding window of atoms"""

    def add_atom(self, atom):
        pass

    def del_atom(self, atom):
        pass

    def get_val(self):
        pass

    def zero(self):
        pass


class _MOCAccumulator(_Accumulator):
    """Placeholder docstring"""

    def __init__(self, exp_map, sim_map, radius):
        from math import ceil, log, pow
        import voxcov as vc

        max_dim = max(exp_map.box_size())
        next_pow2 = int(pow(2, ceil(log(max_dim) / log(2))))
        self.radius = radius

        self.moc = vc.SMOC(
            exp_map.apix,
            exp_map.origin,
            next_pow2,
            [exp_map.x_size(), exp_map.y_size(), exp_map.z_size()],
            np.ascontiguousarray(exp_map.fullMap, dtype="float64"),
            np.ascontiguousarray(sim_map.fullMap, dtype="float64"),
        )

    def add_atom(self, atom):
        self.moc.add_sphere([atom.x, atom.y, atom.z], self.radius)

    def del_atom(self, atom):
        self.moc.del_sphere([atom.x, atom.y, atom.z], self.radius)

    def get_val(self):
        return self.moc.get_val()

    def zero(self):
        self.moc.zero()


class _MIAccumulator(_Accumulator):
    """Incremental calculation of MI score over voxels
    covered by atoms."""

    def __init__(self, exp_map, sim_map, radius, x_bins, y_bins):
        from math import ceil, log, pow
        import voxcov as vc

        max_dim = max(exp_map.box_size())
        next_pow2 = int(pow(2, ceil(log(max_dim) / log(2))))
        self.radius = 3
        self.exp_map = exp_map
        self.sim_map = sim_map

        self.mi = vc.SMI(
            exp_map.apix,
            exp_map.origin,
            next_pow2,
            [exp_map.x_size(), exp_map.y_size(), exp_map.z_size()],
            np.ascontiguousarray(sim_map.fullMap, dtype="float64"),
            np.ascontiguousarray(exp_map.fullMap, dtype="float64"),
            np.min(exp_map.fullMap),
            np.max(exp_map.fullMap),
            np.min(sim_map.fullMap),
            np.max(sim_map.fullMap),
            x_bins,
            y_bins,
        )

    def add_atom(self, atom):
        self.mi.add_sphere(
            [atom.x, atom.y, atom.z],
            self.radius,
        )

    def del_atom(self, atom):
        self.mi.del_sphere(
            [atom.x, atom.y, atom.z],
            self.radius,
        )

    # Not strictly essential, but I should add zeroing to DiffMap in voxcov.
    def zero(self):
        self.mi.zero()

    # Return current MI value
    def get_val(self):
        return self.mi.get_val()

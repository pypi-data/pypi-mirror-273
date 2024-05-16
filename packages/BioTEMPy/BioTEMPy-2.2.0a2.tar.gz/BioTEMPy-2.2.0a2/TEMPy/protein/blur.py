import voxcov as vc
from TEMPy.maps.em_map import Map


class StructureBlurrer:
    def blur_structure(self, structure, target_map):
        pass


class GlobalBlurrer(StructureBlurrer):
    """Blur structures to a global resolution."""

    def __init__(self, resolution, sigma_coeff=0.356, cutoff=3.0):
        self.resolution = resolution
        self.sigma_coeff = sigma_coeff
        self.cutoff = cutoff

    def blur_structure(self, structure, target_map) -> Map:
        blur = vc.BlurMap(
            target_map.apix,
            target_map.origin,
            [target_map.x_size(), target_map.y_size(), target_map.z_size()],
            self.cutoff,
        )
        for atom in structure.atomList:
            blur.add_gaussian(
                [atom.x, atom.y, atom.z],
                atom.get_mass() / self.resolution,
                self.sigma_coeff * self.resolution,
            )
        full_map = blur.to_numpy()
        em_map = Map(
            full_map,
            target_map.origin,
            target_map.apix,
            target_map.filename + "_simulated",
        )
        em_map._mut_normalise()
        return em_map


class LocResBlurrer(StructureBlurrer):
    """Blur structures according to the local resolution determined
    from a LocRes map."""

    def __init__(self, loc_res_map, sigma_coeff=0.356, cutoff=3.0):
        self.sigma_coeff = sigma_coeff
        self.cutoff = cutoff

    def blur_structure(self, structure, target_map):
        pass


class BfacBlurrer(StructureBlurrer):
    def __init__(self, sigma_coeff=0.356, cutoff=3.0):
        self.sigma_coeff = sigma_coeff
        self.cutoff = cutoff

    def blur_structure(self, structure, target_map):
        pass

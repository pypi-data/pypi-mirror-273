import argparse
import os
import urllib
import urllib.request
import tempfile
from TEMPy.protein.structure_parser import PDBParser, mmCIFParser
from TEMPy.maps.map_parser import MapParser


class Model:
    NUM_MODELS = 0
    DEFAULT_COLOURS = ["#3498db", "#28b463", "#f1c40f"]

    def __init__(self, data):
        self._data = data
        self._name = None
        self._color = None
        self._id = Model.NUM_MODELS
        Model.NUM_MODELS += 1

    def get_data(self):
        return self._data

    def get_name(self):
        if self._name is not None:
            return self._name
        return os.path.basename(self._data.filename).split(".")[0]

    def get_color(self):
        if self._color is not None:
            return self._color
        return Model.DEFAULT_COLOURS[self._id]

    def set_name(self, name):
        self._name = name

    def set_color(self, color):
        self._color = color


def parse_color(color_str):
    import string

    if len(color_str) > 6:
        if color_str[0] != "#":
            raise argparse.ArgumentTypeError(
                "Expected color to be of in hexdecimal format. E.g. #12ab34 or 12ab34"
            )
        color_str = color_str[1:]

    if len(color_str) != 6:
        raise argparse.ArgumentTypeError(
            "Expected color to have 6 hexadecimal digits. E.g. #12ab34 or 12ab34"
        )

    if not all(c in string.hexdigits for c in color_str):
        raise argparse.ArgumentTypeError(
            "Expected color to have 6 hexadecimal digits. E.g. #12ab34 or 12ab34"
        )
    return color_str


def parse_plot_unmodelled(action):
    action = action.lower()
    if action in ("band", "dash", "blank"):
        return action
    else:
        raise argparse.ArgumentTypeError("Expected one of: 'band', 'dash', 'blank'")


def parse_format(format):
    format = format.lower()
    if format in ("tsv", "csv", "json", "pdf", "png"):
        return format
    raise argparse.ArgumentTypeError(
        "Expected format to be one or more of: tsv, csv, json, pdf or png"
    )


def parse_plot_normalize(format):
    format = format.lower()
    if format in ("zscore"):
        return format
    raise argparse.ArgumentTypeError("Expected one of 'zscore'")


def parse_plot_type(format):
    format = format.lower()
    if format in ("residue", "violin"):
        return format
    raise argparse.ArgumentTypeError(
        "Expected format to be one or more of: residue, violin"
    )


def parse_plot_residue_range(residue_range):
    try:
        chain, residue_range = residue_range.split(":")
    except Exception:
        chain = None
    try:
        start, end = residue_range.split("-")
        start_int = int(start)
        end_int = int(end)
        return [chain, start_int, end_int]
    except Exception:
        raise argparse.ArgumentTypeError(
            "Expected residue range to be in the format START-END. E.g. 42-69"
        )


def parse_plot_span(span):
    try:
        chain, residue_range, color = span.split(":")
    except Exception:
        chain = None
    try:
        start, end = residue_range.split("-")
        start_int = int(start)
        end_int = int(end)
        color = parse_color(color)
        return [chain, start_int, end_int, color]
    except argparse.ArgumentTypeError as e:
        raise e
    except Exception as e:
        print(e)
        raise argparse.ArgumentTypeError(
            "Expected residue range to be in the format START-END:COLOR. E.g. 42-69:ff00ff"
        )


def _is_rcsb_link(path):
    return path.startswith("rcsb:")


def _is_emdb_link(path):
    return path.startswith("emdb:")


def _get_tempfile(filename):
    temp_dir = tempfile.gettempdir()
    return f"/{temp_dir}/{filename}"


def _read_from_rcsb(path):
    parts = path.split(":")
    if len(parts) == 2:
        _, pdb_id = parts
        local_file = _get_tempfile(f"rcsb_{pdb_id}.cif")
        if not os.path.isfile(local_file):
            url = f"http://www.rcsb.org/pdb/files/{pdb_id}.cif"
            print(f"Downloading {pdb_id} from RCSB")
            urllib.request.urlretrieve(url, filename=local_file)
    elif len(parts) == 3:
        _, pdb_id, version = parts

        local_file = _get_tempfile(f"rcsb_{pdb_id}_v{version}.cif.gz")
        if not os.path.isfile(local_file):
            print(f"Downloading {pdb_id} v{version} from RCSB")

            # RCSB publishes latest minor revision only. We just increment
            # until we find the file. We could be clever and FTP query later.
            max_minor = 10
            found_minor = True
            for minor in range(max_minor):
                url = f"https://ftp-versioned.rcsb.org/pdb_versioned/data/entries/{pdb_id[1:3]}/pdb_0000{pdb_id}/pdb_0000{pdb_id}_xyz_v{version}-{minor}.cif.gz"
                try:
                    urllib.request.urlretrieve(url, filename=local_file)
                    found_minor = True
                    break
                except Exception:
                    continue
            if not found_minor:
                raise Exception(
                    f"Couldn't find major version {version} of {pdb_id} on RCSB server"
                )

    return mmCIFParser.read_mmCIF_file(local_file)


def _read_from_emdb(path):
    emdb_id = path[5:]
    local_file = _get_tempfile(f"emdb_{emdb_id}.mrc.gz")
    if not os.path.isfile(local_file):
        url = f"https://ftp.ebi.ac.uk/pub/databases/emdb/structures/EMD-{emdb_id}/map/emd_{emdb_id}.map.gz"
        print(f"Downloading {emdb_id} from EMDB")
        urllib.request.urlretrieve(url, filename=local_file)

    return MapParser.readMRC(local_file)


def _read_half_map_from_emdb(path, half):
    emdb_id = path[5:]
    local_file = _get_tempfile(f"emdb_{emdb_id}_{half}.mrc.gz")
    if not os.path.isfile(local_file):
        url = f"https://ftp.ebi.ac.uk/pub/databases/emdb/structures/EMD-{emdb_id}/other/emd_{emdb_id}_half_map_{half}.map.gz"
        print(f"Downloading half_map {emdb_id}_{half} from EMDB")
        urllib.request.urlretrieve(url, filename=local_file)

    return MapParser.readMRC(local_file)


def parse_model(path):
    """Given a path or PDB accession tries to return a map.

    Args:
        path (str): A filename or PDB accession in the form of rcsb:1ake
    Returns:
        Map:
    Raise:
        argparse.ArgumentTypeError
    """
    if _is_rcsb_link(path):
        try:
            return _read_from_rcsb(path)
        except Exception as e:
            raise argparse.ArgumentTypeError(e)

    try:
        return PDBParser().read_PDB_file("test", path)
    except Exception:
        pass

    try:
        return mmCIFParser(path).read_mmCIF_file(path)
    except Exception:
        pass

    raise argparse.ArgumentTypeError(f"Failed to read model file: {path}")


def parse_map(path):
    """Given a path or EMDB accession tries to return a map.

    Args:
        path (str): A filename or EMDB accession in the form of emdb:1234
    Returns:
        Map:
    Raise:
        argparse.ArgumentTypeError
    """
    if _is_emdb_link(path):
        try:
            return _read_from_emdb(path)
        except Exception:
            raise argparse.ArgumentTypeError(f"Failed to get map with id: {path[5:]}")
    try:
        return MapParser.readMRC(path)
    except Exception:
        raise argparse.ArgumentTypeError(f"Failed to read map file: {path}")


def _parse_half_map(path, half):
    if _is_emdb_link(path):
        try:
            return _read_half_map_from_emdb(path, half)
        except Exception:
            raise argparse.ArgumentTypeError(f"Failed to get map with id: {path[5:]}")
    try:
        return MapParser.readMRC(path)
    except Exception:
        raise argparse.ArgumentTypeError(f"Failed to read map file: {path}")


def parse_half_map_1(path):
    return _parse_half_map(path, 1)


def parse_half_map_2(path):
    return _parse_half_map(path, 2)


class TEMPyArgParser:
    def __init__(self, script_name):
        self.parser = argparse.ArgumentParser(script_name)
        self.default_group = self.parser.add_argument_group("standard TEMPy arguments")
        self.args = None

    def parse_args(self):
        self.args = self.parser.parse_args()
        self.check_one_range_per_chain()
        return self.args

    def check_one_range_per_chain(self):
        seen = set()
        try:
            if self.args.plot_residue_range:
                for chain, start, end in self.args.plot_residue_range:
                    if chain in seen:
                        self.parser.error(
                            f"Only one range per chain can be specified. Chain {chain} has more than one range specified."
                        )
                    seen.add(chain)
        except:
            pass

    def get_models(self):
        if len(self.args.model_colors) > 0:
            if len(self.args.model_colors) != len(self.args.model):
                self.parser.error(
                    f"The number of models {len(self.args.model)} and colors {len(self.args.model_colors)} do not match"
                )

        if len(self.args.model_names) > 0:
            if len(self.args.model_names) != len(self.args.model):
                self.parser.error(
                    f"The number of models {len(self.args.model)} and names {len(self.args.model_names)} do not match"
                )

        models = [Model(m) for m in self.args.model]
        for model, color in zip(models, self.args.model_colors):
            model.set_color(color)

        for model, name in zip(models, self.args.model_names):
            model.set_name(name)

        return models

    def add_model_arg(self, multiple=False):
        self.model_group = self.parser.add_argument_group(
            "model", "Set additional model information"
        )
        if multiple:
            self.model_group.add_argument(
                "-p",
                "--models",
                help="A model file in PDB, CIF or mmCIF formats. Alternatively, the accession number eg. rcsb:1234",
                dest="model",
                required=True,
                nargs="+",
                type=parse_model,
            )
        else:
            self.model_group.add_argument(
                "-p",
                "--models",
                help="A model file in PDB, CIF or mmCIF formats. Alternatively, the accession number eg. rcsb:1234",
                dest="model",
                required=True,
                type=parse_model,
            )
        self.model_group.add_argument(
            "--model-colors",
            help="Color of the models for plotting",
            dest="model_colors",
            default=[],
            nargs="+",
            type=parse_color,
        )
        self.model_group.add_argument(
            "--model-names",
            help="Names of the models for plotting",
            dest="model_names",
            default=[],
            nargs="+",
        )

    def add_map_arg(self):
        self.default_group.add_argument(
            "-m",
            "--map",
            help="A EM file in MRC format. Alternatively, the accession number eg. emdb:1234",
            dest="map",
            required=True,
            type=parse_map,
        )

    def add_half_map_args(self, required=True):
        self.default_group.add_argument(
            "-hm1",
            "--half-map-1",
            help="A EM half map file in MRC format. Alternatively, the accession number eg. emdb:1234",
            dest="hmap1",
            required=required,
            type=parse_half_map_1,
        )

        self.default_group.add_argument(
            "-hm2",
            "--half-map-2",
            help="A EM half map file in MRC format. Alternatively, the accession number eg. emdb:1234",
            dest="hmap2",
            required=required,
            type=parse_half_map_2,
        )

    def add_resolution_arg(self):
        self.default_group.add_argument(
            "-r",
            "--resolution",
            dest="resolution",
            help="Estimated resolution of EM map",
            required=True,
            type=float,
        )

    def add_residue_output_writer(self):
        output_group = self.parser.add_argument_group("output")
        output_group.add_argument(
            "--output-format",
            dest="output_formats",
            help="Output format: CSV, TSV, JSON, PDF, PNG",
            nargs="+",
            required=True,
            default=["tsv"],
            type=parse_format,
        )

        output_group.add_argument(
            "--output-prefix",
            dest="output_prefix",
            help="Use a custom prefix for output files",
            required=False,
            default=None,
            type=str,
        )

        plot_group = self.parser.add_argument_group("plot")
        plot_group.add_argument(
            "--plot-type",
            dest="plot_types",
            help="Plot type: residue, violin",
            nargs="+",
            default=["residue"],
            type=parse_plot_type,
        )
        plot_group.add_argument(
            "--plot-residue-range",
            dest="plot_residue_range",
            help="Plot only the specified range",
            default=None,
            nargs="*",
            type=parse_plot_residue_range,
        )

        plot_group.add_argument(
            "--plot-normalize",
            dest="plot_normalize",
            help="Normalize the plot",
            default=None,
            type=parse_plot_normalize,
        )

        plot_group.add_argument(
            "--plot-bands",
            dest="plot_bands",
            help="Draw colored bands around ranges of residues. E.g. A:10-20:00ff00 A:70-110:ff0000",
            default=None,
            nargs="*",
            type=parse_plot_span,
        )
        plot_group.add_argument(
            "--plot-unmodelled",
            dest="plot_unmodelled",
            help="Draw colored bands around ranges of residues. E.g. A:10-20:00ff00 A:70-110:ff0000",
            default="blank",
            type=parse_plot_unmodelled,
        )

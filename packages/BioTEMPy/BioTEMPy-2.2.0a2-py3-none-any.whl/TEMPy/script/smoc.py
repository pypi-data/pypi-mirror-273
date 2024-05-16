"""
Example:
    To run SMOC on a model, `synthase.pdb`, and a map, `EMD-1234.mrc.gz`,
    with a window length of 11 and a resolution of 4.53 run::

        $ TEMPy.smoc -p synthase.pdb -m EMD-1234.mrc.gz -w 11 -r 4.53

    The default output of this command will be a series of files, one per
    chain, in tab separated format.  The files are named according to the
    parameters.  For examples, if synthase contains chains A, B and C, the
    following files are expected::

        smoc_EMD-1234_vs_synthase_chain-A_win-11_res-4p53_contig.tsv
        smoc_EMD-1234_vs_synthase_chain-B_win-11_res-4p53_contig.tsv
        smoc_EMD-1234_vs_synthase_chain-C_win-11_res-4p53_contig.tsv

    The output format can be changed using the '-f' flag which supports 'tsv',
    'csv' and 'json'.  For example, to select JSON output::

        $ TEMPy.smoc -p synthase.pdb -m EMD-1234.mrc.gz -w 11 -r 4.53 --output-format json

    This will result in a single JSON file with each chain stored under its own
    key.  The parameters used to generate the score are stored under the
    'parameters' key.  The output file name would be::

        smoc_EMD-1234_vs_synthase.json

    Two approaches to calculating sliding windows are provided, which handle
    unmodelled regions differently.  The new 'contig' based calculation creates
    sliding windows over contiguous residues.  The old method 'spans' these
    unmodelled regions.  The default method is the new 'contig' based approach,
    however this can be changed using the '--method' flag.
"""

import argparse
from TEMPy.cli.arg_parser import TEMPyArgParser
from TEMPy.protein.scoring_functions import FastSMOC
from TEMPy.script.output import ResidueWriter


def _parse_window(window):
    try:
        window = int(window)
    except Exception as exc:
        raise argparse.ArgumentTypeError("Expected an odd number") from exc

    if window % 2 == 0:
        raise argparse.ArgumentTypeError("Expected an odd number")

    return window


def _parse_method(method):
    method = method.lower()
    if method in ("span", "contig"):
        return method
    raise argparse.ArgumentTypeError("Expected method to be one of: span, contig")


parser = TEMPyArgParser("Calculate SMOC scores")
parser.add_map_arg()
parser.add_model_arg(multiple=True)
parser.add_resolution_arg()
parser.add_residue_output_writer()

smoc_group = parser.parser.add_argument_group("smoc", "SMOC specific parameters")

smoc_group.add_argument(
    "--smoc-window",
    dest="smoc_window",
    help="The window size. Should be odd.",
    default=11,
    type=_parse_window,
)
smoc_group.add_argument(
    "--smoc-method",
    dest="smoc_method",
    help="How to handle unmodelled regions",
    required=False,
    default="contig",
    type=_parse_method,
)


def get_parser():
    return parser.parser


class SMOCScript:
    def __init__(self):
        self.args = args = parser.parse_args()
        self.models = parser.get_models()
        self.map = args.map
        self.resolution = args.resolution
        self.window = args.smoc_window
        self.method = args.smoc_method

    def run(self):
        output = ResidueWriter(
            "SMOC",
            self.map,
            {"resolution": self.resolution, "window": self.window},
            self.args,
        )
        for model in self.models:
            scorer = FastSMOC(model.get_data(), self.map, self.resolution)
            chains = set(a.chain for a in model.get_data().atomList)

            chain_scores = {}
            for chain in chains:
                if self.method == "span":
                    chain_scores[chain] = scorer.score_chain_span(chain, self.window)
                else:
                    chain_scores[chain] = scorer.score_chain_contig(chain, self.window)

            output.add_model(model, chain_scores)
        output.write_output_formats()


def main():
    smoc = SMOCScript()
    try:
        smoc.run()
    except Exception as exc:
        raise exc


if __name__ == "__main__":
    main()

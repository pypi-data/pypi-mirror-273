"""
Example:
    To run LoQFit on a model, 7kx7.pdb - which is a PIWI protein from
    the organism *Ephydatia fluviatilis*. 7kx7 has a corresponding
    cryo EM map deposited in the EMDB at the ID 23061. We can grab
    these files from the online repositories and score the model
    with LoQFit by running::

        $ TEMPy.loqfit -p rcsb:7kx7 -m emdb:23061 -r 4.53

    The default output of this command will be a series of files, one per
    chain, in tab separated format.  The files are named according to the
    parameters.  For examples, as 7kx7 contains chains A and B, the
    following files are expected::

        loqfit_emdb_23061_vs_rcsb_7kx7_chainA.tsv
        loqfit_emdb_23061_vs_rcsb_7kx7_chainA.tsv

    As with the smoc script, the output format can be changed using the
    '-f' flag which supports 'tsv', 'csv' and 'json'.  For example,
    to select JSON output::

        $ TEMPy.loqfit -p rcsb:7kx7 -m emdb:23061 -r 4.53 --output-format json

    This will result in a single JSON file with each chain stored under its own
    key. The parameters used to generate the score are stored under the
    'parameters' key.  The output file name would be::

        loqfit_emdb_23061_vs_rcsb_7kx7.json

    The script will also write out a plot of the LoQFit score for each chain
    in the model. These can be saved as either vector graphics '.svg' files
    or as png images by changing the '--output-format' flag. E.g. to save the
    LoQFit plots for the synthase example as png files, run::

        $ TEMPy.loqfit -p rcsb:7kx7 -m emdb:23061 -r 4.53 --output-format png

    This produces this plot for chain A:

    .. figure:: _static/images/loqfit-chainA.png
        :scale: 75%
        :align: center

    And this (slightly silly) plot for chain B, which has just a few modelled
    residues:

    .. figure:: _static/images/loqfit-chainB.png
        :scale: 75%
        :align: center

    Finally, the LoQFit score can be normalised using the local resolution
    of the EM-map. TEMPy needs the half-maps to calculate the local resolution
    and these can be supplied with the '-hm1' and '-hm2' flags.
    If both half maps are supplied, the normalised LoQFit score is
    automatically calculated. We can get the half-maps from the EMDB, assuming
    they are deposited. So, to calculate the normalised LoQFit we can run::

        $ TEMPy.loqfit -p rcsb:7kx7 -m emdb:23061 -r 4.53 --output-format png -hm1 emdb:23061 -hm2 emdb:23061

    Which gives us this plot for chain A:

    .. image:: _static/images/normalised-loqfit-chainA.png
        :scale: 75%
        :align: center

"""

from TEMPy.protein.scoring_functions import ScoringFunctions
from TEMPy.cli import arg_parser
from TEMPy.script.output import ResidueWriter


def get_parser():
    return parser.parser


parser = arg_parser.TEMPyArgParser("Calculate LoQFit scores")
parser.add_map_arg()
parser.add_model_arg(multiple=True)
parser.add_resolution_arg()
parser.add_half_map_args(required=False)
parser.add_residue_output_writer()

loqfit_group = parser.parser.add_argument_group("LoQFit")
loqfit_group.add_argument(
    "--max-loqfit-score",
    required=False,
    type=float,
    default=18.0,
    help="Maximum LoQFit value to be plotted",
)


class LoQFitScript:
    def __init__(self):
        self.args = args = parser.parse_args()
        self.models = parser.get_models()
        self.map = args.map
        self.resolution = args.resolution
        self.max_resolution = args.max_loqfit_score
        self.half_map1 = args.hmap1
        self.half_map2 = args.hmap2

        if self.half_map1 is not None and self.half_map2 is not None:
            self.method = "normalised-LoQFit"
        else:
            self.method = "LoQFit"

    def run(self):
        output = ResidueWriter(
            "LoqFit",
            self.map,
            {
                "resolution": self.resolution,
                "max resolution": self.max_resolution,
                "method": self.method,
            },
            self.args,
        )

        for model in self.models:
            scorer = ScoringFunctions()
            loqfit_score = scorer.LoQFit(
                model.get_data(),
                self.map,
                self.resolution,
                max_res=self.max_resolution,
                half_map_1=self.half_map1,
                half_map_2=self.half_map2,
            )

            chain_scores = self.split_scores_by_chain(loqfit_score)
            output.add_model(model, chain_scores)
        output.write_output_formats()

    def split_scores_by_chain(self, loqfit_scores):
        loqfit_by_chain = {}

        for ((chain, res_no), score) in loqfit_scores.items():
            try:
                loqfit_by_chain[chain][res_no] = score
            except KeyError:
                loqfit_by_chain[chain] = {res_no: score}

        return loqfit_by_chain


def main():
    loqfit = LoQFitScript()
    try:
        loqfit.run()
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()

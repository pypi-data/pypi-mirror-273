from TEMPy.protein.scores.local import SlidingMI
from TEMPy.protein.blur import GlobalBlurrer
from TEMPy.cli import arg_parser
from TEMPy.script.output import ResidueWriter
import time


def get_parser():
    return parser.parser


parser = arg_parser.TEMPyArgParser("Calculate SMI scores")
parser.add_map_arg()
parser.add_model_arg(multiple=True)
parser.add_resolution_arg()
parser.add_residue_output_writer()

loqfit_group = parser.parser.add_argument_group("SMI")
loqfit_group.add_argument(
    "--bins1",
    required=False,
    type=int,
    default=20,
    help="Number of bins for experimental map",
)
loqfit_group.add_argument(
    "--bins2",
    required=False,
    type=int,
    default=20,
    help="Number of bins for simulated map",
)

loqfit_group.add_argument(
    "--mi-window",
    required=False,
    dest="mi_window",
    type=int,
    default=11,
    help="window length",
)


class MI_Script:
    def __init__(self):
        self.args = args = parser.parse_args()

        self.models = parser.get_models()
        self.map = args.map
        self.resolution = args.resolution
        self.output_prefix = args.output_prefix
        self.output_formats = args.output_formats
        self.plot_types = args.plot_types
        self.bins1 = args.bins1
        self.bins2 = args.bins2
        # windowing related options
        self.window = args.mi_window
        self.method = "contig"

    def run(self):
        output = ResidueWriter(
            "MI",
            self.map,
            {"resolution": self.resolution, "window": self.window},
            self.args,
        )
        for model in self.models:
            chain_scores = self.run_model(model.get_data())
            output.add_model(model, chain_scores)
        output.write_output_formats()

    def run_model(self, model):
        blurrer = GlobalBlurrer(self.resolution)
        smi = SlidingMI(model, self.map, blurrer, self.resolution)
        chains = set(a.chain for a in model.atomList)
        chain_scores = {}
        for chain in chains:
            start = time.time()
            if self.method == "span":
                chain_scores[chain] = smi.score_chain_span(chain, self.window)
            else:
                chain_scores[chain] = smi.score_chain_contig(chain, self.window)
            print(f"Elapsed for chain {chain}: {time.time() - start}")
        return chain_scores


def main():
    loqfit = MI_Script()
    try:
        loqfit.run()
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()

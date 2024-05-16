import os
import csv
import argparse
from TEMPy.cli.arg_parser import TEMPyArgParser
from TEMPy.protein.scoring_functions import FastSCCC


def write_tabular_scores(filename, chain_scores, delimiter):
    with open(filename, "w") as tabular_file:
        tabular_writer = csv.writer(tabular_file, delimiter=delimiter)
        for k, v in sorted(chain_scores.items()):
            tabular_writer.writerow([k, v])


def parse_format(format):
    format = format.lower()
    if format in ("tsv", "csv"):
        return format
    raise argparse.ArgumentTypeError("Expected format to be one of: tsv, csv")


parser = TEMPyArgParser("Calculate SCCC scores")
parser.add_map_arg()
parser.add_model_arg()
parser.add_resolution_arg()

output_group = parser.parser.add_argument_group("output")

output_group.add_argument(
    "--output-format",
    dest="output_format",
    help="Output format: CSV, TSV",
    required=True,
    default="tsv",
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


def get_parser():
    return parser.parser


class SCCCScript:
    def __init__(self):
        args = parser.parse_args()
        self.model = args.model
        self.map = args.map
        self.resolution = args.resolution
        self.prefix = args.output_prefix
        self.output_format = args.output_format

    def run(self):
        chains = set(a.chain for a in self.model.atomList)
        sccc = FastSCCC(self.model, self.map, self.resolution)

        chain_scores = {}
        for chain in chains:
            score = sccc.score_segment(self.model.get_chain(chain))
            print("Chain:", chain, score)
            chain_scores[chain] = score

        if self.prefix is not None:
            prefix = self.prefix
        else:
            prefix = "sccc_{}_vs_{}".format(
                os.path.basename(self.map.filename).split(".")[0],
                os.path.basename(self.model.filename).split(".")[0],
            )

        if self.output_format in ("tsv", "csv"):
            filename = "{}_res-{}.{}".format(
                prefix,
                str(self.resolution).replace(".", "p"),
                self.output_format,
            )
            print("Writing scores for chains to file {}".format(filename))
            delimiter = "\t"
            if self.output_format == "csv":
                delimiter = ","
                write_tabular_scores(filename, chain_scores, delimiter)


def main():
    sccc = SCCCScript()
    try:
        sccc.run()
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()

import numpy as np

from TEMPy.protein.scoring_functions import ScoringFunctions
from TEMPy.cli import arg_parser
import csv
from TEMPy.protein.structure_blurrer import StructureBlurrer
import os
import argparse
import warnings


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


def get_parser():
    return parser.parser


parser = arg_parser.TEMPyArgParser("Calculate global scores")
parser.add_map_arg()
parser.add_model_arg()  # multiple=True)
parser.add_resolution_arg()

globscore_group = parser.parser.add_argument_group("global score options")
globscore_group.add_argument(
    "--contour-level",
    required=False,
    type=float,
    default=None,
    dest="contour_level",
    help="Threshold level to contour the map",
)

output_group = parser.parser.add_argument_group("output options")

output_group.add_argument(
    "--output-format",
    dest="output_format",
    help="Output format: CSV, TSV",
    required=False,
    default="csv",
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


class GlobscoreScript:
    def __init__(self):
        args = parser.parser.parse_args()

        self.models = [args.model]  # parser.get_models()
        self.map = args.map
        self.mapname = os.path.splitext(os.path.basename(args.map.filename))[0]
        self.resolution = args.resolution
        self.contour = args.contour_level
        self.output_prefix = args.output_prefix
        self.output_format = args.output_format
        self.prefix = args.output_prefix
        self.blurrer = StructureBlurrer(with_vc=True)
        self.scorer = ScoringFunctions()
        self.model_scores = {}

    def validate_args(self):
        assert os.path.isfile(self.map)
        for model in self.models:
            assert os.path.isfile(model)

    def run(self):
        for model in self.models:
            self.run_model(model)

    def run_model(self, model):
        # Compute a simulated model.
        sim_map = self.blurrer.gaussian_blur_real_space(
            model, self.resolution, densMap=self.map, sigma_coeff=0.225
        )
        self.model_scores["ccc"] = round(
            self.scorer.CCC(self.map, sim_map), 3
        )
        self.model_scores["mi"] = round(
            self.scorer.MI(self.map, sim_map), 3
        )

        if self.contour is not None:
            self.calculate_contour_scores(sim_map, model)

        if self.prefix is not None:
            prefix = self.prefix
        else:
            prefix = "globscores_{}_vs_{}".format(
                self.mapname,
                os.path.splitext(os.path.basename(model.filename))[0],
            )

        if self.output_format in ("tsv", "csv"):
            filename = "{}.{}".format(
                prefix,
                self.output_format,
            )
            print("Writing scores to file {}".format(filename))
            delimiter = "\t"
            if self.output_format == "csv":
                delimiter = ","
            write_tabular_scores(filename, self.model_scores, delimiter)

    def calculate_contour_scores(self, sim_map, model):
        # use a model contour of 0.0 to maximise overlap
        model_contour = self.model_contour(
            sim_map, t=round(0.225 * self.resolution * 0.1, 1)
        )
        # overlap
        overlap_scores = self.scorer.calculate_overlap_scores(
            map_target=self.map,
            map_probe=sim_map,
            map_target_threshold=self.contour,
            map_probe_threshold=model_contour,
        )
        if (
            overlap_scores[1] < 0.1
            or np.isnan(overlap_scores[0])
            or np.isnan(overlap_scores[1])
        ):
            warnings.warn(
                f"Map {self.map.filename} and model {model.filename} do not overlap, "
                f"stopping overlap score calculation.",
                category=RuntimeWarning,
            )
            return
        # store model overlap fraction
        self.model_scores["overlap"] = round(overlap_scores[1], 3)
        # ccc for contoured maps
        ccc_contoured, ovr = self.scorer.CCC_map(
            map_target=self.map,
            map_probe=sim_map,
            map_target_threshold=self.contour,
            map_probe_threshold=model_contour,
            mode=2,
            meanDist=True,
        )
        self.model_scores["ccc_contour"] = round(ccc_contoured, 3)
        # ccc within overlap mask
        ccc_mask, ovr = self.scorer.CCC_map(
            map_target=self.map,
            map_probe=sim_map,
            map_target_threshold=self.contour,
            map_probe_threshold=model_contour,
            mode=3,
            meanDist=True,
        )
        self.model_scores["ccc_mask"] = round(ccc_mask, 3)
        # MI within overlap mask
        mi_mask = self.scorer.MI(
            map_target=self.map,
            map_probe=sim_map,
            map_target_threshold=self.contour,
            map_probe_threshold=model_contour,
            mode=3,
        )
        self.model_scores["mi_mask"] = round(mi_mask, 3)

    # calculate model contour
    def model_contour(self, sim_map, t=-1.0):
        c2 = 0.0
        if t != -1.0:
            c2 = t * sim_map.std()
        return c2


def main():
    gs = GlobscoreScript()
    gs.run()


if __name__ == "__main__":
    main()

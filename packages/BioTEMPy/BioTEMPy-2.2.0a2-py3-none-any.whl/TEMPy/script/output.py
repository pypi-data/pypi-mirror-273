import os
import csv
import json
import matplotlib.pyplot as plt
import scipy.stats

# Returns two lists containing the contigs and breaks
def split(residue_scores):
    residue_numbers = list(residue_scores.keys())
    residue_numbers.sort()
    prev_number = end_number = residue_numbers[0]
    contigs = []
    breaks = []
    for residue_number in residue_numbers[1:]:
        if residue_number == end_number + 1:
            end_number = residue_number
        else:
            breaks.append((end_number, residue_number))
            contigs.append((prev_number, end_number))
            prev_number = residue_number
            end_number = residue_number
    contigs.append((prev_number, end_number))
    return contigs, breaks


class ResiduePlot:
    def __init__(
        self,
        chain,
        score_name,
        title,
        params,
        normalize_score=None,
        residue_range=None,
        spans=None,
        plot_unmodelled="blank",
    ):
        self.chain = chain
        self.break_color = "#aaaaaa"

        self.figure, self.axis = plt.subplots()
        self.axis.set_xlabel(f"Chain {self.chain} residues")
        self.axis.set_ylabel(score_name)
        self.score_name = score_name
        self.figure.suptitle(title)
        if params is not None:
            self.axis.set_title(params)
        self.has_breaks = False
        self.models = []
        self.normalize_score = normalize_score
        self.spans = spans
        self.plot_unmodelled = plot_unmodelled
        self.residue_range = None
        if residue_range:
            for chain, start, end in residue_range:
                if chain == self.chain:
                    self.residue_range = [start, end]
                    break

    def add_contig(self, model, start, end, scores):
        residues = list(range(start, end + 1))
        scores = [scores[r] for r in residues]
        color = model.get_color()
        self.axis.plot(residues, scores, color=color, linewidth=1)

    def add_span(self, start, end, color):
        rect = self.axis.axvspan(start, end)
        rect.set_color(color)

    def add_break(self, start, end):
        self.add_span(start, end, self.break_color)

    def apply_normalisation(self, residue_scores):
        scores = list(residue_scores.values())
        residues = list(residue_scores.keys())
        if self.normalize_score == "zscore":
            scores = scipy.stats.zscore(scores)

        residue_scores = {}
        for residue, score in zip(residues, scores):
            residue_scores[residue] = score
        return residue_scores

    def plot(self, model, residue_scores):
        self.models.append(model)
        residue_scores = self.apply_normalisation(residue_scores)

        contigs, breaks = split(residue_scores)

        if self.plot_unmodelled == "band":
            for start, end in breaks:
                self.has_breaks = True
                self.add_break(start, end)

        if self.plot_unmodelled == "dash":
            for start, end in breaks:
                self.axis.plot(
                    [start, end],
                    [residue_scores[start], residue_scores[end]],
                    color=model.get_color(),
                    linestyle="--",
                )

        if self.spans is not None:
            for chain, start, end, color in self.spans:
                if chain == self.chain:
                    self.add_span(start, end, color)

        for start, end in contigs:
            self.add_contig(model, start, end, residue_scores)

    def write(self, filename):
        labels = [m.get_name() for m in self.models]
        colors = [m.get_color() for m in self.models]
        if self.has_breaks:
            labels += ["Unmodelled"]
            colors += [self.break_color]
        # Color the legend text
        leg = self.axis.legend(labels, labelcolor=colors)
        # Color the little blocks next to legend text
        for plot_id, model in enumerate(self.models):
            leg.legendHandles[plot_id].set_color(model.get_color())
        if self.has_breaks:
            leg.legendHandles[plot_id + 1].set_color(self.break_color)

        if self.residue_range is not None:
            self.axis.set_xlim(self.residue_range[0], self.residue_range[1])
        self.figure.savefig(filename)
        plt.close()


class ViolinPlot:
    def __init__(self, score_name, title, params):
        self.figure, self.axis = plt.subplots()
        self.axis.set_xlabel("Chain")
        self.axis.set_ylabel(f"{score_name} distribution")
        self.score_name = score_name
        self.figure.suptitle(title)
        if params is not None:
            self.axis.set_title(params)
        self.data = []
        self.models = []
        self.all_models = []
        self.chains = []
        self.all_chains = []

    def plot(self, model, chain_name, residue_scores):
        if model not in self.models:
            self.models.append(model)
        self.all_models.append(model)
        if chain_name not in self.chains:
            self.chains.append(chain_name)
        self.data.append(list(residue_scores.values()))

    def write(self, filename):
        p = self.axis.violinplot(self.data, range(1, len(self.data) + 1))
        for model, violin in zip(self.all_models, p["bodies"]):
            violin.set_facecolor(model.get_color())
        # The position of first chain label. Should be between the
        # violins of the models.
        chain_start_xtick = (len(self.models) + 1) * 0.5
        chain_ticks = [
            chain_start_xtick + (len(self.models) * t)
            for t in range(0, len(self.chains))
        ]
        self.axis.set_xticks(chain_ticks, labels=list(self.chains))

        leg = self.axis.legend(
            [m.get_name() for m in self.models],
            labelcolor=[m.get_color() for m in self.models],
        )
        for idx, model in enumerate(self.models):
            leg.legendHandles[idx].set_color(model.get_color())

        self.figure.savefig(filename)
        plt.close()


class ResidueWriter:
    OUTPUT_FORMATS = ("csv", "tsv", "json", "png", "pdf")

    def __init__(self, method, map, params, cli_args):
        self.cli_args = cli_args
        self.method = method
        self.prefix = cli_args.output_prefix
        self.map_name = os.path.basename(map.filename).split(".")[0]
        self.params = params
        self.plot_types = cli_args.plot_types
        self.models = []
        self.chain_scores = []
        self.output_formats = cli_args.output_formats

    def add_model(self, model, chain_scores):
        self.models.append(model)
        self.chain_scores.append(chain_scores)

    def get_plot_title(self):
        if len(self.models) == 1:
            model_name = self.models[0].get_name()
            return f"{model_name} vs. {self.map_name}"
        return f"Multi vs. {self.map_name}"

    def get_plot_params(self):
        if len(self.params) == 0:
            return None
        params = []
        for param in self.params:
            params.append(f"{param}: {self.params[param]}")
        return ", ".join(params)

    def chain_filename(self, model_name, chain, output_format):
        if self.prefix:
            return f"{self.prefix}_chain-{chain}.{output_format}"
        return f"{self.method}_{model_name}_vs_{self.map_name}_chain-{chain}.{output_format}"

    def chain_filename_multi(self, chain, output_format):
        if self.prefix:
            return f"{self.prefix}_chain-{chain}.{output_format}"
        return f"{self.method}_multi_vs_{self.map_name}_chain-{chain}.{output_format}"

    def violin_filename(self, model_name, output_format):
        if self.prefix:
            return f"{self.prefix}.{output_format}"
        return f"{self.method}_{model_name}_vs_{self.map_name}.{output_format}"

    def violin_filename_multi(self, output_format):
        if self.prefix:
            return f"{self.prefix}.{output_format}"
        return f"{self.method}_multi_vs_{self.map_name}.{output_format}"

    def filename(self, model_name, output_format):
        if self.prefix:
            return f"{self.prefix}.{output_format}"
        return f"{self.method}_{model_name}_vs_{self.map_name}.{output_format}"

    def write_output_format(self, output_format):
        if output_format == "json":
            self.write_json(output_format)
        if output_format == "tsv":
            self.write_table(output_format)
        if output_format == "csv":
            self.write_table(output_format)
        if output_format in ("png", "pdf"):
            self.write_plot(output_format)

    def write_output_formats(self):
        for output_format in self.output_formats:
            self.write_output_format(output_format)

    def write_json(self, output_format):
        print("JSON writer")
        for model, chain_scores in zip(self.models, self.chain_scores):
            filename = self.filename(model.get_name(), output_format)
            print(f"   Writing: {filename}")
            with open(filename, "w") as outfile:
                json.dump(
                    {"chains": chain_scores, "parameters": self.params},
                    outfile,
                    indent=4,
                )

    def write_table(self, output_format):
        print(f"Table writer ({output_format})")
        delimiter = ","
        if output_format == "tsv":
            delimiter = "\t"
        for model, chain_scores in zip(self.models, self.chain_scores):
            for chain in chain_scores:
                filename = self.chain_filename(model.get_name(), chain, output_format)
                print(f"   Writing: {filename}")
                residue_scores = chain_scores[chain]
                with open(filename, "w") as tabular_file:
                    tabular_writer = csv.writer(tabular_file, delimiter=delimiter)
                    for (residue_number, score) in residue_scores.items():
                        tabular_writer.writerow([residue_number, score])

    def write_plot(self, output_format):
        for plot_type in self.plot_types:
            if plot_type == "residue":
                self.write_residue_plot(output_format)
            else:
                self.write_violin_plot(output_format)

    def write_violin_plot(self, output_format):
        print("Violin plot")
        plot = ViolinPlot(self.method, self.get_plot_title(), self.get_plot_params())
        chains = list(
            set(chain for chain_scores in self.chain_scores for chain in chain_scores)
        )
        chains.sort()
        for chain in chains:
            for model, chain_scores in zip(self.models, self.chain_scores):
                plot.plot(model, chain, chain_scores[chain])
        if len(self.models) == 1:
            filename = self.violin_filename(self.models[0].get_name(), output_format)
        else:
            filename = self.violin_filename_multi(output_format)
        print(f"   Writing: {filename}")
        plot.write(filename)

    def write_residue_plot(self, output_format):
        print("Residue plot")
        chains = set(
            chain for chain_scores in self.chain_scores for chain in chain_scores
        )
        for chain in chains:
            filename = self.chain_filename_multi(chain, output_format)
            print(f"   Writing: {filename}")

            plot = ResiduePlot(
                chain,
                self.method,
                self.get_plot_title(),
                self.get_plot_params(),
                residue_range=self.cli_args.plot_residue_range,
                normalize_score=self.cli_args.plot_normalize,
                spans=self.cli_args.plot_bands,
                plot_unmodelled=self.cli_args.plot_unmodelled,
            )
            for model, chain_scores in zip(self.models, self.chain_scores):
                print("adding:", model.get_name())
                plot.plot(model, chain_scores[chain])
            plot.write(filename)

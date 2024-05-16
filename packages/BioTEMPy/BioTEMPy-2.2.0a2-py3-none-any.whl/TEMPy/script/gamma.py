# ===============================================================================
#     This file is part of TEMPy.
#
#     TEMPy is a software designed to help the user in the manipulation
#     and analyses of macromolecular assemblies using 3D electron microscopy maps.
#
#     Copyright 2010-2014 TEMPy Inventors and Birkbeck College University of London.
#                          The TEMPy Inventors are: Maya Topf, Daven Vasishtan,
#                           Arun Prasad Pandurangan, Irene Farabella, Agnel-Praveen Joseph,
#                          Harpal Sahota
#
#
#     TEMPy is available under Public Licence.
#
#     Please cite your use of TEMPy in published work:
#
#     Vasishtan D, Topf M. (2011) J Struct Biol 174:333-343. Scoring functions for cryoEM density fitting.
#     Pandurangan AP, Vasishtan D, Topf M. (2015) Structure 23:2365-2376. GAMMA-TEMPy: Simultaneous fitting of components in 3D-EM Maps of their assembly using genetic algorithm.
# ===============================================================================

import os
from TEMPy.protein.structure_parser import PDBParser
from TEMPy.assembly.gamma import GA
from TEMPy.math.vq import get_VQ_points
from TEMPy.cli.arg_parser import TEMPyArgParser
import time


def get_output_directory_name(protein_id, input_model_path):
    path_list = input_model_path.split("/")
    dir = ""
    for i in range(len(path_list) - 1):
        dir = dir + path_list[i] + "/"

    if dir == "":
        list_dir = "."
    else:
        list_dir = dir

    directory_content = os.listdir(list_dir)
    gtempy_dirs = []
    for file in directory_content:
        full_path = list_dir + file
        if os.path.isdir(full_path) and file.startswith("gamma_tempy"):
            gtempy_dirs.append(file)

    file_num = len(gtempy_dirs) + 1

    output_directory_path = (
        dir + "gamma_tempy_" + protein_id + "_run" + str(file_num).zfill(3) + "/"
    )

    return output_directory_path


def get_parser():
    parser = TEMPyArgParser("gamma-TEMPy")
    parser.add_model_arg()
    parser.add_map_arg()
    parser.add_resolution_arg()

    gamma = parser.parser.add_argument_group("gamma")
    output = parser.parser.add_argument_group("output")

    gamma.add_argument(
        "--gamma-pop-size",
        type=int,
        default=160,
        dest="pop_size",
        help="Number population members in each generation (default = 160)",
    )

    gamma.add_argument(
        "--gamma-num-gens",
        type=int,
        default=100,
        dest="num_gens",
        help="Number of generations in the GA (default = 100)",
    )

    gamma.add_argument(
        "--gamma-num-gas",
        type=int,
        default=1,
        dest="num_gas",
        help="Number of GA solutions to generate (default = 1)",
    )

    gamma.add_argument(
        "--gamma-gof",
        type=int,
        default=1,
        dest="gof",
        help="Goodness-of-fit score to use. (1) - Mutual information score, "
        "(2) - CCC (default = MI score)",
    )

    gamma.add_argument(
        "--gamma-num-cpus",
        type=int,
        default=1,
        dest="num_cpus",
        help="Number of CPUs to use (default = 1)",
    )

    output.add_argument(
        "--output-dir",
        required=True,
        dest="output_dir",
        help="Name of the output directory to store results - default is to "
        "create a new folder in the directory of the input map",
    )

    output.add_argument(
        "--output-file",
        required=True,
        dest="output_file",
        help="Prefix name of the predicted fits (default is set to the name "
        "of the input PDB file name)",
    )

    output.add_argument(
        "--output-pdbsnap",
        action="store_true",
        dest="pdbsnap",
        help="Write all the members (PDB fits) in every GA population for "
        "every generation. By default this option is off.",
    )

    gamma.add_argument(
        "--gamma-seed-file",
        metavar="/path/to/seedpoints_file",
        dest="seed_file",
        help="Supply a PDB formated file containing the coordinate to use as "
        "initial VQ points (By default the VQ points will be "
        "generated from the input density map)",
    )

    gamma.add_argument(
        "--gamma-mut-rate",
        type=float,
        default=0.02,
        dest="mut_rate",
        help="Mutation rate (default = 0.02). This is a advanced setting "
        "for expert user",
    )

    gamma.add_argument(
        "--gamma-xover-rate",
        type=float,
        default=0.8,
        dest="xover_rate",
        help="Crossover rate (default = 0.8). This is a advanced setting "
        "for expert user",
    )

    gamma.add_argument(
        "--gamma-offset-mag",
        type=float,
        default=0.0,
        dest="offset_mag",
        help="Magnitude of the displacement used while applying transational "
        "mutation (default set 0.0 will calculate moffset value from "
        "the VQ point distances). This is a advanced setting "
        "for expert user",
    )

    return parser.parser


def main():
    args = get_parser().parse_args()

    prot = args.model
    nchains = prot.no_of_chains()

    emmap = args.map
    emmap.normalise()
    res = args.resolution

    ga = GA()
    total_popsize = args.pop_size
    ngen = args.num_gens
    grun = args.num_gas
    selection_method = (
        1  # Hardcoded param: set selection method; 1=Tournament selection
    )
    gof = args.gof
    w_gof = nchains  # Weight for CCC/MI equals number of chains in model
    w_clash = 0.2  # Hardcoded param: set the weight for clash score
    mrate = args.mut_rate
    crate = args.xover_rate
    moffset = args.offset_mag
    ncpu = args.num_cpus

    output_dir = args.output_dir
    output_filename = args.output_file

    # check if output directory exists and flag a warning if it does
    if os.path.isdir(output_dir):
        print(
            "WARNING: Output directory %s already exists - files in this "
            "directory will potentially be overwritten" % (output_dir)
        )
        overwrite = input("Is it okay to continue? (y/n)\n")
        if overwrite == "y" or overwrite == "yes" or overwrite == "Y":
            pass
        else:
            output_dir = get_output_directory_name(prot.pdb_id, args.ipdb)
            os.mkdir(output_dir)
            print("Generated new directory %s for output files." % (output_dir))
    else:
        os.mkdir(output_dir)
        print("Files will be written into %s" % (output_dir))

    output_name = output_dir + "/" + output_filename

    # Make a directory for intermediate models if needed
    if args.pdbsnap:
        pdb_snapshot_dir = output_dir + "_snapshot"
        pdb_snapshot_file = output_filename

        if not os.path.isdir(pdb_snapshot_dir):
            os.mkdir(pdb_snapshot_dir)
            print(
                "The top scoring model at each generation will be saved as a "
                " PDB file in %s" % (pdb_snapshot_dir)
            )
            pdb_snapshot_name = pdb_snapshot_dir + "/" + pdb_snapshot_file
    else:
        pdb_snapshot_name = "dummy"

    # get VQ points
    if not args.seed_file:
        print("Calculating VQ seed points from EM map file: %s" % (args.map))
        vq_vec_list = get_VQ_points(
            emmap, emmap.std() * 2, nchains, 50, output_name, False
        )
    else:
        vq_struct = PDBParser.read_PDB_file("vq", args.seed_file)
        vq_vec_list = vq_struct.get_vector_list()
        if len(vq_vec_list) < nchains:
            raise RuntimeError(
                "There are only %i VQ points in the seedpoints file "
                "(%s), compared to %i chains in the input protein model (%s). "
                "\nThe number of VQ points must equal the number of chains in"
                " the protein model!"
                % (
                    len(vq_vec_list),
                    args.seed_file,
                    nchains,
                    args.ipdb,
                )
            )

        # Initialise log file
    f = open(output_name + ".log", "w")
    start_time = time.time()
    f.write("Start time : " + str(start_time) + "\n")
    f.write(
        "------------------------------------------------------------------------------------------\n"
    )
    f.write("GAMMA-TEMPy\n")
    f.write("Genetic Algorithm for Modelling Macromolecular Assemblies\n")
    f.write(
        "------------------------------------------------------------------------------------------\n"
    )
    f.write("Input assembly                : " + str(prot.filename) + "\n")
    f.write("Input map                     : " + str(emmap.filename) + "\n")
    f.write("Resolution (angstrom)         : " + str(args.resolution) + "\n")
    f.write("Population size               : " + str(total_popsize) + "\n")
    f.write("Number of GA Generations      : " + str(ngen) + "\n")
    f.write("Number of GA runs             : " + str(grun) + "\n")
    f.write("Mutation rate                 : " + str(mrate) + "\n")
    f.write("Crossover rate                : " + str(crate) + "\n")
    f.write("Mutation ofset                : " + str(moffset) + "\n")
    if gof == 1:
        f.write("Goodness-of-fit score         : Mutual Information\n")
    else:
        f.write("Goodness-of-fit score         : Cross Correlation Coefficient\n")
        f.write("Prefix of the output filename : " + output_filename + "\n")
    if args.pdbsnap:
        f.write(
            "Output assembly model after every generation : Yes ("
            + pdb_snapshot_name
            + ")\n"
        )
    else:
        f.write("Output assembly model after every generation : No\n")

    if not args.seed_file:
        f.write("Map vector quantisation file  : " + output_filename + "_vq.pdb" + "\n")
    else:
        f.write("Map vector quantisation file  : " + args.seed_file + "\n")
    f.close()

    print("Starting gamma tempy run...")
    # Run GA assembly fitting
    _ = ga.run(
        grun,
        ngen,
        total_popsize,
        selection_method,
        gof,
        w_gof,
        w_clash,
        prot,
        nchains,
        emmap,
        res,
        output_name,
        pdb_snapshot_name,
        vq_vec_list,
        mrate,
        crate,
        moffset,
        ncpu,
    )
    # finish job
    f = open(output_name + ".log", "a")
    f.write(
        "------------------------------------------------------------------------------------------\n"
    )
    f.write("Execution time (sec): " + str(time.time() - start_time) + "\n")
    f.close()
    print("Finished gamma tempy run!")
    exit(0)


if __name__ == "__main__":
    main()

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
#     Farabella, I., Vasishtan, D., Joseph, A.P., Pandurangan, A.P., Sahota, H
#     & Topf, M. (2015). J. Appl. Cryst. 48.
#
# =============================================================================

import os
import sys
try:
    import matplotlib.cm as cm
    import matplotlib.gridspec as gridspec
    from matplotlib.ticker import MultipleLocator
    from matplotlib import rcParams  # noqa:F401
except ImportError:
    sys.stderr.write('to run this module please install matplotlib\n')
    sys.exit()

try:
    import matplotlib.pyplot as plt
except RuntimeError:
    plt = None

import scipy.spatial.distance as ssd
import numpy as np
import scipy.cluster.hierarchy as hier


class Plot:
    """A class to create analysis output"""

    def __init__(self):
        pass

    def ShowHierarchicalClusterings(
            self,
            ranked_ensemble,
            mxRMSD,
            rms_cutoff,
            name='HierClustPlt',
            save=False,
            cluster_index=False,
            figsize=(4, 4),
            reverse=False,
    ):
        """
        Plot the Calpha RMSD hierarchical clustering of the multiple "fits".
            Arguments:
                *ranked_ensemble*
                    Input list of Structure Instances. It is list of fits
                    obtained with Cluster.rank_fit_ensemble function.
                *mxRMSD*
                    Pairwise RMSD matrix for all Structure Instance in the
                    ensemble obtained as one Cluster.RMSD_ensemble function.
                *rms_cutoff*
                    float,  the Calpha RMSD cutoff based on which you want to
                    cluster the solutions. For example 3.5 (for 3.5 A).
                    Suggested value the mean of the pairwise RMSD matrix.
                *name*
                    Output file name (.pdf)
                *save*
                    True will save a pdf file of the plot.
                *cluster_index*
                    True will return a list that contains the model and the
                    related cluster index.
        """
        mxscore = np.zeros(shape=(len(ranked_ensemble), 1))
        for k in range(len(ranked_ensemble)):
            mxscore[k] = float('%.3f' % (ranked_ensemble[k][2]))
        fig = plt.figure(figsize=figsize, dpi=300)
        heatmapGS = gridspec.GridSpec(
            1,
            2,
            wspace=0.0,
            hspace=0.0,
            width_ratios=[1, 1],
        )
        denAX = fig.add_subplot(heatmapGS[0, 0])
        # noqa:E501 see why @http://stackoverflow.com/questions/18952587/use-distance-matrix-in-scipy-cluster-hierarchy-linkage

        mxRMSD_cond = ssd.squareform(mxRMSD)
        linkageMatrixZ = hier.linkage(mxRMSD_cond, method='complete')
        labels = [
            ranked_ensemble[x][0].replace("mod_", "")
            for x in range(len(ranked_ensemble))
        ]
        hier_dendo = hier.dendrogram(
            linkageMatrixZ,
            color_threshold=rms_cutoff,
            orientation='right',
            get_leaves=True,
            distance_sort=True,
            show_leaf_counts=True,
            show_contracted=True,
            labels=labels,
        )
        denAX.get_xaxis().set_ticks([])
        heatmapAX = fig.add_subplot(heatmapGS[0, 1])
        index = hier_dendo['leaves']
        cluster_dendro = hier_dendo['ivl']
        # reorder matrix
        mxscore = mxscore[index, :]
        if reverse is True:
            axi = heatmapAX.imshow(
                mxscore,
                interpolation='nearest',
                cmap=plt.cm.Blues_r,
                origin='lower',
            )
        else:
            axi = heatmapAX.imshow(
                mxscore,
                interpolation='nearest',
                cmap=plt.cm.Blues,
                origin='lower',
            )
        ax = axi.get_axes()
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        heatmapAX.get_xaxis().set_ticks([])
        heatmapAX.get_yaxis().set_ticks([])

        if save is True:
            fig.savefig(str(name)+'.pdf')
        plt.show()
        if cluster_index is True:
            ind = hier.fcluster(linkageMatrixZ, rms_cutoff, 'distance')
            ind = ind.ravel()
            ind = ind[index, ]
            print(zip(mxscore.ravel().tolist(), cluster_dendro, ind))
            return zip(mxscore.ravel().tolist(), cluster_dendro, ind)

    def ShowRMSDmatrix(
            self,
            mxRMSD,
            name='RMSDmatrix',
            save=False,
    ):
        """
        Plot the pairwise RMSD matrix for all Structure Instance in the
        ensemble.
            Arguments:
                *mxRMSD*
                    Pairwise RMSD matrix for all Structure Instance in the
                    ensemble obtained as one Cluster.RMSD_ensemble function.
                *name*
                    Output file name (.pdf)
                *save*
                    True will save a pdf file of the plot.
        """

        fig = plt.figure(figsize=(6, 3.2))
        ax = fig.add_subplot(111)
        ax.set_title('RMSD matrix')
        plt.imshow(
            mxRMSD,
            interpolation='nearest',
            cmap=plt.cm.coolwarm,
            origin='lower',
        )
        ax.set_aspect('equal')
        cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
        cax.get_xaxis().set_visible(False)
        cax.get_yaxis().set_visible(False)
        cax.patch.set_alpha(0)
        cax.set_frame_on(False)
        plt.colorbar(orientation='vertical')
        if save is True:
            fig.savefig(str(name) + '.pdf')
        plt.show()

    def ShowGeneralMatrix(
            self,
            mxGen,
            file_name='HeatMap',
            save=False,
            range=(0, 1),
            figsize=(7, 5),
            cmap=None
    ):
        """
        Heat Map plot of a matrix.
        Arguments:
            *mxGen*
               Generic Matrix. Use SCCCHeatMap_fromSCCCfiles or
               SCCCHeatMap_fromSCCCList to generate a matrix from a set of
               segment assessed with SCCC score.
            *name*
                Output file name (.pdf)
            *save*
                True will save a pdf file of the plot.
            *range*
                set the min and max score.
            *cmap*
                color palette to use. Choose form the one available in
                matplotlib or use cmp_Rainbow.
        """
        if cmap is None:
            cmap = plt.cm.Blues
        fig = plt.figure(figsize=figsize, dpi=300)
        ax = fig.add_subplot(111)
        plt.imshow(
            mxGen,
            interpolation='nearest',
            cmap=cmap,
            vmin=range[0],
            vmax=range[1],
            origin='lower',
        )
        ax.set_aspect('equal')
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
        cax.get_xaxis().set_visible(False)
        cax.get_yaxis().set_visible(False)
        cax.patch.set_alpha(0)
        cax.set_frame_on(False)
        plt.show()
        if save is True:
            fig.savefig(str(file_name) + '.pdf', bbox_inches='tight')

    def SCCCHeatMap_fromSCCCfiles(
            self,
            list_file,
            trans=False,
    ):
        """
        Return a matrix from a list of score.txt files as:
             x= Structure Instances and y= Structure Instances segments scored
        Arguments:
            *list_file*
                list of files
            *trans*
                True will transpose the matrix.
        """
        tot_file_list = []
        for f in list_file:
            fileIn = open(f, 'r')
            listfile = fileIn.readlines()
            list_float = []
            for score in listfile:
                num = '%.3f' % (float(score))
                list_float.append(num)
            tot_file_list.append(list_float)
        tot_file_list = np.array(tot_file_list)
        if trans is False:
            mxscoreInT = tot_file_list.transpose()
        else:
            mxscoreInT = tot_file_list
        mxscore = np.zeros(shape=(len(mxscoreInT), len(mxscoreInT[0])))

        for c in range(len(mxscoreInT)):
            for r in range(len(mxscoreInT[c])):
                num = '%.3f' % (float(mxscoreInT[c][r]))
                mxscore[c][r] = num
        return mxscore

    def cmp_Rainbow(self):
        """
        return rainbow color map.
        """
        cmap = plt.cm.get_cmap('spring', 5)
        # extract all colors from the .jet map
        cmaplist = [cmap(i) for i in range(cmap.N)]
        cmaplist[0] = (1.0, 0.0, 0.0, 1.0)
        cmaplist[1] = (1.0, 1.0, 0.0, 1.0)
        cmaplist[2] = (0.0, 1.0, 0.0, 1.0)
        cmaplist[3] = (0.0, 1.0, 1.0, 1.0)
        cmaplist[4] = (0.0, 0.0, 1.0, 1.0)
        cmap = cmap.from_list('Custom cmap', cmaplist, N=256)
        return cmap

    def SCCCHeatMap_fromSCCCList(self, sccc_list, trans=False):
        """
        Return a matrix from a list of score.txt files as:
             x= Structure Instances and y= Structure Instances segments
             scored
        Arguments:
            *sccc_list*
                list of list of SCCC scores
            *trans*
                True will transpose the matrix.
        """
        tot_file_list = []
        for f in sccc_list:
            list_float = []
            for score in sccc_list:
                num = '%.3f' % (float(score))
                list_float.append(num)
                tot_file_list.append(list_float)
        tot_file_list = np.array(tot_file_list)
        if trans is False:
            mxscoreInT = tot_file_list.transpose()
        else:
            mxscoreInT = tot_file_list

        mxscore = np.zeros(shape=(len(mxscoreInT), len(mxscoreInT[0])))

        for c in range(len(mxscoreInT)):
            for r in range(len(mxscoreInT[c])):
                num = '%.3f' % (float(mxscoreInT[c][r]))
                mxscore[c][r] = num
        return mxscore

    def PrintOutClusterAnalysis(
            self,
            cluster_output,
            file_name='cluster.out',
            write=False,
    ):
        """
        Print our a txt file that contains the clustering information after
        hierarchical clustering analysis.".
        Arguments:
            *cluster_output*
                List that contains the model and the related cluster index.
            *file_name*
                Output file name
            *write*
                True will save the file.
        """
        line = "model\tscore\tclusterRMSD\n"
        for x in cluster_output:
            line += '%s\t%s\t%s\n' % (x[1], x[0], x[-1])
        print(line)
        if write is True:
            file_out = open(file_name, 'w')
            file_out.write(line)
            file_out.close()

    def PrintOutChimeraCmdClusterAnalysis(
            self,
            cluster_output,
            path_dir,
            targetMap_location,
            file_name='chimera_cluster_color',
            load_map=True,
    ):
        """
        Print out a Chimera command file that can be used for visual inspection
        of the information after the hierarchical clustering analysis.".

        Arguments:
            *cluster_output*
                List that contains the model and the related cluster index.
            *path_dir*
                path to ensemble directory
            *targetMap_location*
                path to target map location
            *file_name*
                Output file name
            *load_map*
                True will add the loading option to the command file.
        """
        num_cluster = []
        list_mod = []
        list_mod_load = []
        for x in cluster_output:
            num_cluster.append(x[-1])
            list_mod.append(x[1])

        for filein in os.listdir(path_dir):
            for file_name_flag in list_mod:
                file_num = filein.split('.')[0].split('_')[-1]
                if file_name_flag == file_num:
                    list_mod_load.append(filein)

        colors = cm.rainbow(np.linspace(0, 1, np.max(num_cluster)))
        dict_mod = {}
        for lab in list_mod_load:
            file_num = lab.split('.')[0].split('_')[-1]
            print(lab, file_num)
            for mod in list_mod:
                if mod == file_num:
                    dict_mod[mod] = lab
                else:
                    pass
        count = 0
        line_out = ''
        line_out_attr = ''
        if load_map is True:
            line_out += 'open #%s %s\n' % (count, targetMap_location)

        for x in cluster_output:
            count += 1
            mod = x[1]
            clust_mod = x[-1]
            line_out_attr += '\t#%s\t%s\n' % (count, clust_mod)
            line_out += 'open #%s %s/%s\n' % (
                count,
                os.path.abspath(path_dir),
                dict_mod[mod]
            )
            line_out += 'colordef col_%s' % count
            for code_col in colors[(clust_mod-1)]:
                line_out += ' %.3f ' % code_col
            line_out += '\n'

            line_out += 'color col_%s #%s\n' % (count, count)

        outfile = open(file_name+'_attribute.txt', 'w')
        outfile.write('attribute: cluster\n')
        outfile.write('match mode: 1-to-1\n')
        outfile.write('recipient: molecules\n')
        outfile.write(line_out_attr)
        outfile.close()

        line_out += 'defattr %s' % (
            os.path.abspath(file_name+'_attribute.txt')
        )
        file_out = open(file_name+'.cmd', 'w')
        file_out.write(line_out)
        file_out.close()

    def PrintOutChimeraAttributeFileSCCC_Score(
            self,
            code_structure,
            sccc_list,
            listRB,
            out_path=None
    ):
        """
        Print out a Chimera attribute file that can be used for visual
        inspection of the information after Segment based cross-correlation
        (SCCC) calculation.

        Arguments:
            *code_structure*
                name of the structure instance
            *sccc_list*
                SCCC score for each of the segment.
            *listRB*
                list of segment used for the SCCC calculation.
            *out_path*
                set output path for attribute file
        """
        if out_path is None:
            outfile = open(code_structure + '_attribute.txt', 'w')
        else:
            outfile = open(out_path, 'w')
        outfile.write('attribute: sccc\n')
        outfile.write('match mode: 1-to-1\n')
        outfile.write('recipient: residues\n')
        sccc_list_3f = [str('%.3f' % score) for score in sccc_list]
        line_out = ''
        for line1, line2 in zip(listRB, sccc_list_3f):
            tokens = [item for sublist in line1 for item in sublist]
            check = 0
            for i in range(len(tokens) // 2):
                start = int(tokens[i * 2])
                end = int(tokens[i * 2 + 1])
                chainID = ''
                if ':' in tokens[i * 2]:
                    chainID = tokens[i * 2].split(':')[1]
                    if not tokens[i * 2 + 1].split(':')[1] == chainID:
                        print(
                            'Check chain IDs in rigid body file',
                            tokens[i * 2]
                        )
                        chainID = ''
                    start = int(tokens[i * 2].split(':')[0])
                    end = int(tokens[i * 2 + 1].split(':')[0])
                if check == 0:
                    for res in range(int(start), int(end + 1)):
                        if chainID:
                            line_out += '\t:%s.%s\t%s\n' % (
                                res,
                                chainID,
                                line2
                            )
                        else:
                            line_out += '\t:%s\t%s\n' % (res, line2)
                else:
                    for res in range(int(start), int(end + 1)):
                        if chainID:
                            line_out += '\t:%s.%s\t%s\n' % (
                                res,
                                chainID,
                                line2
                            )
                        else:
                            line_out += '\t:%s\t%s\n' % (res, line2)
                check += 1
        outfile.write(line_out)

    def lineplot(
            self,
            dict_points,
            outfile,
            xlabel=None,
            ylabel=None,
            xlim=None,
            ylim=None,
            legend_loc='upper left',
            line=True,
            marker=True,
            leg_pos=1.2,
            lstyle=True
    ):
        print('Setting maptpltlib parameters')
        try:
            plt.style.use('ggplot')
        except AttributeError:
            pass
        if len(dict_points) < 4:
            leg_pos = 1.15
        elif len(dict_points) < 9:
            leg_pos = 1.4
        else:
            leg_pos = 1.6
        ymaxm = xmaxm = -100.0
        for k in dict_points:
            if max(dict_points[k][1]) > ymaxm:
                ymaxm = max(dict_points[k][1])
            if max(dict_points[k][0]) > xmaxm:
                xmaxm = max(dict_points[k][0])

        plt.set_cmap('Spectral')
        if len(dict_points) < 4:
            plt.set_cmap('gist_earth')
        # plt.gca().set_color_cycle([
        #     colormap(i) for i in np.linspace(0, 1, len(dict_points) + 1)
        # ])

        if ylim is not None:
            plt.gca().set_ylim(*ylim)

        plt.rcParams.update({'font.size': 18})
        plt.rcParams.update({'legend.fontsize': 14})

        if xlabel is not None:
            plt.xlabel(xlabel, fontsize=15)
        if ylabel is not None:
            plt.ylabel(ylabel, fontsize=15)

        if legend_loc == 'upper left':
            bbox_to_anchor = (0, leg_pos)
        elif legend_loc == 'upper right':
            bbox_to_anchor = (leg_pos, 0.7)

        list_styles = []
        for i in range(0, len(dict_points), 4):
            list_styles.extend(['-', ':', '-.', '--'])
        list_markers = [
            'o',
            '*',
            '>',
            'D',
            's',
            'p',
            '<',
            'v',
            ':',
            'h',
            'x',
            '+',
            ',',
            '.',
            '_',
            '2',
            'd',
            '^',
            'H',
        ]
        while len(list_markers) < len(dict_points):
            list_markers = list_markers.extend(list_markers)
        i = 0
        for k in dict_points:
            if line and marker:
                plt.plot(
                    dict_points[k][0],
                    dict_points[k][1],
                    linewidth=3.0,
                    label=k,
                    linestyle=list_styles[i],
                    marker=list_markers[i],
                )
            elif line and lstyle:
                plt.plot(
                    dict_points[k][0],
                    dict_points[k][1],
                    linewidth=3.0,
                    label=k,
                    linestyle=list_styles[i],
                )
            elif line:
                plt.plot(
                    dict_points[k][0],
                    dict_points[k][1],
                    linewidth=3.0,
                    label=k,
                )
            elif marker:
                plt.plot(
                    dict_points[k][0],
                    dict_points[k][1],
                    label=k,
                    marker=list_markers[i],
                )
            i += 1
        if legend_loc == 'upper right':
            plt.subplots_adjust(right=.7)
        leg = plt.legend(
            loc=legend_loc,
            bbox_to_anchor=bbox_to_anchor,
            borderaxespad=0.
        )
        for legobj in leg.legendHandles:
            legobj.set_linewidth(2.0)

        plt.savefig(outfile, bbox_extra_artists=(leg,), bbox_inches='tight')
        plt.close()

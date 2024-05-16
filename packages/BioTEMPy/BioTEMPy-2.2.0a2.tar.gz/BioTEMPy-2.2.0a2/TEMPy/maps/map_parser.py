# =============================================================================
#     This file is part of TEMPy.
#
#     TEMPy is a software designed to help the user in the manipulation
#     and analyses of macromolecular assemblies using 3D electron microscopy
#     maps.
#
#     Copyright  2015 Birkbeck College University of London. ]
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
#     Farabella, I., Vasishtan, D., Joseph, A.P., Pandurangan, A.P., Sahota,
#     H. & Topf, M. (2015). J. Appl. Cryst. 48.
#
# =============================================================================

import numpy as np
import struct as binary
import mrcfile

from TEMPy.maps.em_map import Map


class MapParser:

    def __init__(self):

        '''not sure anything needs to be initialised now'''

        pass

    @staticmethod
    def parseCcpemHeader(ccpem_header):
        """
        Convert the header object from mrcfile into the format used in TEMPy.

        Arguments:
            *ccpem_header*
                header object from mrcfile.

        Return:
            An array containing the header information from the mrc file in
            TEMPy format.
        """
        return [int(ccpem_header.nx),
                int(ccpem_header.ny),
                int(ccpem_header.nz),
                int(ccpem_header.mode),
                int(ccpem_header.nxstart),
                int(ccpem_header.nystart),
                int(ccpem_header.nzstart),
                int(ccpem_header.mx),
                int(ccpem_header.my),
                int(ccpem_header.mz),
                float(ccpem_header.cella.x),
                float(ccpem_header.cella.y),
                float(ccpem_header.cella.z),
                float(ccpem_header.cellb.alpha),
                float(ccpem_header.cellb.beta),
                float(ccpem_header.cellb.gamma),
                int(ccpem_header.mapc),
                int(ccpem_header.mapr),
                int(ccpem_header.maps),
                float(ccpem_header.dmin),
                float(ccpem_header.dmax),
                float(ccpem_header.dmean),
                int(ccpem_header.ispg),
                int(ccpem_header.nsymbt),
                ccpem_header.extra1,
                ccpem_header.exttyp,
                int(ccpem_header.nversion),
                ccpem_header.extra2,
                float(ccpem_header.origin.x),
                float(ccpem_header.origin.y),
                float(ccpem_header.origin.z),
                ccpem_header.map,
                ccpem_header.machst,
                float(ccpem_header.rms),
                ccpem_header.nlabl,
                ccpem_header.label
                ]

    @staticmethod
    def readMRCHeader(filename):
        """
        Read an MRC map file header using the ccpem mrcfile module.

        Arguments:
            *filename*
                input MRC map file name.

        Return:
            An array containing the header information from the mrc file in
            TEMPy format.
        """
        with mrcfile.open(filename) as mrc:
            return MapParser.parseCcpemHeader(mrc.header)

    @staticmethod
    def readMRC(filename, final_dtype=np.float64, transpose=True):
        """
        Read an MRC map file using the ccpem mrcfile module.

        Arguments:
            *filename*
                input MRC map file name.

        Return:
           A Map instance containing the data from the MRC map file.
        """
        with mrcfile.open(filename) as mrc:
            header = mrc.header
            data = mrc.data
            ext_header = mrc.extended_header

            apix = np.array((mrc.voxel_size.x,
                             mrc.voxel_size.y,
                             mrc.voxel_size.z))

            origin = np.array((header.origin.x,
                               header.origin.y,
                               header.origin.z))

            # MRC2000 maps tend to use nstart values for defining the origin.
            if np.all(origin == 0):
                origin_idx = np.array((header.nxstart,
                                       header.nystart,
                                       header.nzstart))
                origin = origin_idx * apix

        data = data.astype(final_dtype, copy=False)

        if transpose:
            # The order of axes is not always standard.  MRC axes
            # orders begin at 1, hence decrementing for 0 indexing.
            axes_order = [int(header.mapc) - 1,
                          int(header.mapr) - 1,
                          int(header.maps) - 1]

            apix = np.array((apix[axes_order[0]],
                             apix[axes_order[1]],
                             apix[axes_order[2]]))

            origin = np.array((origin[axes_order[0]],
                               origin[axes_order[1]],
                               origin[axes_order[2]]))

            new_axes = [2 - axes_order[2 - a] for a in (0, 1, 2)]
            data = np.transpose(data, axes=new_axes)

        return Map(
            data,
            origin,
            apix,
            filename,
            header=MapParser.parseCcpemHeader(header),
            ext_header=ext_header
            )

    @staticmethod
    def _readXPLOR(filename, user_origin=None, user_box_size=None):
        """
        Read density map file in XPLOR format
        NOTE: broken.

        Argument:
           *filename*
               input XPLOR map file name.

        Return:
           A Map instance containing the data read from XPLOR map file.
        """
        f = open(filename, 'r')
        while True:
            file_l = f.readline().split()
            if len(file_l) == 1 and file_l[0] == '0':
                break
        new_map = []
        line = 1
        while(True):
            line = f.readline().split()
            for dens in line:
                new_map.append(float(dens))
            if (
                len(new_map) >= new_map.box_size[0] *
                new_map.box_size[1] *
                new_map.box_size[2]
            ):
                break
        new_map = np.array(new_map)
        new_map = new_map.reshape(
            new_map.box_size[2],
            new_map.box_size[1],
            new_map.box_size[0],
        )
        f.close()
        return Map(
            new_map,
            new_map.origin,
            new_map.box_size,
            new_map.apix,
        )

    @staticmethod
    def _readSitus(self, filename):
        """
        Read density map file in Situs format

        Arguments:
           *filename*
               input Situs map file name.

        Return:
            A Map instance containing the data read from Situs map file.

        """
        f = open(self.filename, 'r')
        first_line = f.readline().split()
        apix = float(first_line[0])
        origin = map(float, first_line[1:4])
        box_size = map(int, first_line[4:7])
        new_map = []
        line = 1
        while(True):
            line = f.readline().split()
            for dens in line:
                new_map.append(float(dens))
            if len(new_map) >= box_size[0] * box_size[1] * box_size[2]:
                break
        new_map = np.array(new_map)
        new_map = new_map.reshape(box_size[2], box_size[1], box_size[0])
        f.close()
        return Map(new_map, origin, box_size, apix)


class old_MapParser:
    """
    A class to read various EM map file types into a Map object instance.
    """

    def __init__(self):
        self.numpy2mrc = {
            # convert these to int8
            np.uint8: 0,
            np.bool: 0,
            np.bool_: 0,

            # convert these to int16
            np.int16: 1,
            np.int8: 1,

            # convert these to float32
            np.float32: 2,
            np.float64: 2,
            np.int32: 2,
            np.int: 2,

            # convert these to complex64
            np.complex: 4,
            np.complex64: 4,
            np.complex128: 4,

            # convert these to uint16
            np.uint16: 6,
        }

    @staticmethod
    def readMRCHeader(filename, endian='<'):
        """
        Gets the header information from the MRC map file.

        Argument
           *filename*
               input MRC map file name
           *endian*
               Endianness: Little or big

        Return:
           A string containing the MRC header information.
        """
        f = open(filename, 'rb')
        fm_string = (
                endian + (10 * 'l') + (6 * 'f') + (3 * 'l') + (3 * 'f') +
                (27 * 'l') + (3 * 'f') + (4 * 'c') + 'lfl'
        )
        header = list(binary.unpack(fm_string, f.read(224)))
        notes = f.read(800)
        notes = notes.decode().replace('\x00', '')
        header.append(notes)
        header = tuple(header)
        f.close()
        return header

    @staticmethod
    def get_endian(filename):
        """
        Read an MRC map file

        Arguments:
            *filename*
                input MRC map file name.

        Return:
           Endianness: Little or big
        """
        h = old_MapParser.readMRCHeader(filename)
        if 0 <= h[3] <= 6:
            endian = '<'
        else:
            endian = '>'
        return endian

    @staticmethod
    def readMRC(filename, final_dtype=np.float64, chunk=[]):
        """
        Read an MRC map file

        Arguments:
            *filename*
                input MRC map file name.

        Return:
           A Map instance containing the data read from MRC map file.
        """

        mrc2numpy = {
            0: np.int8,
            1: np.int16,
            2: np.float32,
            4: np.complex64,
            6: np.uint16,  # according to UCSF
        }

        endian = old_MapParser.get_endian(filename)
        header = old_MapParser.readMRCHeader(filename, endian)

        box_size = tuple(np.flipud(header[0:3]))
        origin = header[49:52]  # ctrl UCSF

        # READ ORIGIN BASED ON MRC2000/CCP4 format
        apix = np.array((header[10] / header[0],
                        header[11] / header[1],
                        header[12] / header[2]))
        nstart = (
            header[4] * float(apix[0]),
            header[5] * float(apix[1]),
            header[6] * float(apix[2]),
        )
        crs_index = header[16:19]
        if not (
            1 in (crs_index[0], crs_index[1], crs_index[2]) and
            2 in (crs_index[0], crs_index[1], crs_index[2]) and
            3 in (crs_index[0], crs_index[1], crs_index[2])
        ):
            crs_index = (1, 2, 3)

        flag_orig = 0
        list_orig = [0.0, 0.0, 0.0]

        try:
            if header[52:56] == (b'M', b'A', b'P', b' '):
                origin = header[49:52]
                if (
                    (
                        np.isnan(origin[0]) or
                        np.isnan(origin[1]) or
                        np.isnan(origin[2])
                    ) or
                    (
                        origin[0] == 0.0 and
                        origin[1] == 0.0 and
                        origin[2] == 0.0
                    )
                ):
                    origin = (0.0, 0.0, 0.0)
                    flag_orig = 1
            else:
                flag_orig = 1
        except IndexError:
            origin = (0.0, 0.0, 0.0)
            pass

        if flag_orig == 1:
            if (
                (
                    nstart[0] == 0 and
                    nstart[1] == 0 and
                    nstart[2] == 0
                ) or
                (
                    np.isnan(nstart[0]) or
                    np.isnan(nstart[1]) or
                    np.isnan(nstart[2])
                )
            ):
                origin = (0.0, 0.0, 0.0)
            else:
                list_orig[crs_index[0] - 1] = nstart[0]
                list_orig[crs_index[1] - 1] = nstart[1]
                list_orig[crs_index[2] - 1] = nstart[2]
                origin = (list_orig[0], list_orig[1], list_orig[2])

        map_size = header[0] * header[1] * header[2]
        dt = mrc2numpy[header[3]]
        f = open(filename, 'rb')
        f.seek(1024)

        ext_head = []
        if header[23] != 0:
            fm_str = endian+(header[23]/4)*'f'
            ext_head = binary.unpack(fm_str, f.read(header[23]))

        if not chunk:
            # Read whole map
            map_data = np.fromfile(
                f, dtype=dt, count=map_size
            )
            map_data = map_data.reshape(box_size)
            map_data = np.array(map_data, dtype=final_dtype)
        else:
            # Read in subsection of map
            x1, y1, z1, x2, y2, z2 = chunk

            if (
                any(np.array([z1, y1, x1]) < 0) or
                any(np.array([z2, y2, x2]) > box_size)
            ):
                raise IndexError("Chunk indices outside of map range!")

            if any(np.array([x1, y1, z1]) >= np.array([x2, y2, z2])):
                print('First indices:  '+str(np.array([x1, y1, z1])))
                print('Second indices: '+str(np.array([x2, y2, z2])))
                raise IndexError(
                    "First x,y or z index > second x,y or z index!"
                )

            z_size = z2-z1
            y_size = y2-y1
            x_size = x2-x1
            map_data = []
            voxel_mem = dt(5).nbytes
            if header[3] == 0:
                dt = 'b'
            elif header[3] == 1:
                dt = 'h'
            elif header[3] == 2:
                dt = 'f'
            else:
                raise TypeError(
                    "MRC chunk read cannot currently deal with maps of dtype "
                    + str(dt))

            f.seek(z1*header[1]*header[0]*voxel_mem, 1)
            for p in range(z_size):
                f.seek(y1*header[0]*voxel_mem, 1)
                for q in range(y_size):
                    f.seek(x1*voxel_mem, 1)
                    map_data.extend(
                        binary.unpack(x_size*dt, f.read(x_size*voxel_mem))
                    )
                    f.seek((header[0]-x2)*voxel_mem, 1)
                f.seek((header[1]-y2)*header[0]*voxel_mem, 1)
            map_data = np.array(map_data).reshape((z_size, y_size, x_size))

        if endian == '>':
            map_data.byteswap(True)

        if crs_index[0] != 1 or crs_index[1] != 2 or crs_index[2] != 3:
            list_ind = [crs_index[0] - 1, crs_index[1] - 1, crs_index[2] - 1]
            index_new = (
                list_ind.index(0),
                list_ind.index(1),
                list_ind.index(2),
            )
            index_new1 = [2 - index_new[2 - a] for a in (0, 1, 2)]
            map_data = np.transpose(map_data, index_new1)

        f.close()
        return Map(
            map_data,
            origin,
            apix,
            filename,
            header=header,
            ext_header=ext_head
        )

    @staticmethod
    def _readXPLOR(filename, user_origin=None, user_box_size=None):
        """
        Read density map file in XPLOR format
        NOTE: broken.

        Argument:
           *filename*
               input XPLOR map file name.

        Return:
           A Map instance containing the data read from XPLOR map file.
        """
        f = open(filename, 'r')
        while True:
            file_l = f.readline().split()
            if len(file_l) == 1 and file_l[0] == '0':
                break
        new_map = []
        line = 1
        while(True):
            line = f.readline().split()
            for dens in line:
                new_map.append(float(dens))
            if (
                len(new_map) >= new_map.box_size[0] *
                new_map.box_size[1] *
                new_map.box_size[2]
            ):
                break
        new_map = np.array(new_map)
        new_map = new_map.reshape(
            new_map.box_size[2],
            new_map.box_size[1],
            new_map.box_size[0],
        )
        f.close()
        return Map(
            new_map,
            new_map.origin,
            new_map.box_size,
            new_map.apix,
        )

    @staticmethod
    def _readSitus(self, filename):
        """
        Read density map file in Situs format

        Arguments:
           *filename*
               input Situs map file name.

        Return:
            A Map instance containing the data read from Situs map file.

        """
        f = open(self.filename, 'r')
        first_line = f.readline().split()
        apix = float(first_line[0])
        origin = map(float, first_line[1:4])
        box_size = map(int, first_line[4:7])
        new_map = []
        line = 1
        while(True):
            line = f.readline().split()
            for dens in line:
                new_map.append(float(dens))
            if len(new_map) >= box_size[0] * box_size[1] * box_size[2]:
                break
        new_map = np.array(new_map)
        new_map = new_map.reshape(box_size[2], box_size[1], box_size[0])
        f.close()
        return Map(new_map, origin, box_size, apix)

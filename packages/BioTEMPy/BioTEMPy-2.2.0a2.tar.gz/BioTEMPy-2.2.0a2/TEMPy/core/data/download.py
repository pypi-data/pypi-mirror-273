""" Module regarding downloading data """

from enum import Enum
import os
from pathlib import Path
from urllib.parse import urlparse
import urllib.request
import zipfile


class DataType(Enum):
    """ Mapping of data types to download urls """
    tutorial = 'http://tempy.ismb.lon.ac.uk/tuto_files.zip'


class DownloadData:
    """ Class to download data to home directory """

    def __init__(self, download_type: str):
        self.tempy_path = Path.home()/'.TEMPy'
        self.data_type = download_type
        self.url = DataType[download_type].value
        self._check_tempy_folder_exists()

    def _check_tempy_folder_exists(self) -> None:
        """
        Determines if the .TEMPy folder exists in the home directory. If not
        the directory is made
        """
        if not self.tempy_path.exists():
            self.tempy_path.mkdir(parents=True, exist_ok=True)

    def _unzip_file(self, filename: str) -> None:
        """
        Unzip files downloaded for TEMPy

        :type filename: str
        :param filename: filename to unzip
        """
        zip_ref = zipfile.ZipFile(str(self.tempy_path / filename), 'r')
        zip_ref.extractall(str(self.tempy_path))
        zip_ref.close()

    def download_data(self) -> None:
        """
        Download the data into the .TEMPy folder
        """
        parsed_url = urlparse(self.url)
        filename = os.path.basename(parsed_url.path)
        if not (self.tempy_path/filename).exists():
            print(f'{self.data_type} data not found, downloading...')
            urllib.request.urlretrieve(self.url, str(self.tempy_path/filename))
            self._unzip_file(filename)
            print(
                f'Download complete. Data can be found at: {self.tempy_path}'
            )

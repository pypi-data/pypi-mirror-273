import pandas as pd
import scipy.io as sio
import h5py
import pickle
import json
from PIL import Image
import chardet
import logging
from src.exception.exception import CustomException


class DataReader:
    """
    A class for reading data from various file formats, handling potential
    encoding issues gracefully.

    Supports: CSV, Excel, JSON, MAT, HDF5, Pickle, JPG images

    Args:
        data_path (str): The path to the data file.
        default_encoding (str, optional): The default encoding to try
                                           if chardet fails (defaults to "utf-8").

    Raises:
        FileNotFoundError: If the data file is not found.
        IOError: If an error occurs during file reading.
        UnicodeDecodeError: If there's an issue decoding the file's content
            even with chardet and default encoding.
        UnsupportedFormatError: If the file format is not supported.
    """

    def __init__(self, data_path: str, default_encoding="utf-8"):
        self.data_path = data_path
        self.default_encoding = default_encoding
        self.logger = logging.getLogger(__name__)  # Set up logger

    def read(self) -> object:
        """
        Reads the data from the specified file path, handling encoding issues.

        Returns:
            object: The data loaded from the file, or 'File Not Accepted'
                    if the file format is not supported.

        Raises:
            FileNotFoundError: If the data file is not found.
            IOError: If an error occurs during file reading.
            UnicodeDecodeError: If there's an issue decoding the file's content
                even with chardet and default encoding.
            UnsupportedFormatError: If the file format is not supported.
        """

        extension = self.data_path.lower()

        try:
            with open(self.data_path, 'rb') as data_file:
                raw_data = data_file.read()

                # Try chardet for encoding detection
                try:
                    encoding = chardet.detect(raw_data)['encoding']
                except KeyError:  # Handle missing 'encoding' key
                    self.logger.warning(f"chardet failed to detect encoding for {self.data_path}. Using default ({self.default_encoding})")
                    encoding = self.default_encoding

                if extension[-4:] == '.csv':
                    try:
                        return pd.read_csv(self.data_path, encoding=encoding)
                    except UnicodeDecodeError as e:
                        raise CustomException(f"Error decoding CSV with encoding: {encoding}") from e
                elif extension[-5:] == '.xlsx':
                    return pd.read_excel(self.data_path)
                elif extension[-5:] == '.json':
                    with open(self.data_path, 'r', encoding=encoding) as json_file:
                        return json.load(json_file)
                elif extension[-4:] == '.mat':
                    return sio.loadmat(self.data_path)
                elif extension[-3:] == '.h5':
                    with h5py.File(self.data_path, 'r') as hdf5_file:
                        return hdf5_file['data'][:]
                elif extension in ('.pkl', '.jpg', '.jpeg'):
                    # Handle supported formats (pickle, jpg, jpeg)
                    if extension == '.pkl':
                        with open(self.data_path, 'rb') as pickle_file:
                            return pickle.load(pickle_file)
                    elif extension[-4:] == '.jpg' or extension == '.jpeg':
                        return Image.open(self.data_path)
                else:
                    raise UnsupportedFormatError(f"Unsupported file format: {extension}")

            # Return 'File Not Accepted' for unsupported formats
            return 'File Not Accepted'
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        except IOError as e:
            raise IOError(f"Error reading data: {str(e)}")
        except Exception as e:  # Optional generic exception handler
            self.logger.error(f"Unexpected error reading data: {str(e)}")
            raise  # Re-raise the exception


class UnsupportedFormatError(Exception):
    """Custom exception for unsupported file formats."""
    pass

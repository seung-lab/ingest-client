from __future__ import absolute_import
import six
import numpy as np
import time

from .path import PathProcessor
from .tile import TileProcessor

from PIL import Image

from cloudvolume import CloudVolume
from cloudvolume.lib import Bbox

class CloudVolumePathProcessor(PathProcessor):
    """Class for simple image stacks that only increment in Z, uses the dynamic filesystem utility"""
    def __init__(self):
        """Constructor to add custom class var"""
        PathProcessor.__init__(self)

    def setup(self, parameters):
        """Set the params


        Args:
            parameters (dict): Parameters for the dataset to be processed

        Returns:
            None
        """
        pass

    def process(self, x_index, y_index, z_index, t_index=None):
        """
        Method to compute the file path for the indicated tile

        Args:
            x_index(int): The tile index in the X dimension
            y_index(int): The tile index in the Y dimension
            z_index(int): The tile index in the Z dimension
            t_index(int): The time index

        Returns:
            (str): An absolute file path that contains the specified data

        """
        return ""


class CloudVolumeTileProcessor(TileProcessor):
    """A Tile processor for a single image file identified by z index"""

    def __init__(self):
        """Constructor to add custom class var"""
        TileProcessor.__init__(self)
        self.cv = None
        self.parameters = None

    def setup(self, parameters):
        """ Method to load the file for uploading data. Assumes intern token is set via environment variable or config
        default file

        Args:
            parameters (dict): Parameters for the dataset to be processed


        MUST HAVE THE CUSTOM PARAMETERS: "x_offset": offset to apply when querying the Boss
                                         "y_offset": offset to apply when querying the Boss
                                         "z_offset": offset to apply when querying the Boss
                                         "x_tile": size of a tile in x dimension
                                         "y_tile": size of a tile in y dimension
                                         "collection": source collection
                                         "experiment": source experiment
                                         "channel": source channel
                                         "resolution": source resolution

        Returns:
            None
        """
        self.parameters = parameters
        self.cv = CloudVolume(parameters['source_url'], fill_missing=True, progress=True)

    def process(self, file_path, x_index, y_index, z_index, t_index=0):
        """
        Method to load the image file.

        Args:
            file_path(str): An absolute file path for the specified tile
            x_index(int): The tile index in the X dimension
            y_index(int): The tile index in the Y dimension
            z_index(int): The tile index in the Z dimension
            t_index(int): The time index

        Returns:
            (io.BufferedReader): A file handle for the specified tile

        """
        # Compute cutout args

        tile_size = self.parameters['ingest_job']['tile_size']
        bbox = Bbox( 
            (
                tile_size["x"] * x_index,
                tile_size["y"] * y_index,
                tile_size["z"] * z_index, 
            ),
            (
                tile_size["x"] * (x_index + 1),
                tile_size["y"] * (y_index + 1),
                tile_size["z"] * (z_index + 1),
            )
        )

        if bbox.volume() < 1:
            data = np.zeros((tile_size['x'], tile_size['y']), dtype=self.cv.dtype)
        else:
            data = self.cv[ bbox.to_slices() ]

        # Save sub-img to png and return handle
        upload_img = Image.fromarray(np.squeeze(data))
        output = six.BytesIO()
        upload_img.save(output, format="TIFF")
        upload_img.save('./' + bbox.to_filename() + '.tiff', format='TIFF')

        # Send handle back
        return output
















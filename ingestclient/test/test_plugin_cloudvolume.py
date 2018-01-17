# Copyright 2016 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import

import json
import os
import unittest
import six
from pkg_resources import resource_filename

from PIL import Image
import numpy as np

from cloudvolume import CloudVolume
from cloudvolume.lib import xyzrange
from ingestclient.core.config import Configuration

class TestCloudVolumeTileProcessor(unittest.TestCase):
  
    def test_CloudVolumeImageStackTileProcessor(self):
        
        tp = self.config.tile_processor_class
        tp.setup(self.config.get_tile_processor_params())

        handle = tp.process(None, 0, 0, 0, 0)
        vol = CloudVolume(tp.parameters['source_url'])
        data = np.squeeze(vol[0:256, 0:256, 0])

        # Save sub-img to png and return handle
        upload_img = Image.fromarray(data)
        output = six.BytesIO()
        upload_img.save(output, format="TIFF")

        assert handle.read() == output.read()


    @classmethod
    def setUpClass(cls):
        cls.config_file = os.path.join(resource_filename("ingestclient", "test/data"), "boss-v0.1-cloudvolume.json")

        with open(cls.config_file, 'rt') as example_file:
            cls.example_config_data = json.load(example_file)

        cls.config = Configuration(cls.example_config_data)
        cls.config.load_plugins()







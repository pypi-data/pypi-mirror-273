from enum import Enum
from adzip.streams import *

import logging
logger = logging.getLogger("adzip")

class AdzCompression(Enum):
    Lossless = 0    # This compression level ensures no information loss
    HighQuality = 1 # This compression level ensures no visible loss in image and point cloud streams
    LowQuality = 2  # This compression level has acceptable visible loss in image and point cloud streams, but offers much smaller archive

class AdzFile:
    def __init__(self, compress_level = AdzCompression.Lossless):
        self._default_compression = compress_level
        self._pose_stream = None

    def open_stream(self, name: str, mode: str, stream_type: AdzStreamType, compress_level: AdzCompression = None, zip_options: dict = None) -> AdzStream:
        pass

    def inspect_stream(self, name: str) -> dict:
        # return meta data of 
        pass

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        # TODO: check that every stream has the same length, otherwise raise error
        # TODO: flush checksum of meta info and save the meta info into zip comment
        pass

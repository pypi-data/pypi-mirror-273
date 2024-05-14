from enum import Enum

import logging
logger = logging.getLogger("adzip")

class AdzStreamType(Enum):
    Unknown = 0 # stream types here are not exhaustive, to support stream customizations
    Pose = 1
    Video = 2
    Points = 3
    Structured = 4
    Raw = 5

class AdzStream:
    def __init__(self, parent, name, segmented=True): # segmented=True will make 
        self._parent = parent
        self._closed = False

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if self._closed:
            return

        # TODO: flush remaining data

    def push(self, data, *args, **kwargs):
        pass

class AdzVideoStream(AdzStream):
    def __init__(self):
        pass

    def push(self, data):
        # frame data is either pillow object or image file path
        pass

class AdzPointsStream(AdzStream):
    def __init__(self):
        pass

    def push(self, data, data_cls=None, data_aux=None):
        # frame data N*3 float numpy array, data_cls N*1 5bit uint numpy array, data_aux N*1 8bit uint numpy array
        pass

class AdzStructStream(AdzStream):
    def __init__(self):
        pass

    def push(self, data):
        # frame data has to be json serializable
        pass

class AdzRawStream(AdzStream):
    def __init__(self):
        pass

    def push(self, data: str | bytes):
        # frame data is either bytes or file path
        pass

class AdzPoseStream(AdzStream): # struct stream specialized for pose information
    def __init__(self):
        pass

    def push(self, data):
        # frame data is pos3d and rotation3d reported from an odometry system
        pass

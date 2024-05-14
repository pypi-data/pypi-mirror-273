class KITTIParser:
    def __init__(self, path):
        self._path = path

    @property
    def available_sequences(self, task: str):
        if task == "odometry":
            return ["%02d" % i for i in range(22)]
        else:
            raise ValueError("Unsupported KITTI task type!")

    def push_odometry_color(self, adz_file, sequence_id):
        pass

    def push_odometry_velodyne(self, adz_file, sequence_id, with_semantic_labels: bool = False):
        pass

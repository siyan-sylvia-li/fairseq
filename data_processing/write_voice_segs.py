import glob
import soundfile as sf
from swbd_processor import *

"""
    TODO: Segment into ~ 15 s segments
    Then store individual words based on mrk time stamps
    Then pass in those for kmeans extraction
"""

MASTER_PATH = "/scr/biggest/siyanli/unit_data/"
WRITE_PATH = "/scr/biggest/siyanli/unit_segments/"
DATA_PATH = "/nlp/scr/siyanli/icarus/icarus/full_data/"

class SegmentWriter:
    def __init__(self, fname):
        self.start_ind = -1
        self.end_ind = -1
        self.curr_f = 0

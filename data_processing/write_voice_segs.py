import glob
import os
import re

import soundfile as sf
from swbd_processor import SWBDTranscriptParser, SWBDAudioSegmenter
import gc

"""
    TODO: Segment into ~ 15 s segments
    Then store individual words based on mrk time stamps
    Then pass in those for kmeans extraction
"""

MASTER_PATH = "/scr/biggest/siyanli/unit_data/"
WRITE_PATH = "/scr/biggest/siyanli/unit_segments/"
DATA_PATH = "/nlp/scr/siyanli/icarus/icarus/full_data/"


class SegmentWriter:
    def __init__(self, fname_A, fname_B, tp, aseg):
        self.start = 0
        self.end = 0
        self.curr_f = 0
        self.fname_store_A = fname_A
        self.fname_store_B = fname_B
        self.tp = tp
        self.aseg = aseg
        self.file_len = aseg.get_conv_len()
        self.interval = 12.5

    def write_all_segs(self):
        while self.end + self.interval < self.file_len and self.curr_f < 50:
            # First extract the words from mrk files
            a_f, b_f, self.end = self.tp.filter_by_time(self.start, self.start + self.interval)
            # Then use the audio extractors to write to output audio files
            self.curr_f += 1
            curr_suffix = "_" + str(self.curr_f).zfill(4) + ".wav"
            curr_trans_suffix = "_" + str(self.curr_f).zfill(4) + ".txt"
            self.aseg.write_segments(self.start, self.end, store_path_A=self.fname_store_A + curr_suffix,
                                     store_path_B=self.fname_store_B + curr_suffix)
            # Write to transcript files
            a_words = [a.utterance for a in a_f]
            b_words = [b.utterance for b in b_f]
            f_a = open(self.fname_store_A.replace("raw_audio", "transcripts") + curr_trans_suffix, "w+")
            f_a.write(" ".join(a_words))
            f_b = open(self.fname_store_B.replace("raw_audio", "transcripts") + curr_trans_suffix, "w+")
            f_b.write(" ".join(b_words))
            print(self.start, self.end, self.curr_f, a_words, b_words)
            self.start = self.end


if __name__ == "__main__":
    all_sw_names = list(glob.glob(os.path.join(MASTER_PATH, "audio") + "/sw*.wav"))
    all_sw_names = set([re.search(r'sw[0-9]+', s).group() for s in all_sw_names])
    for f in all_sw_names:
        # Construct mrk file path
        mrk_path = DATA_PATH + f + "/" + f + ".mrk"
        trans_parse = SWBDTranscriptParser(mrk_path)
        # Construt audio file paths
        audio_path = MASTER_PATH + "audio/" + f
        audio_seg = SWBDAudioSegmenter(fname=None, fname_A=audio_path + "_A.wav", fname_B=audio_path + "_B.wav")
        segwrite = SegmentWriter(WRITE_PATH + "/raw_audio/" + f + "_A", WRITE_PATH + "/raw_audio/" + f + "_B",
                                 trans_parse, audio_seg)
        segwrite.write_all_segs()
        del segwrite
        del audio_seg
        del trans_parse
        gc.collect()


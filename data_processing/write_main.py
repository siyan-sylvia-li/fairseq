import os.path
import glob
import re

import librosa
import pandas
import soundfile as sf


wrong_files = ['sw2247', 'sw2262', 'sw2290', 'sw2485', 'sw2521', 'sw2533', 'sw2543', 'sw2617', 'sw2627', 'sw2631',
               'sw2684', 'sw2844', 'sw2930', 'sw2954', 'sw2968', 'sw3039', 'sw3050', 'sw3129', 'sw3144', 'sw2073',
               'sw2616']


def clean_num(text):
    text = re.sub(r'[^0-9*.]+', '', text).lower()
    return text


def clean_no_split(text):
    text = re.sub(r'\*\[\[.+]]', '', text)
    text = re.sub(r'[^a-zA-Z0-9{<> ]+', '', text).lower()
    text = text.replace("<<", "<")
    text = text.replace(">>", ">")
    while "<" in text and ">" in text:
        ind_l = text.index("<")
        ind_r = text.index(">")
        text = text[: ind_l] + text[ind_r + 1:]
    return text


class MonoWriter:
    def __init__(self, store_path, data_path):
        self.store_path = store_path
        self.data_path = data_path

    def extract_and_write_audio(self, name, audio_f):
        # first perform resampling
        wav, sr = librosa.load(audio_f, sr=16000, mono=False)
        # write separate channels into individual files
        sf.write(os.path.join(self.store_path, "audio", name + "_A.wav"), wav[0], sr)
        sf.write(os.path.join(self.store_path, "audio", name + "_B.wav"), wav[1], sr)

    def extract_and_write_transcript(self, name, transcript_f):
        words_A = []
        words_B = []
        mrk_lines = open(transcript_f).readlines()
        for i in range(len(mrk_lines)):
            mrk_lines[i] = re.sub(r' +', '|', mrk_lines[i]).replace("\n", "")
            mrk_lines[i] = [x for x in mrk_lines[i].split('|') if len(x)]
            if len(mrk_lines[i]):
                mrk_lines[i][-1] = clean_no_split(mrk_lines[i][-1])
                try:
                    if "A" in mrk_lines[i][0]:
                        words_A.append(mrk_lines[i][-1])
                    elif "B" in mrk_lines[i][0]:
                        words_B.append(mrk_lines[i][-1])
                except ValueError:
                    continue
        f_a = open(os.path.join(self.store_path, "text", name + "_A.txt"), "w+")
        f_a.write(" ".join(words_A))
        f_b = open(os.path.join(self.store_path, "text", name + "_B.txt"), "w+")
        f_b.write(" ".join(words_B))

    def extract_and_write_lines(self, name, transcript_df):
        df_trans = pandas.read_csv(transcript_df)
        lines_a = []
        lines_b = []
        for i, row in df_trans.iterrows():
            if not pandas.isna(row['clean_output']):
                t = row['clean_output'].replace("\n", "").replace("- /", "").replace(" /", "")
                if "A" in row['caller']:
                    lines_a.append(t)
                elif "B" in row['caller']:
                    lines_b.append(t)
        f_a = open(os.path.join(self.store_path, "text", name + "_A.txt"), "w+")
        f_a.write(" ".join(lines_a))
        f_b = open(os.path.join(self.store_path, "text", name + "_B.txt"), "w+")
        f_b.write(" ".join(lines_b))


    def read_and_write_all(self):
        for swname in glob.glob(self.data_path + "/*/"):
            sw_id = swname.replace(self.data_path, "").replace("/", "")
            try:
                audio_f = glob.glob(swname + "*.wav")[0]
                self.extract_and_write_audio(sw_id, audio_f)
                trans_f = glob.glob(swname + "*.dialogue.csv")[0]
                self.extract_and_write_lines(sw_id, trans_f)
            except IndexError:
                continue


if __name__=="__main__":
    mono_w = MonoWriter("/scr/biggest/siyanli/unit_data/", "/nlp/scr/siyanli/icarus/icarus/full_data/")
    mono_w.read_and_write_all()


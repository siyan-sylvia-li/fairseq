import glob
import librosa

if __name__=="__main__":
    root_path = "/scr/biggest/siyanli/unit_data/audio/"
    man_file = open("manifest_quant.txt", "a")
    for f in glob.glob(root_path + "*.wav"):
        f_fin = f.replace(root_path, "")
        y, sr = librosa.load(f, mono=True, sr=16000)
        num_frames = len(y)
        f_fin = f_fin + "\t" + str(num_frames) + "\n"
        man_file.write(f_fin)

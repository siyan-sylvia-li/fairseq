import glob
import librosa

if __name__=="__main__":
    root_path = "/scr/biggest/siyanli/unit_segments/raw_audio/"
    cts = 0
    man_file = open("manifest_0.txt", "w+")
    man_file.write(root_path + "\n")
    for f in glob.glob(root_path + "*.wav"):
        if cts % 10000 == 0:
            man_file = open("manifest_{}.txt".format(cts // 10000), "w+")
            man_file.write(root_path + "\n")
        cts += 1

        f_fin = f.replace(root_path, "")
        y, sr = librosa.load(f, mono=True, sr=16000)
        num_frames = len(y)
        if num_frames > 0:
            f_fin = f_fin + "\t" + str(num_frames) + "\n"
            man_file.write(f_fin)

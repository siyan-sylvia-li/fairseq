import glob

if __name__=="__main__":
    root_path = "/scr/biggest/siyanli/unit_output/clips/"
    man_file = open("manifest.txt", "a")
    for f in glob.glob(root_path + "*.wav"):
        f_fin = f.replace(root_path, "")
        f_fin = f_fin + "\t0.2\n"
        man_file.write(f_fin)

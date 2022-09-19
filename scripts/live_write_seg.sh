export TRANSFORMERS_CACHE=/scr/biggest/siyanli/.cache/
export HF_DATASETS_CACHE=/scr/biggest/siyanli/.cache/datasets/

cd /nlp/scr/siyanli/unit_icarus/data_processing
python3 write_voice_segs.py
echo "COMPLETED WRITING SEGMENTS"


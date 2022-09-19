#!/bin/bash
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:0
#SBATCH --mem 64G
#SBATCH --partition jag-hi
##SBATCH --exclude=jagupard4,jagupard5,jagupard6,jagupard7,jagupard8,jagupard10,jagupard11,jagupard12,jagupard13,jagupard14,jagupard15,jagupard16,jagupard17,jagupard18,jagupard19,jagupard20,jagupard21,jagupard22,jagupard23,jagupard24,jagupard25
#SBATCH -o /u/scr/siyanli/unit_icarus/%j.out
#SBATCH --nodelist=jagupard18

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/u/nlp/anaconda/main/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/u/nlp/anaconda/main/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/u/nlp/anaconda/main/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/u/nlp/anaconda/main/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<< case $HOSTNAME in

source activate siyan-unit-data
mkdir -p /scr/biggest/siyanli/
mkdir -p /scr/biggest/siyanli/unit_segments/raw_audio/
mkdir -p /scr/biggest/siyanli/unit_segments/transcripts/
export TRANSFORMERS_CACHE=/scr/biggest/siyanli/.cache/
export HF_DATASETS_CACHE=/scr/biggest/siyanli/.cache/datasets/

cd /nlp/scr/siyanli/unit_icarus/data_processing
python3 write_voice_segs.py
echo "COMPLETED WRITING SEGMENTS"


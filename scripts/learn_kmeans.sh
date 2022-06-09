#!/bin/bash
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH --mem 64G
#SBATCH --partition jag-hi
#SBATCH --exclude=jagupard10,jagupard11,jagupard12,jagupard13,jagupard14,jagupard15,jagupard16,jagupard17,jagupard18,jagupard19,jagupard20,jagupard21,jagupard22,jagupard23,jagupard24,jagupard25
##SBATCH --nodelist=jagupard28
#SBATCH -o /u/scr/siyanli/unit_icarus/%j.out

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

source activate siyan-units
# conda activate siyanli-icarus

mkdir -p /scr/biggest/siyanli/
export TRANSFORMERS_CACHE=/scr/biggest/siyanli/.cache/
export HF_DATASETS_CACHE=/scr/biggest/siyanli/.cache/datasets/

cd /nlp/scr/siyanli/unit_icarus/examples/textless_nlp/gslm/speech2unit/clustering

N_CLUSTERS=500
TYPE=w2v2swbd
CKPT_PATH=swbd_single
LAYER=0
MANIFEST=/nlp/scr/siyanli/unit_icarus/test_manifest.txt
KM_MODEL_PATH=/nlp/scr/siyanli/unit_icarus/outputs/

python3 cluster_kmeans.py \
    --num_clusters $N_CLUSTERS \
    --feature_type $TYPE \
    --checkpoint_path $CKPT_PATH \
    --layer $LAYER \
    --manifest_path $MANIFEST \
    --out_kmeans_model_path $KM_MODEL_PATH

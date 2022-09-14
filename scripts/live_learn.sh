export TRANSFORMERS_CACHE=/scr/biggest/siyanli/.cache/
export HF_DATASETS_CACHE=/scr/biggest/siyanli/.cache/datasets/

cd /nlp/scr/siyanli/unit_icarus/examples/textless_nlp/gslm/speech2unit/clustering

N_CLUSTERS=500
TYPE=w2v2swbd
CKPT_PATH=swbd_single
LAYER=0
MANIFEST=/scr/biggest/siyanli/unit_output/manifests/manifest.txt
KM_MODEL_PATH=/nlp/scr/siyanli/unit_icarus/outputs/

python3 cluster_kmeans.py \
    --num_clusters $N_CLUSTERS \
    --feature_type $TYPE \
    --checkpoint_path $CKPT_PATH \
    --layer $LAYER \
    --manifest_path $MANIFEST \
    --out_kmeans_model_path $KM_MODEL_PATH --sample_pct=1.0

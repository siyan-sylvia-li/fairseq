#pip install pandas plotly
export BRANCH='r1.10.0'
#git clone -b $BRANCH https://github.com/NVIDIA/NeMo
cd NeMo
python -m pip install git+https://github.com/NVIDIA/NeMo.git@$BRANCH#egg=nemo_toolkit[all]
#
#wget https://raw.githubusercontent.com/NVIDIA/NeMo/${BRANCH}/tools/ctc_segmentation/requirements.txt
#pip install -r requirements.txt

export NEMO_DIR_PATH="NeMo"
export OFFSET=0
export THRESHOLD=-2

bash tools/ctc_segmentation/run_segmentation.sh --MODEL_NAME_OR_PATH="QuartzNet15x5Base-En" \
  --DATA_DIR="/scr/biggest/siyanli/unit_data/" \
  --OUTPUT_DIR="/scr/biggest/siyanli/unit_output" \
  --SCRIPTS_DIR="tools/ctc_segmentation/scripts" \
  --MIN_SCORE=$THRESHOLD \
  --USE_NEMO_NORMALIZATION="False"

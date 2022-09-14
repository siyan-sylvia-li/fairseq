# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import random

import torch
import soundfile as sf
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, Wav2Vec2FeatureExtractor


class SWBDWav2vecFeatureReader:
    """
    Wrapper class to run inference on Wav2Vec 2.0 model.
    Helps extract features for a given audio file.
    """

    def __init__(self, checkpoint_path, layer, cuda=True):
        model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-robust-ft-swbd-300h")
        model.eval()
        self.cuda = cuda
        if self.cuda:
            model.cuda()
        model.freeze_feature_encoder()
        self.model = model
        self.feats_model = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-robust-ft-swbd-300h")
        self.layer = layer
        self.mode = checkpoint_path

    def read_audio(self, fname):
        wav, sr = librosa.load(fname, sr=16000, mono=True)
        # if len(wav.shape) == 1:
        #     wav = wav.reshape((1,) + wav.shape + (1,))
        print(wav.shape, "WAV SHAPE")
        return wav

    def get_feats(self, file_path):
        x = self.read_audio(file_path)
        with torch.no_grad():
            input_values = self.feats_model(x, return_tensors="pt", padding="longest", sampling_rate=16000).input_values
            # input_values = input_values.unsqueeze(-1).squeeze(0)
            if self.cuda:
                input_values = input_values.cuda()
            # input_values = input_values.unsqueeze(0)
            res = self.model.wav2vec2(input_values).extract_features
            if self.mode == "swbd_single":
                random_ind = random.randint(0, 1)
                return res[random_ind, :, :]
            return res

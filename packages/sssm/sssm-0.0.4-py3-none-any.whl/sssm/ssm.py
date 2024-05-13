import json
from glob import glob

import scipy
import torch
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample
import seaborn as sns
import pandas as pd
import einops
from torch import nn
from . import saved_models


class SSM:
    def __init__(self, device='cuda', model_path=None):
        self.input_data_length = None
        self.step = None
        self.device = torch.device(device)
        self.model = self.__load_model(model_path)
        self.softmax = torch.nn.Softmax(dim=1)
        self.predict_proba = None
        self.pred = None
        self.N_TIME = 300
        self.LABEL_SHORT = ['Sp', 'Kc', 'SWA', 'St', 'VS', 'Bg', 'Ar']
        self.LABEL_LONG = ['Spindle', 'K-complex', 'Slow wave', 'Sawtooth', 'Vertex Sharp', 'Background', 'Arousal']

    def predict(self, data=None, step=50, window=20):
        """
        input data, predict sleep event for each time step
        :param step: 300 >= step >= 1
        :param data: (n_epoch, n_channel, n_time)
        :param window: the window of the median filter for predicted label
        :return: predict_proba, pred, filtered pred, feature
        """
        assert data.shape[2] >= 300, 'n_time should > 300'
        assert 300 >= step >= 1
        self.step = step
        self.input_data_length = data.shape[2]

        n_epoch = data.shape[0]
        sliding_window_sample = np.lib.stride_tricks.sliding_window_view(data, self.N_TIME, axis=2)[:, :, ::step]
        sliding_window_sample = einops.rearrange(sliding_window_sample,
                                                 'n_epoch n_ch n_window n_time -> (n_epoch n_window) n_ch n_time')
        sample = torch.from_numpy(sliding_window_sample).float().to(self.device)
        proba, fea = self.__predict(sample)
        fea = einops.rearrange(fea, '(n_epoch n_window) n_hd n_step -> n_epoch n_window n_hd n_step',
                               n_epoch=n_epoch)
        pred = np.argmax(proba, axis=1)
        self.predict_proba = einops.rearrange(proba, '(n_epoch n_window) n_class -> n_epoch n_window n_class',
                                              n_epoch=n_epoch)
        self.pred = einops.rearrange(pred, '(n_epoch n_window) -> n_epoch n_window', n_epoch=n_epoch)
        pred_f = scipy.signal.medfilt(self.pred, [1, int(window + 1)])

        return self.predict_proba, self.pred, pred_f, fea

    def plot_predictions(self, epoch_ind=0):
        proba = pd.DataFrame(self.predict_proba[epoch_ind] * 100, columns=self.LABEL_SHORT)
        sns.set_theme('notebook', style='ticks', palette='bright')
        ax = proba.plot(kind='area', figsize=(50, 4), alpha=0.9, stacked=True, lw=0)
        ax.set_xlim(0, proba.shape[0])
        ax.set_ylim(0, 100)
        ax.set_ylabel("Probability")
        ax.set_xlabel("Epoch Index / 30s")
        N_WIN_PER_EPOCH = int((3000 - self.N_TIME) / self.step + 1)
        N_EPOCH_STEP = 50
        ori_ticks = np.arange(0, len(proba), N_EPOCH_STEP * N_WIN_PER_EPOCH, dtype=int)
        ax.set_xticks(ori_ticks, (ori_ticks / N_WIN_PER_EPOCH).astype(int))
        # ax.plot(sample_[0,0,150:2850]/300+1.5,color='0')
        # confidence = proba.max(1)
        plt.legend(bbox_to_anchor=(0.04, 0.5))
        # plt.legend()
        # plt.figure(figsize=(50, 4))
        # plt.xlim(0, 2700)
        # plt.plot(self.pred[epoch_ind] + 0.1)
        # plt.yticks(range(len(labels)), labels, rotation=90)
        # plt.ylabel("Label")
        # plt.ylim(len(labels) - 0.5, -0.5)
        # _ = plt.plot(pred_f[ind])

    def to_json(self):
        pass

    def to_pandas(self, overall_threshold=0.5, describe=False, event_threshold=None):
        """
        get pandas dataframe
        :param overall_threshold:
        :param describe: if return describe statics or not
        :param event_threshold: dict, predict proba threshhold for each label
        :return: predicted results in pandas Dataframe format
        """
        label_ind = np.argwhere(self.predict_proba > overall_threshold)
        last_ind = label_ind[0]
        starts = [last_ind]
        ends = []
        for this_ind in label_ind[1:]:
            if this_ind[1] - last_ind[1] == 1 and this_ind[2] == last_ind[2]:
                last_ind = this_ind
            else:
                ends.append(last_ind)
                starts.append(this_ind)
                last_ind = this_ind
        ends.append(label_ind[-1])

        step = self.step
        starts_ = np.array(starts)
        ends_ = np.array(ends)
        proba_ = []
        for s_, e_ in zip(starts_, ends_):
            proba_.append(self.predict_proba[s_[0], s_[1]:e_[1] + 1, s_[2]].mean())
        starts = starts_[:, 1] * step + int(150 - step / 2)
        ends = ends_[:, 1] * step + int(150 + step / 2)
        starts = np.where(starts <= int(150 - step / 2), 0, starts)
        ends = np.where(ends >= self.input_data_length - int(150 + step / 2), self.input_data_length, ends)

        df = pd.DataFrame({
            'Start': starts,
            'End': ends,
            'Duration': ends - starts,
            'label': [self.LABEL_LONG[label_ind] for label_ind in ends_[:, 2]],
            'predict_proba': proba_,
            'epoch_id': ends_[:, 0],
        })

        if event_threshold is None:
            event_threshold = {
                'Spindle': 0.95,
                'Background': 0.9,
                'Arousal': 0.9,
                'K-complex': 0.6,
                'Slow wave': 0.6,
                'Vertex Sharp': 0.6,
                'Sawtooth': 0.6}
        inds = []
        for label in event_threshold:
            inds.extend(df.query(f'label=="{label}" and predict_proba<{event_threshold[label]}').index.to_list())
        df = df.drop(index=inds)

        if describe is True:
            describe = df.groupby('label').describe()['predict_proba'][['count', 'mean']]
            describe['percentage'] = 100 * describe['count'] / describe['count'].sum()
            describe.rename(columns={'mean': 'predict_proba_mean'}, inplace=True)
            describe['predict_proba_mean'] *= 100
            return df, describe
        else:
            return df

    def __predict(self, data):
        torch.cuda.empty_cache()
        with torch.no_grad():
            pre, fea = self.model(data)
            proba = self.softmax(pre).cpu().numpy()
        torch.cuda.empty_cache()
        return proba, fea
        # pre = einops.rearrange(pre, '(n_epoch n_window) n_class -> n_epoch n_window n_class', n_epoch=n_epoch)
        # fea = einops.rearrange(fea, '(n_epoch n_window) n_hd n_step -> n_epoch n_window n_hd n_step', n_epoch=n_epoch)

    def __load_model(self, model_path):
        model = base_Model(Config()).to(self.device)
        if model_path is None:
            from importlib import resources
            model_path = os.path.join(resources.files(saved_models), 'model.pt')
        chkpoint = torch.load(model_path, map_location=self.device)
        pretrained_dict = chkpoint["model_state_dict"]
        model.load_state_dict(pretrained_dict)
        model.eval()
        return model

class base_Model(nn.Module):
    def __init__(self, configs):
        super(base_Model, self).__init__()

        self.conv_block1 = nn.Sequential(
            nn.Conv1d(configs.input_channels, 32, kernel_size=configs.kernel_size,
                      stride=configs.stride, bias=False, padding=(configs.kernel_size // 2)),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2, padding=1),
            nn.Dropout(configs.dropout)
        )

        self.conv_block2 = nn.Sequential(
            nn.Conv1d(32, 64, kernel_size=8, stride=1, bias=False, padding=4),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2, padding=1)
        )

        self.conv_block3 = nn.Sequential(
            nn.Conv1d(64, configs.final_out_channels, kernel_size=8, stride=1, bias=False, padding=4),
            nn.BatchNorm1d(configs.final_out_channels),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2, padding=1),
        )

        model_output_dim = configs.features_len
        self.logits = nn.Linear(model_output_dim * configs.final_out_channels, configs.num_classes)

    def forward(self, x_in):
        x = self.conv_block1(x_in)
        x = self.conv_block2(x)
        x = self.conv_block3(x)

        x_flat = x.reshape(x.shape[0], -1)
        logits = self.logits(x_flat)
        return logits, x

class Config(object):
    def __init__(self):
        # model configs
        self.input_channels = 1
        self.final_out_channels = 128
        self.num_classes = 7
        self.dropout = 0.35

        self.kernel_size = 25
        self.stride = 3
        self.features_len = 15  # 15  # 127, 44

        # training configs
        self.num_epoch =50

        # optimizer parameters
        self.optimizer = 'adam'
        self.beta1 = 0.9
        self.beta2 = 0.99
        self.lr = 3e-4

        # data parameters
        self.drop_last = True
        self.batch_size = 3500

        self.Context_Cont = Context_Cont_configs()
        self.TC = TC()
        self.augmentation = augmentations()


class augmentations(object):
    def __init__(self):
        self.jitter_scale_ratio = 1.5
        self.jitter_ratio = 2
        self.max_seg = 12


class Context_Cont_configs(object):
    def __init__(self):
        self.temperature = 0.2
        self.use_cosine_similarity = True


class TC(object):
    def __init__(self):
        self.hidden_dim = 128
        self.timesteps = 5

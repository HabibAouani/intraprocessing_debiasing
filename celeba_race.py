import sys
import os
import torch
import torchvision
import numpy as np
from torchvision.datasets import CelebA
from torch.utils.data import Subset

white = np.load(os.path.expanduser('celebrace/white_full.npy'))
black = np.load(os.path.expanduser('celebrace/black_full.npy'))
asian = np.load(os.path.expanduser('celebrace/asian_full.npy'))


class CelebRace(CelebA):

    def __getitem__(self, index):

        X, target = super().__getitem__(index)
        ind = int(self.filename[index].split('.')[0])

        augment = torch.tensor([white[ind-1] > .501,
                                black[ind-1] > .501,
                                asian[ind-1] > .501,
                                ind,
                                1-target[20]], dtype=torch.long)

        return X, torch.cat((target, augment))


def unambiguous(dataset, split='train', thresh=.7):
    # return only the images which were predicted white, black, or asian by >70%

    if split == 'train':
        n = 162770
    else:
        n = 19962
    unambiguous_indices = [i for i in range(n) if (white[i] > thresh or black[i] > thresh or asian[i] > thresh)]

    return Subset(dataset, unambiguous_indices)


def split_check(dataset, split='train', thresh=.7):

    if split == 'train':
        n = 162770
    else:
        n = 19962
    unambiguous_indices = [i for i in range(n) if (asian[i] > thresh)]

    return Subset(dataset, unambiguous_indices)

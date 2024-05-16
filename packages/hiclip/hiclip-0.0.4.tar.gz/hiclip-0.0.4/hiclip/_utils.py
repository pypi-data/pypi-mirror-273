import logging
from math import log10, sqrt

import numpy as np
import torch
from numpy.fft import fft2, ifft2, ifftshift
from scvi import scvi_logger, settings

"""
Hi-C matrix transformation
"""


def mat2array(mat):
    return mat[np.triu_indices_from(mat, k=0)]


def array2mat(array):
    def _get_square_root(number):
        _number, _tmp = number, 0
        while _number:
            _tmp += 1
            _number -= _tmp
        _number = _tmp
        return _number

    _len = _get_square_root(len(array))

    mat, a = np.zeros((_len, _len)), 0
    for i in range(_len):
        mat[i, i:] = array[a : a + _len - i]
        a += _len - i
    return mat + np.triu(mat, k=1).T


def tensor2mat(tensor: torch.Tensor) -> torch.Tensor:
    _tensor = torch.Tensor(
        np.array(
            [array2mat(tensor[i, :].flatten().cpu()) for i in range(tensor.shape[0])]
        )
    )
    return _tensor.to(tensor.device)


"""
Coarsen the matrix.
"""


def _fftblur(img, sigma):
    h, w = img.shape

    X, Y = np.meshgrid(np.arange(w), np.arange(h))
    X, Y = X - w // 2, Y - h // 2
    Z = np.exp(-0.5 * (X**2 + Y**2) / (sigma**2))
    Z = Z / Z.sum()

    out = ifftshift(ifft2(fft2(img) * fft2(Z)))
    return out


def _fan(sparse_mat, mask):
    N = np.prod(mask.shape)
    num_kept = np.nonzero(mask)[0].shape[0]
    sigma = sqrt(N / (np.pi * num_kept))

    c = _fftblur(sparse_mat, sigma)
    i = _fftblur(mask, sigma)

    mat = np.abs(c / i)
    return mat


def _sparsify(mat, sparse_mat, span):
    h, w = mat.shape
    for i in range(0, h, span):
        for j in range(0, w, span):
            tmp = mat[i : i + span, j : j + span].mean()
            _x, _y = i + span / 2, j + span / 2
            _length = max(abs(_x - _y), 1)
            tmp *= max(log10(_length), 1)
            sparse_mat[i : i + span, j : j + span] += tmp
    return sparse_mat


def coarsen(mat, spans=[5, 10]):
    mask = np.ones(mat.shape)
    sparse_mat = np.zeros(mat.shape)

    spans.sort(reverse=True)
    for span in spans:
        sparse_mat = _sparsify(mat, sparse_mat, span)

    return _fan(sparse_mat, mask)


"""
metric
"""


def hiclip_metric(
    l1_loss: float,
    perceptual_loss: float,
) -> float:
    return np.nanmean([l1_loss, perceptual_loss])


"""
log
"""

_logger = scvi_logger
settings.logging_dir = "./.hiclip/"

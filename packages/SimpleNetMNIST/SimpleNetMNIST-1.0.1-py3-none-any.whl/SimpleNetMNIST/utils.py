"""
Utilities for using PyTorch. 
"""

import math
import random
import matplotlib.pyplot as plt
import torch

from typing import Optional

def get_available_device():
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    return device

def plot_dataset_images(dataset: torch.utils.data.Dataset,
                        k: int = 9,
                        *,
                        classes: Optional[list[str]] = None,
                        seed: Optional[int] = None):
    """
    Given a dataset, pick random images and plot them.

    :param dataset: dataset to pick images from
    :param k: the number of images to pick
    :param classes: used as the list of classes if provided, defaults to `dataset.classes`
    :param seed: the number used to seed the random generator
    """
    if classes is None:
        if hasattr(dataset, "classes"):
            classes = dataset.classes
        else:
            raise ValueError("dataset doesn't have attribute classes,"
                             " please provide the list of classes manually")
    if seed is not None:
        random.seed(seed)
    idx = random.sample(range(len(dataset)), k=k)

    a = math.floor(math.sqrt(9))
    b = math.ceil(k / a)
    for i in range(k):
        image, target = dataset[idx[i]]
        title = f"{classes[target]}"
        plt.subplot(a, b, i+1)
        plt.imshow(image.squeeze(), cmap="gray")
        plt.title(title)
        plt.axis(False)

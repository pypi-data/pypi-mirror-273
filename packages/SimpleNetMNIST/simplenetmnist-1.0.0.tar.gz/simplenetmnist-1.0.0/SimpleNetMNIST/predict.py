"""
Making, visualizing, and summarizing predictions using PyTorch models.
"""
import math
import matplotlib.pyplot as plt
import pandas as pd
import torch

from typing import Any, Optional

from torch import nn
from tqdm.auto import tqdm

from utils import get_available_device

device = get_available_device()

def plot_prediction(model: nn.Module,
                    image: torch.Tensor,
                    classes: list,
                    *,
                    ax: Optional[plt.Axes] = None,
                    device=device):
    """
    Predict an image using a given model and plot them.
    """
    if ax is None:
        ax = plt.subplot()

    model.to(device)
    model.eval()
    with torch.inference_mode():
        logits = model(image.unsqueeze(0).to(device))
        probs = torch.softmax(logits, dim=1)
        class_ = classes[torch.argmax(probs, dim=1)]

    ax.imshow(image.permute(1, 2, 0), cmap="gray")
    ax.set_title(f"predict: {class_}")
    ax.axis(False)

    return probs, class_

def prediction_dataframe(model, dataset, classes, device=device):
    """
    Predict all images in a given dataset using a given model and produce a
    data frame containing the prediction, label and probabilities the model
    thinks that they are for both.
    """

    model.to(device)
    model.eval()

    results = []
    with torch.inference_mode():
        for image, label in (tqdm(dataset, desc="Predict", unit="sample")):
            logits = model(image.unsqueeze(0).to(device))
            probs = torch.softmax(logits, dim=1)
            predict = torch.argmax(probs, dim=1).item()
            pred_prob = probs[0, predict].item()
            label_prob = probs[0, label].item()
            results.append([
                classes[predict],
                pred_prob,
                classes[label],
                label_prob
            ])

    return pd.DataFrame(
        results,
        columns=[
            "prediction",
            "predict_probability",
            "label",
            "label_probability"
        ]
    )

def plot_worst_predictions(pred_df: pd.DataFrame, dataset, n=9):
    """
    Plot the worst predictions in a given prediction DataFrame.

    The wrong predictions with the highest probabilities are considered the most
    incorrect predictions.

    :param pred_df: the data frame containing the prediction results, see :meth:`prediction_dataframe`
    :param dataset: the dataset used for the model predictions
    :param int n: the number of worst predictions to plot
    """
    wrong_df = pred_df[pred_df["prediction"] != pred_df["label"]]
    worst_df = wrong_df.sort_values(
        "predict_probability",
        ascending=False
    ).head(n)
    a = math.floor(math.sqrt(9))
    b = math.ceil(n / a)
    for i, row in enumerate(worst_df.itertuples()):
        image, target = dataset[row.Index]
        plt.subplot(a, b, i + 1)
        plt.imshow(image.squeeze(), cmap="gray")
        plt.title(
            f"Predict: {row.prediction}\n"
            f"Label: {row.label}",
        )
        plt.axis(False)
    plt.tight_layout(w_pad=3)

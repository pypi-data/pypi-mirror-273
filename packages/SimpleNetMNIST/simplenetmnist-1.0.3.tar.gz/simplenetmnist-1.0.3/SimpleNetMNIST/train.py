"""
Train and test PyTorch models with data loaders.
"""

import torch

from pathlib import Path
from typing import Optional

from torch import nn
from torch.utils.data import DataLoader
from torch.utils.tensorboard.writer import SummaryWriter
from tqdm.auto import tqdm

from utils import get_available_device

device = get_available_device()

def train_one_epoch(model: nn.Module,
                    dataloader: DataLoader,
                    loss_fn: nn.Module,
                    optimizer: torch.optim.Optimizer,
                    device: torch.device = device,
                    ):
    model.to(device)
    model.train()

    running_loss = 0.
    running_acc = 0.

    for data in dataloader:
        inputs, labels = data

        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(inputs)

        loss = loss_fn(outputs, labels)
        loss.backward()

        optimizer.step()

        running_loss += loss.item()
        correct = torch.sum(labels == torch.argmax(outputs, dim=1)).item()
        running_acc += correct / len(labels)

    return running_loss / len(dataloader), running_acc / len(dataloader)

def test_one_epoch(model: nn.Module,
                   dataloader: DataLoader,
                   loss_fn: nn.Module,
                   device: torch.device = device,
                   ):
    model.to(device)
    model.eval()

    running_loss = 0.
    running_acc = 0.

    with torch.inference_mode():
        for data in dataloader:
            inputs, labels = data
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)    
            loss = loss_fn(outputs, labels)
            
            running_loss += loss.item()
            correct = torch.sum(labels == torch.argmax(outputs, dim=1)).item()
            running_acc += correct / len(labels)

    return running_loss / len(dataloader), running_acc / len(dataloader)

def train_test_loop(model: nn.Module,
                    train_dataloader: DataLoader,
                    test_dataloader: DataLoader,
                    loss_fn: nn.Module,
                    optimizer: torch.optim.Optimizer,
                    *,
                    epochs: int = 5,
                    device: torch.device = device,
                    print_epochs: Optional[int] = True,
                    writer: Optional[SummaryWriter] = None,
                    save_to: Optional[str | Path] = None
                    ):
    """
    Train and test a model using the given train and test data loaders, loss
    function, and optimizer.

    :param model: model to train and test
    :param train_dataloader: data loader for training
    :param test_dataloader: data loader for testing
    :param loss_fn: loss function
    :param optimizer: optimizer
    :param epochs: train for this many iterations
    :param device: device to train the model on
    :param print_epochs: print results every this many epochs
    :param writer: a summary writer to write statistics to
    :param save_to: a path to save the model with highest accuracy
    """    
    if save_to is not None:
        save_to = Path(save_to)
        save_to.parent.mkdir(parents=True, exist_ok=True)

    best_test_acc = 0
    for epoch in tqdm(range(1, epochs + 1), unit="epoch"):
        avg_train_loss, avg_train_acc = train_one_epoch(
            model,
            train_dataloader,
            loss_fn,
            optimizer,
            device
        )

        avg_test_loss, avg_test_acc = test_one_epoch(
            model,
            test_dataloader,
            loss_fn,
            device
        )

        if print_epochs is not None and epoch % print_epochs == 0:
            tqdm.write(
                f"epoch: {epoch:5d} |"
                f" train loss: {avg_train_loss:.3f} |"
                f" train accuracy: {avg_train_acc:.1%} |"
                f" test loss: {avg_test_loss:.3f} |"
                f" test accuracy: {avg_test_acc:.1%}"
            )
        
        if writer is not None:
            writer.add_scalars(
                "Training vs. Test Loss",
                {"Training": avg_train_loss, "Test": avg_test_loss},
                epoch
            )
            writer.add_scalars(
                "Training vs. Test Accuracy",
                {"Training": avg_train_acc, "Test": avg_test_acc},
                epoch
            )
            writer.flush()

        if save_to is not None and avg_test_acc > best_test_acc:
            best_test_acc = avg_test_acc
            torch.save(model.state_dict(), save_to)

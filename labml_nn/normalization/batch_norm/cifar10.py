"""
---
title: CIFAR10 Experiment to try Group Normalization
summary: >
  This trains is a simple convolutional neural network that uses group normalization
  to classify CIFAR10 images.
---

# CIFAR10 Experiment for Group Normalization
"""

import torch.nn as nn

from labml import experiment
from labml.configs import option
from labml_helpers.module import Module
from labml_nn.experiments.cifar10 import CIFAR10Configs
from labml_nn.normalization.batch_norm import BatchNorm


class Model(Module):
    def __init__(self):
        super().__init__()
        layers = []
        in_channels = 3
        for block in [[64, 64], [128, 128], [256, 256, 256], [512, 512, 512], [512, 512, 512]]:
            for channels in block:
                layers += [nn.Conv2d(in_channels, channels, kernel_size=3, padding=1),
                           BatchNorm(channels),
                           nn.ReLU(inplace=True)]
                in_channels = channels
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        layers += [nn.AvgPool2d(kernel_size=1, stride=1)]
        self.layers = nn.Sequential(*layers)
        self.fc = nn.Linear(512, 10)

    def __call__(self, x):
        x = self.layers(x)
        x = x.view(x.shape[0], -1)
        return self.fc(x)


@option(CIFAR10Configs.model)
def model(c: CIFAR10Configs):
    """
    ### Create model
    """
    return Model().to(c.device)


def main():
    # Create experiment
    experiment.create(name='cifar10', comment='batch norm')
    # Create configurations
    conf = CIFAR10Configs()
    # Load configurations
    experiment.configs(conf, {
        'optimizer.optimizer': 'Adam',
        'optimizer.learning_rate': 2.5e-4,
        'train_batch_size': 64,
    })
    # Start the experiment and run the training loop
    with experiment.start():
        conf.run()


#
if __name__ == '__main__':
    main()

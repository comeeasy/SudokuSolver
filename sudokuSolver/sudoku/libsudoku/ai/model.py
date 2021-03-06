import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import logging
import os

from django.conf import settings

class MNISTModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(in_channels=1 ,out_channels=64, kernel_size=(7, 7), padding=(3, 3)),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 2)),

            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=(3, 3), padding=(1, 1)),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 2)),

            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=(1, 1)),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 2)),

            nn.Conv2d(in_channels=256, out_channels=10, kernel_size=(1, 1)),
            nn.BatchNorm2d(10),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 2)),

            nn.AdaptiveAvgPool2d(1)
        )

    def forward(self, x):
        output = self.layers(x)
        output = output.view(-1, 10)
        return output


class EfficientNet(nn.Module):
    def __init__(self):
        
        super(EfficientNet, self).__init__()
        self.first_layer = nn.Sequential(
            nn.Conv2d(1, 40, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False),
            nn.BatchNorm2d(40, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True),
            nn.GELU()
        )
        
        self._first_layer = nn.Sequential(
            *list(torchvision.models.efficientnet_b3(pretrained=True).children())[0][0]
        )
        
        self.origin_layer = nn.Sequential(
            *list(torchvision.models.efficientnet_b3(pretrained=True).children())[0][1:]
        )
        self._last_layer = nn.Sequential(
            *list(torchvision.models.efficientnet_b3(pretrained=True).children())[1:]
        )
        self.last_layer = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
        )

        self.fc_layer = nn.Sequential(
            nn.Dropout2d(p=0.3, inplace=True),
            nn.Linear(1536, 10, bias=True)
        )


    def forward(self, x):
        out = self.first_layer(x)
        out = self.origin_layer(out)
        out = self.last_layer(out)
        out = out.view(-1, 1536)
        out = self.fc_layer(out)

        return out

    def load(self, path="weights/EfficientNet-epoch29-acc0.99.pt", device="cpu"):
        self.load_state_dict(torch.load(path))
        self.to(device)
        self.eval()

        logging.info(f"model is loaded path={path}, device={device}")



class ConvNeXtTiny(nn.Module):
    def __init__(self) -> None:
        super().__init__()

        self.model = torchvision.models.convnext_tiny(pretrained=True, progress=True)

        self.model.features[0][0] = nn.Conv2d(1, 96, kernel_size=(4, 4), stride=(4, 4))
        self.model.classifier[2] = nn.Linear(768, 10, bias=True)

    def forward(self, x):
        return self.model.forward(x)


class ResNet34(nn.Module):
    def __init__(self) -> None:
        super().__init__()

        self.model = torchvision.models.resnet34(pretrained=True)
        self.model.conv1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        self.model.fc = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(512, 10, bias=False)
        )

    def forward(self, x):
        return self.model.forward(x)

    def load(self, path=os.path.join('..', 'static', 'weights', 'ResNet34-epoch58-acc99.65.pt'), device="cpu"):
        self.load_state_dict(torch.load(path, map_location=device))
        self.to(device)
        self.eval()

        logging.info(f"model is loaded path={path}, device={device}")

if __name__ == '__main__':
    model = ResNet34()
    
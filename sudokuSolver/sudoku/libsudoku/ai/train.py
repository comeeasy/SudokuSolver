import torchvision.datasets as datasets
import torchvision.transforms as transforms

import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
import torch.optim.lr_scheduler as lr_scheduler

import cv2

from model import EfficientNet, ConvNeXtTiny, ResNet34
from tqdm import tqdm


class AddGaussianNoise(object):
    def __init__(self, mean=0., std=1.):
        self.std = std
        self.mean = mean
        
    def __call__(self, tensor):
        return tensor + torch.randn(tensor.size()) * self.std + self.mean
    
    def __repr__(self):
        return self.__class__.__name__ + '(mean={0}, std={1})'.format(self.mean, self.std)

# download data
mnist_train_data = datasets.MNIST(root="./data",
                                  train=True,
                                  transform=transforms.Compose([
                                      transforms.ToTensor(),
                                      transforms.RandomAffine(degrees=(5, 10), translate=(0.1, 0.3), scale=(0.5, 1)),
                                      transforms.RandomInvert(0.5),
                                      AddGaussianNoise(0, 0.1),
                                      transforms.Resize((100, 100)),
                                  ]),
                                  download=True)
mnist_val_data = datasets.MNIST(root="./data",
                                train=False,
                                transform=transforms.Compose([
                                    transforms.ToTensor(),
                                    transforms.RandomInvert(0.5),
                                    transforms.Resize((100, 100))
                                ]),
                                download=True)

# DataLoad
mnist_train_dataloader = DataLoader(dataset=mnist_train_data,
                                    shuffle=True,
                                    batch_size=256,
                                    drop_last=True,
                                    num_workers=8)

mnist_val_dataloader = DataLoader(dataset=mnist_val_data,
                                  shuffle=False,
                                  batch_size=256,
                                  drop_last=True,
                                  num_workers=8)

if __name__ == "__main__":
    epochs = 60
    # model = MNISTModel().train().to("cuda")
    model = ResNet34()
    model.to("cuda")

    print(model.__class__.__name__)

    criteria = nn.CrossEntropyLoss().to("cuda")
    optimizer = optim.AdamW(params=model.parameters(), lr=1e-4)
    scheduler = lr_scheduler.CosineAnnealingLR(optimizer=optimizer, T_max=20, eta_min=0)

    minAcc = 0
    torch.backends.cudnn.benchmark = True
    model.train()
    for epoch in range(epochs):
        loss = 0
        for img, target in tqdm(mnist_train_dataloader):
            img[target == 0] = torch.normal(mean=0, std=0.1, size=img[target==0].shape)
            img = img.to("cuda")
            target = target.to("cuda")

            predict = model(img).to("cuda")
            cost = criteria(predict, target)

            optimizer.zero_grad()
            cost.backward()
            optimizer.step()

            loss += cost / len(mnist_train_dataloader)
        scheduler.step(epoch)

        model = model.eval()
        with torch.no_grad():
            accuracy = 0
            for img, target in tqdm(mnist_val_dataloader):
                img[target == 0] = torch.normal(mean=0, std=0.3, size=img[target==0].shape)
                img = img.to("cuda")
                target = target.to("cuda")

                predict = model(img).to("cuda")
                correct_predict = torch.argmax(predict, 1) == target
                accuracy += correct_predict.float().mean() / len(mnist_val_dataloader)

        print(f"epoch: {epoch:2d}\tloss: {loss:.5f}\taccuracy: {100*accuracy:.4f}")

        if accuracy > minAcc:
            minAcc = accuracy
            torch.save(model.state_dict(), f"./weights/{model.__class__.__name__}-epoch{epoch}-acc{100*accuracy:.2f}.pt")
            print(f"weights/{model.__class__.__name__}-epoch{epoch}-acc{100*accuracy:.2f}.pt saved!")

        if epoch == epochs-1:
            torch.save(model.state_dict(), f"./weights/{model.__class__.__name__}-last-epoch{epoch}-acc{100*accuracy:.2f}.pt")
            print(f"weights/{model.__class__.__name__}-last-epoch{epoch}-acc{100*accuracy:.2f}.pt saved!")
            

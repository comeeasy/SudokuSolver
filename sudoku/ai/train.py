import torchvision.datasets as datasets
import torchvision.transforms as transforms

import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim

from model import EfficientNet

# download data
mnist_train_data = datasets.MNIST(root="./data",
                                  train=True,
                                  transform=transforms.Compose([
                                      transforms.ToTensor(),
                                      transforms.Resize((100, 100)),
                                      transforms.RandomInvert(0.5),
                                      transforms.RandomAffine(degrees=(5, 10), translate=(0.1, 0.3), scale=(0.5, 0.75)),
                                      transforms.RandomAdjustSharpness(sharpness_factor=2)
                                  ]),
                                  download=True)
mnist_val_data = datasets.MNIST(root="./data",
                                train=False,
                                transform=transforms.Compose([
                                    transforms.ToTensor(),
                                    transforms.Resize((100, 100))
                                ]),
                                download=True)

# DataLoad
mnist_train_dataloader = DataLoader(dataset=mnist_train_data,
                                    shuffle=True,
                                    batch_size=64,
                                    drop_last=True,
                                    num_workers=4)

mnist_val_dataloader = DataLoader(dataset=mnist_val_data,
                                  shuffle=True,
                                  batch_size=64,
                                  drop_last=True,
                                  num_workers=4)

if __name__ == "__main__":
    epochs = 30
    # model = MNISTModel().train().to("cuda")
    model = EfficientNet()
    model.to("cuda")

    print(model.__class__.__name__)

    criteria = nn.CrossEntropyLoss().to("cuda")
    optimizer = optim.Adam(params=model.parameters(), lr=1e-4)


    minAcc = 0
    torch.backends.cudnn.benchmark = True
    model.train()
    for epoch in range(epochs):
        loss = 0
        for img, target in mnist_train_dataloader:
            img = img.to("cuda")
            target = target.to("cuda")

            predict = model(img).to("cuda")
            cost = criteria(predict, target)

            optimizer.zero_grad()
            cost.backward()
            optimizer.step()

            loss += cost / len(mnist_train_dataloader)

        model = model.eval()
        with torch.no_grad():
            accuracy = 0
            for img, target in mnist_val_dataloader:
                img = img.to("cuda")
                target = target.to("cuda")

                predict = model(img).to("cuda")
                correct_predict = torch.argmax(predict, 1) == target
                accuracy += correct_predict.float().mean() / len(mnist_val_dataloader)

        print(f"epoch: {epoch:2d}\tloss: {loss:.5f}\taccuracy: {100*accuracy:.4f}")

        if accuracy > minAcc:
            torch.save(model.state_dict(), f"{model.__class__.__name__}-epoch{epoch}-acc{accuracy:.2f}.pt")
            print(f"weights/{model.__class__.__name__}-epoch{epoch}-acc{accuracy:.2f}.pt saved!")
            

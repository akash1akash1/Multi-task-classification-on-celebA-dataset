# -*- coding: utf-8 -*-
"""M22MA007_PA3_QUESTION1_CODE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pIhB1FSjBzmGObA7kk0AUcISkMnb1OnC
"""

from google.colab import drive
drive.mount('/content/drive')

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision.datasets import CelebA
from torchvision.transforms import transforms
from tqdm import tqdm
import os 
from PIL import Image
from torch.utils.data import Dataset
import numpy as np

!unzip /content/drive/MyDrive/CelebA/Img/img_align_celeba.zip

!ls

class CelebA(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.filenames = []
        self.attributes = []
        self.attribute_names = []
        self.selected_attributes = ['Wearing_Earrings', 'Wearing_Necklace', 'Big_Lips', 'High_Cheekbones', 'Arched_Eyebrows', 'Heavy_Makeup', 'Smiling', 'Young']
        with open(os.path.join(data_dir, '/content/drive/MyDrive/CelebA/Anno/list_attr_celeba.txt'), 'r') as f:
            num_images = int(f.readline().strip())
            self.attribute_names = f.readline().strip().split()
            for i in range(num_images):
                line = f.readline().strip().split()
                self.filenames.append(os.path.join(data_dir, '/content/img_align_celeba', line[0]))
                self.attributes.append([int(line[self.attribute_names.index(attr)+1] == '1') for attr in self.selected_attributes])
        self.attributes = np.array(self.attributes)

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, index):
        image = Image.open(self.filenames[index]).convert('RGB')
        attributes = self.attributes[index]
        if self.transform is not None:
            image = self.transform(image)
        return image, attributes

import torchvision.transforms as transforms
from sklearn.model_selection import train_test_split

transform_train = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
])

transform_val = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
])


dataset = CelebA('./CelebA/', transform_train)

# trainset, valset = train_test_split(dataset, test_size=0.2, random_state=42)
trainset = CelebA('./CelebA/', transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=16, shuffle=True, num_workers=2)
trainloader = tqdm(trainloader, total=len(trainloader))


valset = CelebA('./CelebA/', transform_val)
valloader = torch.utils.data.DataLoader(valset, batch_size=16, shuffle=False, num_workers=2)
valloader = tqdm(valloader, total=len(valloader))

for i, (images, attrs) in enumerate(trainloader):
    print(f"Batch {i}: images shape = {images.shape}, attributes shape = {attrs.shape}")
    i==1
    break

for i, (images, attrs) in enumerate(valloader):
    print(f"Batch {i}: images shape = {images.shape}, attributes shape = {attrs.shape}")
    i==1
    break

print(len(valloader))
print(len(trainloader))

import torchvision.models as models
attributes = ['Wearing_Earrings', 'Wearing_Necklace', 'Big_Lips', 'High_Cheekbones', 'Arched_Eyebrows', 'Heavy_Makeup', 'Smiling', 'Young']

# Define the ResNet18 model architecture
model = models.resnet18(pretrained=True)

# Modify the last layer of the ResNet18 model to output 8 attributes
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 8)

# Define the loss function and optimizer
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

num_attributes=len(attributes)

print(len(attributes))
print(dataset.attribute_names)

# Train the model on the train set and evaluate it on the validation set

attributes = ['Wearing_Earrings', 'Wearing_Necklace', 'Big_Lips', 'High_Cheekbones', 'Arched_Eyebrows', 'Heavy_Makeup', 'Smiling', 'Young']
num_epochs = 5
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)
from tqdm import tqdm

for epoch in range(num_epochs):
    print(f"Epoch {epoch+1}/{num_epochs}")
    for images, labels in trainloader:
        images = images.to(device)
        labels = labels[:,0:8].float().to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        # print(f"Training loss: {loss.item():.4f}")
    
    # Evaluate on validation set
    # Initialize variables for overall accuracy
    overall_correct = 0
    overall_total = 0

    # Evaluate on validation set
    model.eval()
    task_wise_correct = torch.zeros(num_attributes).to(device)
    task_wise_total = torch.zeros(num_attributes).to(device)
    with torch.no_grad():
        for images, labels in valloader:
            images = images.to(device)
            labels = labels[:,0:8].float().to(device)
            outputs = model(images)
            predicted = torch.sigmoid(outputs)
            predicted[predicted >= 0.5] = 1
            predicted[predicted < 0.5] = 0

            # Calculate task-wise accuracy for this batch
            task_wise_correct += (predicted == labels.to(predicted.device)).sum(dim=0)
            task_wise_total += labels.size(0)

            # Calculate overall accuracy for this batch
            overall_correct += (predicted == labels.to(predicted.device)).all(dim=1).sum().item()
            overall_total += labels.size(0)

    # Calculate and print task-wise accuracy
    task_wise_accuracy = task_wise_correct / task_wise_total
    for i, task in enumerate(attributes):
        print(f"{task} accuracy: {task_wise_accuracy[i].item():.4f}")
    print(f"mean of Task-wise accuracy: {task_wise_accuracy.mean().item():.4f}")

    # Calculate and print overall accuracy
    overall_accuracy = overall_correct / overall_total
    print(f"Overall accuracy: {overall_accuracy:.4f}")

# Save the model
torch.save(model.state_dict(), 'model.pth')

import torchvision.models as models
import torch.nn as nn
import torch
from PIL import Image
from torchvision import transforms

# Define the ResNet18 model architecture
model = models.resnet18(pretrained=True)

# Modify the last layer of the ResNet18 model to output 8 attributes
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 8)

# Load the saved model state_dict
model_state_dict = torch.load("/content/model.pth")

# Update the state_dict to match the modified model architecture
new_state_dict = {}
for k, v in model_state_dict.items():
    if k.startswith('fc'):
        continue
    new_state_dict[k] = v
new_state_dict['fc.weight'] = model_state_dict['fc.weight'][:8,:]
new_state_dict['fc.bias'] = model_state_dict['fc.bias'][:8]

# Load the state_dict into the modified model
model.load_state_dict(new_state_dict)

# Put the model in evaluation mode
model.eval()

# Load the image
img_path = "/content/old.jpeg"
img = Image.open(img_path)

# Preprocess the image
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
img_tensor = transform(img)

# Add batch dimension to the tensor
img_tensor = img_tensor.unsqueeze(0)

# Make the prediction
with torch.no_grad():
    output = model(img_tensor)
    predicted = torch.sigmoid(output)

# Print the predicted attributes
attributes = ['Wearing_Earrings', 'Wearing_Necklace', 'Big_Lips', 'High_Cheekbones', 'Arched_Eyebrows', 'Heavy_Makeup', 'Smiling', 'Young']
for i, task in enumerate(attributes):
    print(f"{task}: {'Yes' if predicted[0][i] >= 0.5 else 'No'}")
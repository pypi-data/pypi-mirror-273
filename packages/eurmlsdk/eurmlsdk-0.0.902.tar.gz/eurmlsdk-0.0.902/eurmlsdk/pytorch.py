# from .eur_sdk import EurBaseSDK, ModelNotFound
import timm
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.datasets import CIFAR10
from torchvision.utils import make_grid
import matplotlib.pyplot as plt
import numpy as np
from .eur_sdk import EurBaseSDK

class ModelPytorch(EurBaseSDK):
    def load_model(self, model_path):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = timm.create_model(model_path, pretrained=True)
        save_path = 'resnet50.pth'
        torch.save(model.state_dict(), save_path)
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, 1000)
        model.load_state_dict(torch.load(save_path, map_location=device))
        model.to(device)
        
        transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        test_dataset = CIFAR10(root='./data', train=False, download=True, transform=transform)
        test_dataloader = DataLoader(test_dataset, batch_size=4, shuffle=False)
        return model, device, test_dataset, test_dataloader

    def predict_model(self, model_path):
        model, device, test_dataset, test_dataloader = self.load_model(model_path)
        test_image, _ = test_dataset[0]
        test_image = test_image.unsqueeze(0).to(device)
        model.eval()
        with torch.no_grad():
            outputs = model(test_image)
            _, predicted = torch.max(outputs, 1 )
            return predicted
        
    def validate_model(self, model_path):
        model, device, test_dataset, test_dataloader = self.load_model(model_path)
        model.eval()
        total=0
        correct=0
        with torch.no_grad():
            for images, labels in test_dataloader:
                images = images.to(device)
                labels = labels.to(device)
                output = model(images)
                _, predicted = torch.max(output, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        accuracy = correct/total
        return accuracy
    
    def get_predicted_results(self, results):
        list_predicted_set = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
        predictied_values = list(map(int, results[0]))
        print(predictied_values)
        for res in predictied_values:
            print("Predicted_result :", list_predicted_set[res]) 


 


    # def loadModel(self, model_path):
    #     modelFile = self.get_model(model_path)
    #     if modelFile != "":
    #         print("model loading is yet to start")
    #         model = torch.hub.load(model_path)
    #         print("model loading ended")
    #         model.eval()
    #         return model 
    #     else: 
    #         raise ModelNotFound()

    # def predictModel(self, model_path, dataset):
    #     try:
    #         print("setPredection")
    #         model = self.loadModel(model_path)
    #         print("PyTorch Predection started.......")
    #         predection = self.get_prediction(model, dataset)
    #         labelClass = self.loadLabels("image-net.txt")
    #         print(labelClass[predection.item()])
    #     except ModelNotFound as err:
    #         print("Error :", err)
    #         exit(1)
    #     except Exception as err:
    #         print ("Error in Predection :", err)
    #         exit(1)
    
    # def loadLabels(self, file_path):
    #     with open(file_path) as label:  
    #         predection_list = [data.strip() for data in label.readlines()]
    #     return predection_list

    # def get_prediction(self, model, image):
    #     print("get predection result index invoked")
    #     with torch.no_grad():
    #         output = model(image)
    #     _, predicted = torch.max(output, 1)
    #     print(predicted)
    #     return predicted


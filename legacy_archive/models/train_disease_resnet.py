import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
import os

# Config
DATA_DIR = "models/data/disease_patches"
MODEL_DIR = "models/artifacts"
MODEL_PATH = os.path.join(MODEL_DIR, "disease_resnet18.pth")
BATCH_SIZE = 16
EPOCHS = 5 # Short run for demo

def train_disease_model():
    print("[INFO] Starting ResNet-18 Disease Model Training...")
    
    if not os.path.exists(DATA_DIR):
        print(f"[ERROR] Data directory {DATA_DIR} not found. Run synthetic_data_generator.py first.")
        return

    # Transforms
    # ResNet expects 224x224 usually, but we can adapt or resize.
    # Our synthetic data is 64x64. We will resize to 224 for standard ResNet compatibility.
    data_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # Load Data
    try:
        dataset = datasets.ImageFolder(DATA_DIR, transform=data_transforms)
    except Exception as e:
         print(f"[ERROR] Failed to load dataset: {e}. Ensure 'Healthy' and 'Stressed' folders exist.")
         return

    dataloader = torch.utils.data.DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    class_names = dataset.classes
    print(f"[INFO] Classes found: {class_names}")
    
    # Model Setup (Transfer Learning)
    # We use a pretresioned ResNet18 and modify the final layer
    model = models.resnet18(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 2) # Binary Classification
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    
    # Training Loop
    model.train()
    for epoch in range(EPOCHS):
        running_loss = 0.0
        correct = 0
        total = 0
        
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
        epoch_acc = 100 * correct / total
        print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {running_loss/len(dataloader):.4f} - Acc: {epoch_acc:.2f}%")
        
    # Save Model
    os.makedirs(MODEL_DIR, exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"[INFO] Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_disease_model()

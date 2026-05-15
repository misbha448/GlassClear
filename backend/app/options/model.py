import torch
import torchvision.models as models
from torchvision.models import ResNet18_Weights
from PIL import Image
import torchvision.transforms as transforms
import torch.nn.functional as F
import os

# ✅ Load pretrained model (updated way)
model = models.resnet18(weights=ResNet18_Weights.DEFAULT)
model.eval()

# ✅ Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# ✅ Load labels safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
labels_path = os.path.join(BASE_DIR, "imagenet_classes.txt")

with open(labels_path) as f:
    labels = [line.strip() for line in f.readlines()]

# ✅ Prediction function
def predict(image: Image.Image):
    img = transform(image).unsqueeze(0)
    
    with torch.no_grad():
        output = model(img)

    # probabilities
    probs = F.softmax(output, dim=1)

    # top prediction
    top_prob, top_idx = torch.max(probs, 1)

    return {
        "label": labels[top_idx.item()],
        "confidence": round(top_prob.item() * 100, 2)
    }
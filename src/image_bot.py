# src/image_bot.py
import ssl
import torch
from PIL import Image
from torchvision import models

# Global variables for caching model [cite: 712]
_model = None
_labels = None
_preprocess = None

def _load_model():
    """Loads the model and labels only when needed."""
    global _model, _labels, _preprocess
    
    if _model is None:
        print("Loading ResNet50 model... please wait.")
        weights = models.ResNet50_Weights.DEFAULT
        try:
            _model = models.resnet50(weights=weights)
        except Exception as exc:
            # Retry with an unverified SSL context for macOS cert issues.
            if "CERTIFICATE_VERIFY_FAILED" in str(exc):
                ssl._create_default_https_context = ssl._create_unverified_context
                _model = models.resnet50(weights=weights)
            else:
                raise
        _model.eval()

        _labels = weights.meta["categories"]
        _preprocess = weights.transforms()

def describe_image(image_path: str) -> str:
    """
    Classifies an image and returns a templated description.
    """
    global _model, _labels, _preprocess
    
    try:
        # Load model on first run
        _load_model()
        
        # Open and convert image [cite: 723]
        img = Image.open(image_path).convert("RGB")
        
    except Exception as e:
        return (f"[label]\nunknown\n"
                f"[description]\nCould not read image: {e}\n"
                f"[meaning]\nN/A")

    # Inference
    with torch.no_grad():
        inp = _preprocess(img).unsqueeze(0)
        logits = _model(inp)
        pred = logits.softmax(dim=1).argmax(dim=1).item()
        
        # Get label
        label = _labels[pred] if _labels and 0 <= pred < len(_labels) else "unknown object"

    # Templated output as per Offline Track requirements [cite: 528]
    description = f"An image likely containing: {label}."
    meaning = (
        f"The term '{label}' refers to a common object or concept categorized by the "
        "ResNet50 image classifier. It identifies the dominant visual feature."
    )

    return (
        f"[label]\n{label}\n"
        f"[description]\n{description}\n"
        f"[meaning]\n{meaning}"
    )
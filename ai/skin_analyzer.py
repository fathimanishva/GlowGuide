from PIL import Image
from transformers import pipeline


# Load the pretrained skin-type classification model
skin_classifier = pipeline(
    "image-classification",
    model="dima806/skin_types_image_detection"
)


def analyze_skin(image_path):

    image = Image.open(image_path).convert("RGB")

    results = skin_classifier(image)

    return results
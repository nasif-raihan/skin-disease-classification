import base64
import io
import json

import torch
import torchvision.transforms as transforms
from PIL import Image
from django.http import JsonResponse
from django.views import View
from environs import Env

env = Env()
env.read_env()


class PredictImageView(View):
    def __init__(self):
        super().__init__()
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Load the model with map_location to ensure it's loaded on the correct device
        self.__model = torch.load(env.str("MODEL_PATH"), map_location=self.__device)
        self.__classes = (
            "Melanoma Skin Cancer Nevi and Moles",
            "Seborrheic Keratoses and other Benign Tumors",
            "Lupus and other Connective Tissue diseases",
            "Hair Loss Photos Alopecia and other Hair Diseases",
            "Psoriasis pictures Lichen Planus and related d...",
            "Tinea Ringworm Candidiasis and other Fungal In...",
            "Warts Molluscum and other Viral Infections",
            "Herpes HPV and other STDs Photos",
            "Poison Ivy Photos and other Contact Dermatitis",
            "Actinic Keratosis Basal Cell Carcinoma and oth...",
            "Scabies Lyme Disease and other Infestations an...",
            "Exanthems and Drug Eruptions",
            "Vascular Tumors",
            "Nail Fungus and other Nail Disease",
            "Vasculitis Photos",
            "Urticaria Hives",
            "Systemic Disease",
            "Bullous Disease Photos",
            "Cellulitis Impetigo and other Bacterial Infect...",
            "Eczema Photos",
            "Light Diseases and Disorders of Pigmentation",
            "Atopic Dermatitis Photos",
            "Acne and Rosacea Photos",
        )

    def post(self, request) -> JsonResponse:
        try:
            payload = json.loads(request.body)
            image_data = payload.get("image_base64")
            if not image_data:
                return JsonResponse({"error": "No image data provided"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        try:
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            return JsonResponse({"error": "Invalid image data"}, status=400)

        transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

        image_tensor = transform(image)
        image_tensor = image_tensor.to(self.__device)

        try:
            predicted_class = self.predict_image_class(image_tensor)
            return JsonResponse({"predicted_class": predicted_class}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def predict_image_class(
        self, image_tensor: torch.Tensor, normalize: bool = True
    ) -> str:
        self.__model.eval()
        with torch.no_grad():
            if normalize:
                image_tensor = (image_tensor - image_tensor.mean()) / image_tensor.std()

            image_tensor = image_tensor.to(self.__device)
            outputs = self.__model(image_tensor.unsqueeze(0))
            predicted = torch.argmax(outputs.data, -1)
            prediction = predicted.cpu().numpy()

        return self.__classes[prediction[0]]

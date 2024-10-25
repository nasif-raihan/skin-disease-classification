# Skin Disease Classification

This project demonstrates the deployment of a skin disease classification model as an image classification API. The provided model is a dummy pretrained model intended for demonstration purposes only, and is sourced from the [Skin Diseases Classification Dermnet project](https://github.com/yuliyabohdan/Skin-diseases-classification-Dermnet-). Due to limited training (1 iteration), the model's predictions may not be accurate, but this setup provides a foundation for further development and tuning.

## Project Overview

The project is designed to classify skin disease images by deploying a deep learning model with Docker and Django. It provides an API endpoint that accepts a base64-encoded image and returns the predicted class of the skin disease.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### 1. Environment Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/skin-disease-classification
   cd skin-disease-classification
   ```

2. Copy the `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

   Update any necessary environment variables in the `.env` file, such as `MODEL_PATH`.

### 2. Docker Deployment

Build and start the project with Docker Compose:
```bash
docker compose up --build
```

This will build the Docker image, install dependencies, and start the Django development server.

## Usage

1. **Prepare the Image Payload**

   Convert your image to base64 encoding using the following command:
   ```bash
   base64 -w 0 weight/Nail-Disease-BedRidges.jpg > weight/encoded_image.txt
   ```

2. **Create the API Payload**

   Use the contents of `encoded_image.txt` as the value for the `"image_base64"` key:
   ```json
   {
       "image_base64": "/9j/4AAQSkZJRgABAQEAYABgAAD/"
   }
   ```

3. **Send the Request**

   Send a POST request to the `/predict/` endpoint. Here is a sample request using `curl`:

   ```bash
   curl -X POST http://0.0.0.0:8000/predict/ \
        -H "Content-Type: application/json" \
        -d '{"image_base64": "/9j/4AAQSkZJRgABAQEAYABgAAD/"}'
   ```

4. **Expected Output**
   The API will return a JSON response with the predicted class:
   ```json
   {
       "predicted_class": "Vascular Tumors"
   }
   ```

## Model Information

The model used here is a basic pretrained model downloaded from the original [Skin Diseases Classification Dermnet GitHub repository](https://github.com/yuliyabohdan/Skin-diseases-classification-Dermnet-). To enhance accuracy, we recommend further fine-tuning the model using additional training epochs and domain-specific data.

## Additional Notes

- **Model Training**: The pretrained model is stored in the `weights` directory as `pretrained_dummy_model.pth`. Since it was only trained for a single iteration, it may produce inaccurate results. The objective is to demonstrate the deployment pipeline rather than model accuracy.
- **Extending the Model**: For more accurate classification, please refer to the original repository linked above, where you can perform further model training and fine-tuning for better accuracy.

## License

This project is for educational and demonstration purposes. For licensing information related to the pretrained model, please refer to the original repository.

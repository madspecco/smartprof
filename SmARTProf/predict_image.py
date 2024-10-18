from keras import models
from PIL import Image
import numpy as np


# Load the saved model
model = models.load_model('models//doody_v1_2.keras')


def prepare_image(image_path):
    image = Image.open(image_path).resize((50, 50)).convert("L")
    image_array = np.array(image)
    return image_array / 255.0


def get_predicted_class(path_to_drawing):
    # Load and preprocess the image
    image_path = path_to_drawing
    image_array = prepare_image(image_path)
    image_array = image_array.reshape(1, 50, 50, 1)

    # Predict the class
    prediction = model.predict(image_array)
    predicted_class = np.argmax(prediction)
    return predicted_class

import tensorflow as tf
from keras.preprocessing import image
import numpy as np
import os

model = tf.keras.models.load_model("model/bone_fracture_model.h5")

def predict_fracture(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0) / 255.0

    prediction = model.predict(img_tensor)
    class_idx = np.argmax(prediction)

    classes = ["No Fracture", "Fracture"]
    recommendations = [
        "No fracture detected. No treatment needed.",
        "Fracture detected. Consult an orthopedic doctor immediately."
    ]

    return classes[class_idx], recommendations[class_idx]

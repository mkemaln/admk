from flask import Flask, request, jsonify
import tensorflow as tf
import base64
import numpy as np
from PIL import Image
from io import BytesIO
import logging

app = Flask(__name__)
model = tf.keras.models.load_model('rwn-epc10v2.keras')

class_names = ['Bacterial Spot', 'Early Blight', 'Healthy', 'Late Blight', 'Leaf Mold', 'Mosaic Virus', 'Septoria Leaf Spot', 'Spider Mites', 'Target Spot', 'Yellow Leaf Curl Virus']


# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # logging.info("Received request data: %s", data)  # Log the received data

        image_data = data['image']  # Assuming you send the image under the key 'image'
        logging.info("Received image data of length: %d", len(image_data))  # Log the length of the image data

        # Decode the base64 image
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        logging.info("Decoded image size: %s", image.size)
        # Preprocess the image as required by your model
        image = image.resize((180, 180))  # Resize to the input shape of your model
        # image_array = np.array(image) / 255.0  # Normalize if required
        # image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension if required
        image_array = tf.keras.utils.img_to_array(image)
        image_array = tf.expand_dims(image_array, 0) # Create a batch

        # Make prediction
        prediction = model.predict(image_array)
        score = tf.nn.softmax(prediction[0])
        predicted_class_index = np.argmax(score)  # Get the index of the class with the highest probability
        predicted_label = class_names[predicted_class_index]  # Map index to label

        logging.info("Predicted label: %s", predicted_label)  # Log the predicted label
        logging.info("Accuracy: %s", 100 * np.max(score))  # Log the predicted label

        # Return the predicted label as a plain string
        return predicted_label, 200  # Return the label and HTTP status code 200
    except KeyError as e:
        logging.error("Missing key: %s", str(e))  # Log the error
        return f'Missing key: {str(e)}', 400  # Return error message as string
    except Exception as e:
        logging.error("Error occurred: %s", str(e))  # Log the error
        return str(e), 500  # Return error message as string
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

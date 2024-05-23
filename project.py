from flask import Flask, render_template, request, Response
from PIL import Image
from ultralytics import YOLO
import io
from flask_cors import CORS 
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}}) 

# Load your YOLO model
def load_model():
    # Load your YOLO model here
    model = YOLO("best.pt", "yolov8")  # Update the path and model name accordingly
    return model

# Perform inference on the input image
def inference(model, image):
    # Perform inference using the YOLO model
    detection_output = model.predict(image)  # Predict with confidence threshold of 0.25
    
    # Get the PIL image with bounding boxes drawn by the model
    boxes = detection_output[0].boxes
    res_plotted = detection_output[0].plot()[:,:,::-1]
    
    # Convert numpy array to bytes
    image_bytes = io.BytesIO()
    Image.fromarray(np.uint8(res_plotted)).save(image_bytes, format='JPEG')
    image_bytes.seek(0)
    
    # Return the image bytes
    return image_bytes.getvalue()

# Home page route
@app.route('/')
def home():
    return render_template('result.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Access the uploaded image file
        image_file = request.files['image']
        
        # Read the image file
        image = Image.open(image_file)
        
        # Load the YOLO model
        model = load_model()
        
        # Perform inference on the image using the YOLO model
        result_image_bytes = inference(model, image)
        
        # Return the result image as bytes
        return Response(result_image_bytes, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
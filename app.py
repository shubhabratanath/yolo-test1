from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import Flask-CORS
import io
import cv2
import os
from ultralytics import YOLO
from PIL import Image
import numpy as np

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for all routes (default behavior)

# Load your model (only once at startup)
model = YOLO('best.pt')

def detect_objects(image_bytes):
    try:
        img = Image.open(image_bytes)
        img_np = np.array(img)
        img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        results = model.predict(source=img_cv)
        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls)
                confidence = float(box.conf)
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({
                    'class': result.names[class_id],
                    'confidence': confidence,
                    'bbox': [x1, y1, x2, y2]
                })
        return detections
    except Exception as e:
        print(f"Error during detection: {e}") # Print the exception for debugging
        return []

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    try:
        image_bytes = io.BytesIO(image_file.read())
        detections = detect_objects(image_bytes)
        return jsonify({'detections': detections}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('.', 'index.html') # Serve index.html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

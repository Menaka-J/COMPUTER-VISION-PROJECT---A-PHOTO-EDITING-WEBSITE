from flask import Flask, request, jsonify, send_file, render_template
import cv2
import numpy as np
import os
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home route
@app.route('/')
def home():
    return render_template('page1.html')

# Routes for additional pages
@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')


# Route to upload an image
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, 'uploaded_image.png')
    image.save(filepath)

    return jsonify({'message': 'Image uploaded successfully'}), 200

# Apply transformations
def apply_transformation(image, action):
    if action == 'rotate':
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif action == 'flip':
        image = cv2.flip(image, 1)
    elif action == 'grayscale':
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif action == 'blur':
        image = cv2.GaussianBlur(image, (15, 15), 0)
    elif action == 'brightness':
        image = cv2.convertScaleAbs(image, alpha=1.5, beta=30)
    elif action == 'contrast':
        image = cv2.convertScaleAbs(image, alpha=2.0, beta=0)

    return image

# Route to apply filters or transformations
@app.route('/edit', methods=['POST'])
def edit_image():
    action = request.form.get('action')

    if not action:
        return jsonify({'error': 'No action specified'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, 'uploaded_image.png')
    if not os.path.exists(filepath):
        return jsonify({'error': 'No uploaded image found'}), 404

    image = cv2.imread(filepath)
    image = apply_transformation(image, action)

    edited_filepath = os.path.join(UPLOAD_FOLDER, 'edited_image.png')
    cv2.imwrite(edited_filepath, image)

    return send_file(edited_filepath, mimetype='image/png')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
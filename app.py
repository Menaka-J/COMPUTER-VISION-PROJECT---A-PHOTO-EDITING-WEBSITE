from flask import Flask, request, jsonify, send_from_directory, render_template
import numpy as np
import cv2
import base64
import os

app = Flask(__name__, static_folder='.')

def base64_to_img(base64_str):
    header_removed = base64_str.split(',')[1] if ',' in base64_str else base64_str
    img_bytes = base64.b64decode(header_removed)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
    return img

def img_to_base64(img):
    _, buf = cv2.imencode('.png', img)
    return "data:image/png;base64," + base64.b64encode(buf).decode('utf-8')

# --- Editing Functions (same as your code, no major changes) ---

# [Keep all your image functions unchanged here: brightness, contrast, hue, blur, etc.]

# Editing functions

def adjust_brightness(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    v = np.clip(v.astype(np.int32) + int(value*255), 0, 255).astype(np.uint8)
    hsv = cv2.merge([h,s,v])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def adjust_contrast(img, alpha):
    # alpha >1 increase contrast, 0..1 decrease contrast
    img = img.astype(np.float32)
    img = img * alpha
    img = np.clip(img, 0, 255)
    return img.astype(np.uint8)

def adjust_exposure(img, value):
    # Exposure approximately handled as brightness adjustment
    return adjust_brightness(img, value)

def adjust_highlights(img, value):
    # Simplified: apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l,a,b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0+value*10)
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return img

def adjust_hue(img, degree):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    h = (h.astype(np.int32) + degree) % 180
    hsv = cv2.merge([h.astype(np.uint8), s, v])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def adjust_saturation(img, scale):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    s = np.clip(s.astype(np.float32) * scale, 0, 255).astype(np.uint8)
    hsv = cv2.merge([h,s,v])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def adjust_luminance(img, scale):
    # Approximate luminance by scaling V channel in HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    v = np.clip(v.astype(np.float32) * scale, 0, 255).astype(np.uint8)
    hsv = cv2.merge([h,s,v])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def apply_color_grading(img, scale):
    # Placeholder, just increasing saturation for demo
    return adjust_saturation(img, scale)

def apply_blur(img, kernel_size):
    if kernel_size % 2 == 0:
        kernel_size += 1  # Kernel size must be odd
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def noise_reduction(img, strength):
    return cv2.fastNlMeansDenoisingColored(img, None, strength*10, strength*10, 7, 21)

def smoothness(img, strength):
    # Bilateral filter for smoothness
    return cv2.bilateralFilter(img, d=9, sigmaColor=75*strength, sigmaSpace=75*strength)

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def sepia(img):
    kernel = np.array([[0.272,0.534,0.131],
                      [0.349,0.686,0.168],
                      [0.393,0.769,0.189]])
    sepia_img = cv2.transform(img, kernel)
    sepia_img = np.clip(sepia_img,0,255).astype(np.uint8)
    return sepia_img

def negative(img):
    return cv2.bitwise_not(img)

def fade(img, alpha):
    white = np.full(img.shape, 255, dtype=np.uint8)
    return cv2.addWeighted(img, alpha, white, 1 - alpha, 0)

def sharpen(img):
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    return cv2.filter2D(src=img, ddepth=-1, kernel=kernel)

def clarity(img, strength):
    blurred = cv2.GaussianBlur(img, (0,0), sigmaX=3)
    return cv2.addWeighted(img, 1 + strength, blurred, -strength, 0)

def resize_canvas(img, aspect_ratio):
    h, w = img.shape[:2]
    target_ratios = {
        "1:1": 1,
        "4:5": 4/5,
        "9:16": 9/16,
        "16:9": 16/9
    }
    if aspect_ratio not in target_ratios:
        return img
    target_ratio = target_ratios[aspect_ratio]
    current_ratio = w / h

    if current_ratio > target_ratio:
        # crop width
        new_w = int(h * target_ratio)
        start_x = (w - new_w)//2
        img = img[:, start_x:start_x+new_w]
    else:
        # crop height
        new_h = int(w / target_ratio)
        start_y = (h - new_h)//2
        img = img[start_y:start_y+new_h, :]

    return img

def apply_custom_filter(img, filter_type):
    # Placeholder: implement different filters based on filter_type string
    if filter_type=="highlight_color":
        overlay = img.copy()
        overlay[:] = (0, 255, 255)  # Cyan overlay for highlights as example
        return cv2.addWeighted(img, 0.7, overlay, 0.3, 0)
    elif filter_type=="shadows":
        # Darken shadows - simple gamma correction
        gamma = 0.5
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(img, table)
    else:
        return img

def add_frame(img, frame_type):
    # Placeholder: add a simple border frame
    if frame_type=="border":
        return cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[0,0,0])
    else:
        return img

def crop_image(img, x, y, w, h):
    return img[y:y+h, x:x+w]

def rotate_image(img, angle):
    h, w = img.shape[:2]
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w,h))
    return rotated

def flip_image(img, horizontal=True):
    if horizontal:
        return cv2.flip(img, 1)
    else:
        return cv2.flip(img, 0)

def create_collage(images, layout='grid'):
    # For simplicity, create horizontal collage
    return cv2.hconcat(images) if images else None


@app.route('/')
def home():
    return render_template('page1.html')

@app.route('/page2.html')
def serve_page2():
    return render_template('page2.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/edit', methods=['POST'])
def edit():
    data = request.get_json()
    image_b64 = data.get('image')
    edits = data.get('edits', {})

    if not image_b64:
        return jsonify({"error": "No image provided"}), 400

    img = base64_to_img(image_b64)
    if img is None:
        return jsonify({"error": "Invalid image data"}), 400

    try:
        if 'brightness' in edits:
            img = adjust_brightness(img, edits['brightness'])
        if 'contrast' in edits:
            img = adjust_contrast(img, edits['contrast'])
        if 'exposure' in edits:
            img = adjust_exposure(img, edits['exposure'])
        if 'highlights' in edits:
            img = adjust_highlights(img, edits['highlights'])
        if 'hue' in edits:
            img = adjust_hue(img, int(edits['hue']))
        if 'saturation' in edits:
            img = adjust_saturation(img, edits['saturation'])
        if 'luminance' in edits:
            img = adjust_luminance(img, edits['luminance'])
        if 'color_grading' in edits:
            img = apply_color_grading(img, edits['color_grading'])
        if 'blur' in edits:
            img = apply_blur(img, int(edits['blur']))
        if 'noise_reduction' in edits:
            img = noise_reduction(img, int(edits['noise_reduction']))
        if 'smoothness' in edits:
            img = smoothness(img, edits['smoothness'])
        if 'grayscale' in edits and edits['grayscale']:
            img = grayscale(img)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if 'sepia' in edits and edits['sepia']:
            img = sepia(img)
        if 'negative' in edits and edits['negative']:
            img = negative(img)
        if 'fade' in edits:
            img = fade(img, edits['fade'])
        if 'sharpening' in edits:
            img = sharpen(img)
        if 'clarity' in edits:
            img = clarity(img, edits['clarity'])
        if 'aspect_ratio' in edits:
            img = resize_canvas(img, edits['aspect_ratio'])
        if 'custom_filter' in edits:
            img = apply_custom_filter(img, edits['custom_filter'])
        if 'frame' in edits:
            img = add_frame(img, edits['frame'])
        if 'crop' in edits:
            c = edits['crop']
            img = crop_image(img, c['x'], c['y'], c['width'], c['height'])
        if 'rotate' in edits:
            img = rotate_image(img, edits['rotate'])
        if 'flip_horizontal' in edits and edits['flip_horizontal']:
            img = flip_image(img, True)
        if 'flip_vertical' in edits and edits['flip_vertical']:
            img = flip_image(img, False)

    except Exception as e:
        return jsonify({"error": f"Editing error: {str(e)}"}), 500

    result_img_b64 = img_to_base64(img)
    return jsonify({"edited_image": result_img_b64})



if __name__ == "__main__":
    app.run(debug=True)

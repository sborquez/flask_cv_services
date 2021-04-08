from flask import current_app
import cv2
import numpy as np
import io
import base64
from PIL import Image

#SERVICES_URL = "http://localhost:5000" #todo add to configuration
SERVICES_URL = None # Use same host

def get_url(service_name):
    return f"{SERVICES_URL or ''}/api/{service_name}"


cv_services = {
    "gray": {
        "name": "Gray Scale",
        "url": get_url("gray"),
        "description": "Convert image to gray scale.",
        "image_url": None,
        #"request": None,
        #"respond": None,
    }
}

def convert_to_image(encoded_image):
    "Convert encoded image from request to pillow image."
    img_arr =  np.fromstring(encoded_image, np.uint8)
    image = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    return image

def convert_to_base64(image, img_format="JPEG"):
    "Convert image to base64 encoded."
    image = Image.fromarray(image.astype("uint8"))
    rawBytes = io.BytesIO()
    image.save(rawBytes, img_format)
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return img_base64

def gray(image):
    "Convert image to gray scale."
    err = None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);
    return err, gray
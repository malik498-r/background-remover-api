from flask import Flask, request, jsonify, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "working"})

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    input_image = Image.open(image_file.stream)
    output_image = remove(input_image)

    output_bytes = io.BytesIO()
    output_image.save(output_bytes, format="PNG")
    output_bytes.seek(0)

    return send_file(output_bytes, mimetype="image/png")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

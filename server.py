from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.post("/remove-bg")
def remove_bg():
    if 'image' not in request.files:
        return {"error": "No image uploaded"}, 400

    img = request.files['image'].read()
    output = remove(img)

    return send_file(
        io.BytesIO(output),
        mimetype='image/png',
        download_name='removed.png'
    )

@app.get("/")
def home():
    return {"status": "Background Remover API Running!"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

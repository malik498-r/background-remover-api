from flask import Flask, request, send_file
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

app = Flask(__name__)

def remove_bg(img):
    # simple grabcut
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    h, w = img.shape[:2]
    rect = (10,10,w-20,h-20)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,np.newaxis]
    return img

@app.route('/remove-bg', methods=['POST'])
def api():
    file = request.files['image']
    img = Image.open(file.stream).convert("RGB")
    img_np = np.array(img)
    out = remove_bg(img_np)
    out_img = Image.fromarray(out)
    buf = BytesIO()
    out_img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

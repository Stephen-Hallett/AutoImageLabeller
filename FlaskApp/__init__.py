from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import os
import cv2 as cv
from .handle_image_upload import handle_upload

UPLOAD_FOLDER = 'uploads'

if not os.path.exists(os.path.join(".",UPLOAD_FOLDER)):
    os.mkdir(os.path.join(".",UPLOAD_FOLDER))

app = Flask(__name__)
app.config[ 'UPLOAD_FOLDER' ] = UPLOAD_FOLDER

@app.route('/upload-image', methods=[ 'GET', 'POST' ])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    else:
        main_img = request.files[ 'file' ]
        obj = request.files[ 'object' ]
        label = request.form[ 'label' ]

        filename = secure_filename(main_img.filename)
        obj_filename = secure_filename(obj.filename)
        main_img.save(os.path.join(app.config[ 'UPLOAD_FOLDER' ], filename))
        obj.save(os.path.join(app.config[ 'UPLOAD_FOLDER' ], obj_filename))
        result_path = handle_upload(os.path.join(app.config[ 'UPLOAD_FOLDER' ], filename), 
                               os.path.join(app.config[ 'UPLOAD_FOLDER' ], obj_filename), 
                               label, 
                               remove=True)
        if result_path and os.path.exists(result_path):
            #return send_file(result_path, mimetype='image/jpg'), 200
            return "Image upload successful!", 200
        else:
            return 'Error processing the image', 500

if __name__ == '__main__':
    app.run(debug=True)
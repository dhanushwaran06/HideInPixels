from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
from steganography import encode_message, decode_message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create the uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        if 'image' not in request.files or 'message' not in request.form or 'key' not in request.form:
            flash('No file, message, or key found')
            return redirect(request.url)

        image_file = request.files['image']
        message = request.form['message']
        key = request.form['key']

        if image_file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)

            encoded_image_path = encode_message(image_path, message, key)

            return redirect(url_for('result', filename=os.path.basename(encoded_image_path), mode='encode'))

    return render_template('encode.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        if 'image' not in request.files or 'key' not in request.form:
            flash('No file or key found')
            return redirect(request.url)

        image_file = request.files['image']
        key = request.form['key']

        if image_file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)

            decoded_message = decode_message(image_path, key)

            if decoded_message is not None:
                return render_template('result.html', filename=filename, mode='decode', message=decoded_message)
            else:
                flash('Incorrect key or no message found in image')
                return redirect(request.url)

    return render_template('decode.html')

@app.route('/result/<filename>/<mode>')
def result(filename, mode):
    return render_template('result.html', filename=filename, mode=mode)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)

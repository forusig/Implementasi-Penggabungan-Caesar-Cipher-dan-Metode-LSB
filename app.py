# app.py
from flask import Flask, render_template, request, redirect, url_for
from stegano import lsb
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def caesar_encrypt(text, shift):
    encrypted_text = ""
    text = text.lower()

    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char_index = ord(char) - ord('a')
            char_index = (char_index + shift) % 26
            encrypted_char = chr(char_index + ord('a'))
            if is_upper:
                encrypted_char = encrypted_char.upper()
            encrypted_text += encrypted_char
        else:
            encrypted_text += char

    return encrypted_text

def caesar_decrypt(encrypted_text, shift):
    decrypted_text = ""
    encrypted_text = encrypted_text.lower()

    for char in encrypted_text:
        if char.isalpha():
            is_upper = char.isupper()
            char_index = ord(char) - ord('a')
            char_index = (char_index - shift + 26) % 26
            decrypted_char = chr(char_index + ord('a'))
            if is_upper:
                decrypted_char = decrypted_char.upper()
            decrypted_text += decrypted_char
        else:
            decrypted_text += char

    return decrypted_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        plaintext = request.form['plaintext']
        shift = int(request.form['shift'])

        if 'image' not in request.files:
            return redirect(request.url)
        image = request.files['image']
        if image.filename == '':
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = image.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            encrypted_text = caesar_encrypt(plaintext, shift)
            result_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'hasil.png')
            lsb.hide(image_path, encrypted_text).save(result_image_path)
            decrypted_text = caesar_decrypt(encrypted_text, shift)

            return render_template('result.html', encrypted_text=encrypted_text, decrypted_text=decrypted_text, image_path=result_image_path)

    return render_template('index.html')

@app.route('/decryption', methods=['GET', 'POST'])
def decryption():
    decrypted_text = ""

    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)

        image = request.files['image']
        if image.filename == '':
            return redirect(request.url)

        if image and allowed_file(image.filename):
            # Simpan gambar yang akan didekripsi
            filename = image.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            # Ekstrak pesan tersembunyi dari gambar menggunakan steganografi LSB
            decrypted_text = lsb.reveal(image_path)

    return render_template('decryption.html', decrypted_text=decrypted_text)


if __name__ == '__main__':
    app.run(debug=True)

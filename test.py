from flask import Flask, request, render_template
import sqlite3
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['image']
        image = Image.open(file)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO images (name, data) VALUES (?, ?)", (file.filename, image.tobytes()))
        conn.commit()
        conn.close()
        return 'Image uploaded successfully'

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
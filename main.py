from flask import render_template, request, Flask, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from colorthief import ColorThief
import os



app = Flask(__name__)
app.secret_key = "smell"

app.config['UPLOAD_FOLDER'] = "static/images/display_image"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        image = request.files['file']
        if image.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = f"static/images/display_image/{image.filename}"
            color_thief = ColorThief(file_path)
            top_colors = color_thief.get_palette(color_count=11)
            return render_template("image.html", path=file_path, colors=top_colors)
        else:
            flash('Allowed image types are - png, jpg, jpeg')
            return redirect(request.url)
    else:
        return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)

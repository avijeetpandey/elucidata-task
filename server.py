from flask import Flask , request 
from flask import render_template

from werkzeug.utils import secure_filename

# creating the flask application named app
app=Flask(__name__,static_url_path='',static_folder='web/static',template_folder='web/templates')

# intial route when server is hit first
@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/upload',methods=['POST'])
def upload():
    if request.method == 'POST':
        # checking of the post request has the file part
        if 'file' not in request.files:
            print("No file found")
            return "OOPS No File Uploaded"
        file = request.files['file']
        if file :
            fileName = secure_filename(file.filename)
            print(fileName)
            return fileName

# running the application
app.run(debug=True)
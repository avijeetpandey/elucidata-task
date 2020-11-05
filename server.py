import os
from flask import Flask, request , jsonify , make_response 
from flask import render_template
from werkzeug.utils import secure_filename
import pandas as pd

# defining folder configuration for uploaded data
UPLOAD_FOLDER = 'uploads/'

# creating the flask application named app
app = Flask(__name__, static_url_path='',static_folder='web/static', template_folder='web/templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# intial route when server is hit first
@app.route('/')
def hello():
    return render_template('index.html')


# API end point to upload the file and save it to the server for future use
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # checking of the post request has the file part
        if 'file' not in request.files:
            print("No file found")
            return "OOPS No File Uploaded"
        file = request.files['file']
        if file:
            fileName = secure_filename(file.filename)
# checking if uploads folder exists or not
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
            return "File Uploaded Succesfully"


# API endpoint to filter the file compound id
@app.route('/filter', methods=['GET'])
def filter():
# creating the dataframe
    df = pd.read_excel('uploads/mass_spec_data_assgnmnt.xlsx.xlsx')
# creating the child dataset for PC
    pc_dataset = df[df['Accepted Compound ID'].str.contains(r'\bPC\b', na=False)]
# creating the child dataset for LPC
    lpc_dataset = df[df['Accepted Compound ID'].str.contains(r'\bLPC\b', na=False)]
# creating the child dataset for plasmalogen
    plasmogen_dataset = df[df['Accepted Compound ID'].str.contains(r'\bplasmalogen\b', na=False)]
  
# row counts of the datasets 
    pc_row = pc_dataset.shape[0]
    lpc_row = lpc_dataset.shape[0]
    plasmogen_row = plasmogen_dataset.shape[0]

# creating suitable response to be return back to the client
    response = make_response(
        jsonify({
            "PC count" : pc_row,
            "LPC count" : lpc_row,
            "Plasmogent count" : plasmogen_row
        })
    )
    response.headers["Content-Type"] = "application/json"
    
    return response

# running the application
app.run(debug=True)

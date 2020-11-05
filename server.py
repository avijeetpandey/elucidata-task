import os
from flask import Flask, request , jsonify , make_response , send_file 
from flask import render_template
from werkzeug.utils import secure_filename
import pandas as pd

from zipfile import ZipFile
import io

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
    pc_dataset =df[(df['Accepted Compound ID'].str.endswith('PC',na=False)) & (df['Accepted Compound ID'].str[-3]!='L')]
    pc_dataset.to_csv('PC.csv',index=False)
    
    # creating the child dataset for LPC
    lpc_dataset =df[df['Accepted Compound ID'].str.endswith('LPC',na=False)]
    lpc_dataset.to_csv('LPC.csv',index=False)
    
    # creating the child dataset for plasmalogen
    plasmalogen_dataset = df[df['Accepted Compound ID'].str.endswith('plasmalogen',na=False)]
    plasmalogen_dataset.to_csv('Plasmalogen.csv',index=False)
    
    # creating zip file for user to download after filtering
    download_zipfile_list = ['PC.csv','LPC.csv','Plasmalogen.csv']
    
    download_file=io.BytesIO()
    
    zip_file = ZipFile('Processed.zip','w')
    zip_file.write('PC.csv')
    zip_file.write('LPC.csv')
    zip_file.write('Plasmalogen.csv') 
    
    zip_file.close()   
    
    os.remove('PC.csv')
    os.remove('LPC.csv')
    os.remove('Plasmalogen.csv')
    
    return send_file('./Processed.zip',
                     attachment_filename='Processed.zip',
                     as_attachment=True)


# API endpoint for Retention time roundoff and mean calculation
@app.route('/retention',methods=['GET'])
def retention_time():
    # parent dataframe
    df = pd.read_excel('uploads/mass_spec_data_assgnmnt.xlsx.xlsx')
    
    # creating blank series (label)
    retention_time_roundoff = pd.Series([],dtype='int64')
    
    # iterating through the dataframe to round off the values to integer
    for i in range(len(df)):
        retention_time_roundoff[i]= int(round(df['Retention time (min)'][i]))
    
    df.insert(2,'Retention Time Roundoff (in mins)',retention_time_roundoff)
    
    # deleting unwanted data columns
    del df['m/z']
    del df['Retention time (min)']
    
    # creating new dataframe
    new_data_frame = df.groupby(df['Retention Time Roundoff (in mins)']).mean()
    
    new_data_frame.to_csv('Mean.csv')
    
    return send_file('./Mean.csv',
                     mimetype='text/csv',
                     attachment_filename='Mean.csv',
                     as_attachment=True)

# running the application
app.run(debug=True)

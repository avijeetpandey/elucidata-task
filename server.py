from flask import Flask
from flask import render_template


# creating the flask application named app
app=Flask(__name__,static_url_path='',static_folder='web/static',template_folder='web/templates')

# intial route when server is hit first
@app.route('/')
def hello():
    return render_template('index.html',message='Yo man i am the Flask')


# running the application
app.run(debug=True)
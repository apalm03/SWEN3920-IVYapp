import os
from flask import render_template, request, redirect, url_for, flash, abort, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from werkzeug import *
from forms import UploadForm
from scripts import label_image
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json



import subprocess

UPLOAD_FOLDER= "./static/uploads"





SECRET_KEY = 'Sup3r$3cretkey'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:////mnt/c/Users/acm47/PycharmProjects/Plantapp/plantdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
db=SQLAlchemy(app)


class Plant(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    plant_name = db.Column(db.String(80))
    scientific_name= db.Column(db.String(80))
    uses = db.Column(db.String(500))
    class_ = db.Column(db.String(80))
    species = db.Column(db.String(80))

class UploadImages(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)

 




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/camera')
def camera():
    return render_template('camera_capture.html')


@app.route('/upload',methods=['POST','GET'])
def upload():

    uploadform = UploadForm()
    if request.method =='POST'and uploadform.validate_on_submit():
        image = uploadform.image.data
        photo = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], photo))
        newImage=UploadImages(name=photo,data=image.read())
        db.session.add(newImage)
        db.session.commit
        flash('Image Saved', 'success')
        return redirect(url_for('uploaded_file',photo=photo))
        
        
    return render_template('upload.html',form=uploadform) 


    


@app.route('/show/<photo>')
def uploaded_file(photo):
    return render_template('photo_display.html', photo=photo)

@app.route('/uploads/<photo>')
def send_file(photo):
    return send_from_directory(UPLOAD_FOLDER, photo)


  
@app.route('/prediction/<image>',methods=['POST','GET'])
def prediction(image):
    filename= "1.hibiscus_7y0GBN.jpg"
    result=subprocess.Popen("python -m scripts.label_image --graph=tf_files/retrained_graph.pb --image=static/uploads/" + filename ,stdout=subprocess.PIPE, shell=True)
    (output, err) = result.communicate()
    return jsonify({'data':render_template('results.html',output=output)})
    

    





if __name__ == '__main__':
    app.debug = True
    app.run()
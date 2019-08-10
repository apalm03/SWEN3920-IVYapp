
import os
from flask import render_template, request, redirect, url_for, flash, abort, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from werkzeug import *
from app import app
from .forms import UploadForm
from app.scripts import label_image



import subprocess








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
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
        flash('Image Saved', 'success')
        return redirect(url_for('uploaded_file',filename=filename))
        return filename
        
    return render_template('upload.html',form=uploadform) 


    


@app.route('/show/<filename>')
def uploaded_file(filename):
    return render_template('photo_display.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


  
@app.route('/prediction/<filename>',methods=['POST','GET'])
def prediction(filename):
    filename= "5.Life-plant-Health-benefits.png"
    result=subprocess.Popen("python -m app.scripts.label_image --graph=tf_files/retrained_graph.pb --image=app/static/uploads/%s" %filename ,stdout=subprocess.PIPE, shell=True)
    (output, err) = result.communicate()
    return jsonify({'data':render_template('results.html',output=output,filename=filename)})
    

    





if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")

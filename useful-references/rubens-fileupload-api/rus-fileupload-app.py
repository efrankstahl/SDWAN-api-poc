# From 6/28 video on uplaoding a file via API
import os
from app import app 
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'yaml', 'yml'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/file-upload', method=['POST'])
def upload_file():
	#check if the post request has the file part
	# E: he spoke about this line individually after looking at robert's code
	print(request.form.git('gdoc_type'))
	if 'file' not in request.files:
		resp = jsonify({'message': 'No file part in the request'})
		resp.status_code = 400
		return resp 
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message': 'No file selected for uploading.'})
		resp.status_code = 400
		return resp 

	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		# change this as it is in api-preproc.py
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message': 'file successfully uploaded'})
		resp.status_code = 201
		return resp 
	else: 
		resp = jsonify({'message': 'Allowed file types are txt pdf png jpg etc'})
		resp.status_code = 400
		return resp 
	 
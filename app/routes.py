import os, sys

from pymongo import MongoClient
from app import app2
from flask import Flask, render_template, request
from werkzeug import secure_filename
from app.process import *
import app.globals

@app2.route('/')
@app2.route('/index')
def index():
    return "Hello, Worlrrrd!"

@app2.route('/upload')
def upload_page():
    app.globals.client = MongoClient("mongodb+srv://reg:none@cluster0-ymvoa.mongodb.net/test")
    app.globals.db = app.globals.client.database
    app.globals.db.docs.drop()
    for f in os.listdir('uploads'):
        os.remove('uploads/' + f)
    #print("YO" + app.globals.db, file=sys.stderr)
    return render_template('upload.html')

@app2.route('/uploader', methods=['GET','POST'])
def upload_file():
    fs = request.files.getlist('file')
    print(fs, file=sys.stderr)
    for f in fs:
        sfname = secure_filename(f.filename)
        f.save(app2.config['UPLOAD_FOLDER'] + '/' + sfname)
    return render_template('uploader.html', filelist=fs)


@app2.route('/indexer', methods=['GET', 'POST'])
def indexer():
    for f in os.listdir('uploads'):
        invertedIndex(f)
    return render_template('indexed.html')

@app2.route('/lister', methods=['GET', 'POST'])
def lister():
    f = request.form
    reslist = search(list(f.values())[0])
    return render_template('lister.html', rs=reslist)

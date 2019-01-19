from flask import Flask

app2 = Flask(__name__)
app2.config['UPLOAD_FOLDER'] = './uploads'
from app import routes, globals

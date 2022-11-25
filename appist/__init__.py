from flask import Flask
from appist.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask_ist.db')))

from appist import routes

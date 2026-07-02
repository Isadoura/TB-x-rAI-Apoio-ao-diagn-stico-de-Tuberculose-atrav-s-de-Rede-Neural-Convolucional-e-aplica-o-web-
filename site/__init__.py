from flask import Flask 

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "sitemodelo/static/uploads"

from sitemodelo import routes

import os

import mongoengine
from dotenv import load_dotenv
from flask import Flask
from flask_wtf import CSRFProtect

from app.views import router

load_dotenv()

app = Flask(__name__, template_folder="../templates/")
app.secret_key = os.environ["SECRET_KEY"]
app.register_blueprint(router)

CSRFProtect(app)


if os.environ.get("FLASK_ENV") == "development":
    app.config["TEMPLATES_AUTO_RELOAD"] = True

mongoengine.connect(host=os.environ["MONGO_URI"])

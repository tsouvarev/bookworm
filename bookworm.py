import os

import mongoengine
from dotenv import load_dotenv
from flask import Flask
from flask_wtf import CSRFProtect

from app.utils import get_readable_month_name
from app.views import router

load_dotenv()

app = Flask(__name__, template_folder="../templates/")
app.secret_key = os.environ["SECRET_KEY"]
app.register_blueprint(router)
app.add_template_filter(get_readable_month_name, name="readable_month")

CSRFProtect(app)


if os.environ.get("FLASK_ENV") == "development":
    app.config["TEMPLATES_AUTO_RELOAD"] = True

mongoengine.connect(host=os.environ["MONGO_URI"])

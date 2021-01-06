import os

import mongoengine
from dotenv import load_dotenv
from flask import Flask

from app.utils import pretty_date
from app.views import router

load_dotenv()

app = Flask(__name__, template_folder="../templates/")
app.secret_key = os.environ["SECRET_KEY"]
app.template_filter()(pretty_date)
app.register_blueprint(router)

mongoengine.connect(host=os.environ["MONGO_URI"])

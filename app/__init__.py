from flask import Flask

app = Flask(__name__)

from app import views

app.config.update(
    SECRET_KEY = "gh3F+"
)

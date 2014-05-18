__author__ = 'MrTrustworthy'


from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("app_config.py")


from ProjectSL import views
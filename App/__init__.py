from flask import  Flask, render_template, request, jsonify
# Build your app

app = Flask(__name__)
app.secret_key = 'secret'

# Isbaris applicatoin-kaaga
from App.public import  public_view

from App.user import user_view
from App.user import user_model
#admin view
from  App.admin import admin_view
#admin model
from App.admin import admin_model
from App import configuration
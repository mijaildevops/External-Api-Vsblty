from flask import Flask, request
from flask import render_template
from flask import jsonify

import requests
# DB
import pymysql

import json
import os

# GUID
import uuid 

# Cors
from flask_cors import CORS

# Mkdir
from shutil import rmtree 
from os import makedirs
from os import remove
import shutil

# FecHa
from datetime import date
from datetime import datetime
# Numero Random
import random2

# Email 
import smtplib



# Cors access
app=Flask(__name__,template_folder='templates')
cors = CORS(app)

#//////////////////////////////////////////////////////////////////////////
# Index
#//////////////////////////////////////////////////////////////////////////
@app.route('/')
def home():
    return 'Api Rest External (App V3)'

#///////////////////////////////////////////////////////
# FUncion Email
#//////////////////////////////////////////////////////
@app.route('/Email', methods=[ 'POST'])
def SendEmail ():

    # Capturamos la Variable Email Enviada
    Text = "Contacto Perfil Profesional /n"
    NameContact= request.form['Name']
    EmailContact = request.form['Email']
    MessageContact = request.form['Message']  

    # datos del Email
    asunto = str(Text) + "-" +str(NameContact) + " -"
    subject =  asunto 
    message =  str(MessageContact) + " -" +str (EmailContact)
    message = "Subject: {}\n\n{}".format(subject, message)

    #Servidor de Email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("mijail.test4@gmail.com", "58722191")

    # Destinatarios    
    #server.sendmail("mijail.test4@gmail.com", "mijail.test7@gmail.com", message)
    server.sendmail("mijail.test4@gmail.com", "mijailosorioh@gmail.com", message)

    server.quit()
    print (" -Correo enviado correctamente! Funcion Email")

    return jsonify({ "Session": "Email Send", "message": "Your email was sent"})


#***************************************************************************
#//////////////////////////////////////////////////////////////////////////
# Host Api
#//////////////////////////////////////////////////////////////////////////
#***************************************************************************


if __name__ == '__main__':
    #app.run(host='192.168.100.233', port=5080, debug=True)
    app.run(host='192.168.100.51', port=5060, debug=True)

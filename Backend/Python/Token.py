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

app=Flask(__name__,template_folder='templates')
cors = CORS(app)

@app.route('/')
def home():
    return 'Api Rest External'

@app.route('/Token/Genered', methods=['POST'])
def TokenGenered():

    Environment = request.form.get("Environment")
    
    
    #Environment = 0
    grant_type = "client_credentials"
    client_id = "F4DAB8A1-774D-4957-8497-FD4D73361E32"
    client_secret = "g44bIeDH/YRjeM7IpkOwyfjr8kRUOVUxE/h3swR6RCCs2SPP3eDq4VVXo124YIH3084+nJvAG4SmMVcOxx7JYA=="
    
    if (Environment == 1):
        Url = "https://api.vsblty.net/"
    else:
        Url = "https://vsblty-apiv2-qa.azurewebsites.net/"

    result = [grant_type, client_id, client_secret, Url]

    grant_type = result[0]
    client_id = result[1]
    client_secret = result[2]
    Environment_Url = result[3] + "/token"
    

    #Realizamos peticion Http
    pload = {'grant_type':grant_type,'client_id':client_id,'client_secret':client_secret}
    r = requests.post(Environment_Url, data = pload)

    #encoded respuesta
    data_string = json.dumps(r.json())

    #Decoded respuesta
    decoded = json.loads(data_string)

    # capturamos Variables
    try:
        Token = str(decoded["access_token"])
        Generado = str(decoded[".issued"])
        Expira = str(decoded[".expires"])
        Message = "Token generated correctly... (Expires in 1 Hour)"
        error = ""
    except:
        error = str(decoded["error"])

    if len(error) > 0:
        return jsonify([{'Message': error}])
    else:
        return jsonify([{'Environment': Url, 'Message': Message, 'Token': Token, 'Generated': Generado, 'Expires': Expira}])

@app.route('/Token/<UserId>')
def TokenData(UserId):
    #print (EndpointId)
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `grant_type`, `client_id`, `client_secret`, `Environment` FROM `User` WHERE `Id`=%s"
            cursor.execute(sql, (UserId))
            result = cursor.fetchone()



            grant_type = str(result.get('grant_type'))
            client_id = str(result.get('client_id'))
            client_secret = str(result.get('client_secret'))
            Environment = str(result.get('Environment'))

            result = [grant_type, client_id, client_secret, Environment]

            grant_type = result[0]
            client_id = result[1]
            client_secret = result[2]
            Environment_Url = result[3] + "/token"
            

            #Realizamos peticion Http
            pload = {'grant_type':grant_type,'client_id':client_id,'client_secret':client_secret}
            r = requests.post(Environment_Url, data = pload)

            #encoded respuesta
            data_string = json.dumps(r.json())

            #Decoded respuesta
            decoded = json.loads(data_string)

            # capturamos Variables
            Token = str(decoded["access_token"])
            Generado = str(decoded[".issued"])
            Expira = str(decoded[".expires"])


            # Actualizar todos los registos del Usuario
            sql_update_query = """UPDATE Token set IsActive = %s where User_Id = %s"""
            data_tuple = (0, UserId)

            cursor.execute(sql_update_query, data_tuple)
            connection.commit()

            # Insertar \             
            sql = "INSERT INTO `Token` (`User_Id`, `Token`, `Toke_Generated`, `Token_Expiration`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (UserId, Token, Generado, Expira))
            
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        return jsonify("Se ha Generado Token Correctamente..")

    finally:
        connection.close()

        # Agregar Token Funcion AddToken

if __name__ == '__main__':
    app.run(host='192.168.100.233', port=5080, debug=True)
    #app.run(host='192.168.100.51', port=5080, debug=True)
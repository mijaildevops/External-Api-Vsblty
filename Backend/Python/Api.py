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
    return 'Api rest External'

# Token
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

# Mostartr data
@app.route('/Data/<UserId>')
def GetData(UserId):

    #///////////////////////////////////////////
    # Generamos Un GUID 
    #///////////////////////////////////////////
    IdUnico = uuid.uuid4()
    Guid = str(IdUnico)

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
            sql = "SELECT `Token` FROM `Token` WHERE `User_Id`=%s AND IsActive=%s "
            cursor.execute(sql, (UserId, 1))
            result = cursor.fetchone()
            Token = str(result.get('Token'))

            # Armamos el Token
            Token = 'Bearer ' + Token
            headers = {'Authorization' :  Token  }

            # Read a single record
            sql = "SELECT `Endpoint_Id`, `Environment` FROM `User` WHERE `Id`=%s"
            cursor.execute(sql, (UserId))
            result = cursor.fetchone()

            Endpoint_Id = str(result.get('Endpoint_Id'))
            Environment = str(result.get('Environment'))

            Url = Environment + '/api/LiveEndpointData/'+ Endpoint_Id

            #pload = {'Authorization' : 'Bearer' + 'Token 90JATsV1lIYYXuH44jyfwkrpTiPv0eGxo_2FD4aqgKyiNUjzA56D7vXZG25tvV6jFjhoCF8NuoG0SgwzL3PVSPTcRCRT3PbWqULOhpl8FtVfe1whTjolBM-1iafgRiQKaRAO85CfO0x1Mwh9G8HtXZjzTfvylx4ajkzZ8upCD_dXrSXCQg8MHH_nHYDu47-DZ9XyzFOIAt9qJQjHf3jpUiPQNjKHmVwAQy17u3wENUVS4g8VrL0nBo76XEGshVyp7zXR428KnuMgjb4HjP_F1g'}
            r = requests.post(Url, headers=headers)
            print(r.text)

            dir = 'C:/Pruebas'  # También es válido 'C:\\Pruebas' o r'C:\Pruebas'
            file_name = Guid +".json"

            with open(os.path.join(dir, file_name), 'w') as file:
                json.dump(r.json(), file)
        
                 
        return jsonify(r.json())

    finally:
        connection.close()

@app.route('/User/<Idtest>')
def User(Idtest):
    #print (EndpointId)
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


    try:
        with connection.cursor() as cursor:

            #///////////////////////////////
            
            sql2 = "SELECT `User`, `Endpoint_Id`, `Environment` FROM `User` WHERE `Id`=%s"
            cursor.execute(sql2, (Idtest))
            resultMensajes_Actual = cursor.fetchall()
            #print(resultMale)
            
            #///////////////////////////////
         

        return jsonify(resultMensajes_Actual)

    finally:
        connection.close()

@app.route('/TokenInfo/<Idtest>')
def TokenInfo(Idtest):
    #print (EndpointId)
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


    try:
        with connection.cursor() as cursor:

            #///////////////////////////////
            
            sql = "SELECT `Id`, `Toke_Generated`, `Token_Expiration`, `Time` FROM `Token` WHERE `User_Id`=%s AND `IsActive`=%s  "
            cursor.execute(sql, (Idtest, 1))
            resultMensajes_Actual = cursor.fetchall()
            #print(resultMale)
            
            #///////////////////////////////
         

        return jsonify(resultMensajes_Actual)

    finally:
        connection.close()

if __name__ == '__main__':
    #app.run(host='192.168.100.233', port=5080, debug=True)
    app.run(host='192.168.100.51', port=5080, debug=True)
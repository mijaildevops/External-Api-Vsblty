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

app=Flask(__name__,template_folder='templates')
cors = CORS(app)

#//////////////////////////////////////////////////////////////////////////
# Index
#//////////////////////////////////////////////////////////////////////////
@app.route('/')
def home():
    return 'Api Rest External'

#//////////////////////////////////////////////////////////////////////////
# User
#//////////////////////////////////////////////////////////////////////////
@app.route('/Update/<UserId>', methods=[ 'POST'])
def UpdateUser(UserId):

    if request.method == 'POST':
        GrantType = request.form['GrantType']
        ClientId = request.form['ClientId']
        ClientSecret = request.form['ClientSecret']
        EndpointId = request.form['EndpointId']
        Environment = request.form['Environment']
        Intervalo = request.form['Intervalo']
        try:
            Email = request.form['Email']
        except:
            Email = 0 
        print (GrantType)
        print (ClientId)
        print (ClientSecret)
        print (EndpointId)
        print (Environment)
        print (Intervalo)
        print (Email)
        
        UserId = int(UserId)
        Intervalo = int(Intervalo)
    
        connection = pymysql.connect(host='192.168.100.51',
            user='Qatest',
            password='Quito.2019',
            db='External-Api',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
            
        try:
            with connection.cursor() as cursor:
                # Actualizar todos los registos del Usuario
                sql_update_query = """UPDATE User set  grant_type = %s, client_id = %s, client_secret = %s, Endpoint_Id = %s, Environment = %s, Intervalo = %s, Email = %s  where Id = %s"""
                data_tuple = (GrantType, ClientId, ClientSecret, EndpointId, Environment, Intervalo, Email, UserId)

                print (data_tuple)
                cursor.execute(sql_update_query, data_tuple)
                connection.commit()
                Message = "Datos actualizados Correctamente"
                return jsonify(Message)
        finally:
            connection.close()

    else:
        return jsonify("Error al Intentar Actualizar los datos")

    

    


#///////////////////////////////////////
# UserData
#///////////////////////////////////////
@app.route('/User/<UserId>')
def User(UserId):
    #print (EndpointId)
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


    try:
        with connection.cursor() as cursor:
           
            sql2 = "SELECT `User`, `Endpoint_Id`, `Environment` FROM `User` WHERE `Id`=%s"
            cursor.execute(sql2, (UserId))
            result = cursor.fetchone()
            
            try:

                User = str(result.get('User'))
                Endpoint_Id = str(result.get('Endpoint_Id'))
                Environment = int(result.get('Environment'))

                if (Environment == 1):
                    Url = "https://api.vsblty.net/"
                else:
                    Url = "https://vsblty-apiv2-qa.azurewebsites.net/"
            
                connection.commit()
                Message = "Successful"

                return jsonify([{'Environment': Url, 'Message': Message, 'User': User, 'Endpoint_Id': Endpoint_Id}])
            except:
                Message = "Error, Peticion Negada"
                return jsonify([{'Message': Message}])

    finally:
        connection.close()

#//////////////////////////////////////////////////////////////////////////
# Generar Token
#//////////////////////////////////////////////////////////////////////////
@app.route('/Token/<UserId>')
def Token(UserId):

    UserId = int(UserId)
    
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

            connection.commit()

            grant_type = str(result.get('grant_type'))
            client_id = str(result.get('client_id'))
            client_secret = str(result.get('client_secret'))
            Environment = int(result.get('Environment'))

            if (Environment == 1):
                Url = "https://api.vsblty.net/"
            else:
                Url = "https://vsblty-apiv2-qa.azurewebsites.net/"

            print (grant_type)
            print (client_id)
            print (client_secret)
            print (Url)

            Environment_Url = Url + "/token"

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

                # Actualizar todos los registos del Usuario
                sql_update_query = """DELETE FROM Token where User_Id = %s"""
                data_tuple = (UserId)
                cursor.execute(sql_update_query, data_tuple)
                connection.commit()

                # Insertar 
                sql = "INSERT INTO `Token` (`User_Id`, `Token`, `Toke_Generated`, `Token_Expiration`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (UserId, Token, Generado, Expira))
                connection.commit()
                
                # Mensaje 
                return jsonify([{'Environment': Url, 'Message': Message, 'Token': Token, 'Generated': Generado, 'Expires': Expira}])
                # Actualizar todos los registos del Usuario
           
            connection.commit() 

    finally:
        connection.close()

#//////////////////////////////////////////////////////////////////////////
# Token Data
#//////////////////////////////////////////////////////////////////////////
@app.route('/Generated/<UserId>')
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
            sql = "SELECT `Token`, `Toke_Generated`, `Token_Expiration` FROM `Token` WHERE `User_Id`=%s"
            cursor.execute(sql, (UserId))
            result = cursor.fetchone()

            # commit to save
            connection.commit()

            try:
                Token = str(result.get('Token'))
                Toke_Generated = str(result.get('Toke_Generated'))
                Token_Expiration = str(result.get('Token_Expiration'))
                Message = "Data Succesful"
                return jsonify([{'Message': Message, 'Token': Token, 'Generated': Toke_Generated, 'Expires': Token_Expiration}])
            except:
                Message = "Error Pericion Invalida"
                return jsonify([{'Message': Message}])

    finally:
        connection.close()

#//////////////////////////////////////////////////////////////////////////
# #Get data One
#//////////////////////////////////////////////////////////////////////////
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
            sql = "SELECT `Token` FROM `Token` WHERE `User_Id`=%s AND IsActive=%s"
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
            Environment = int(result.get('Environment'))

            if (Environment == 1):
                Environment = "https://api.vsblty.net/"
            else:
                Environment = "https://vsblty-apiv2-qa.azurewebsites.net/"

            Url = Environment + '/api/LiveEndpointData/'+ Endpoint_Id

            now = datetime.now() 
            Fecha=str(now.strftime("%Y-%m-%d-%H-%M-%S"))
            
            file_name =Fecha + "---" + Guid +".json"
            
            
            
            

            try:
                #pload = {'Authorization' : 'Bearer' + 'Token 90JATsV1lIYYXuH44jyfwkrpTiPv0eGxo_2FD4aqgKyiNUjzA56D7vXZG25tvV6jFjhoCF8NuoG0SgwzL3PVSPTcRCRT3PbWqULOhpl8FtVfe1whTjolBM-1iafgRiQKaRAO85CfO0x1Mwh9G8HtXZjzTfvylx4ajkzZ8upCD_dXrSXCQg8MHH_nHYDu47-DZ9XyzFOIAt9qJQjHf3jpUiPQNjKHmVwAQy17u3wENUVS4g8VrL0nBo76XEGshVyp7zXR428KnuMgjb4HjP_F1g'}
                r = requests.post(Url, headers=headers)
                print(r.text)

                try:
                    # change the destination path
                    dir = "C:/Pruebas/"  +str(UserId) + "/" 
                    makedirs(dir)
                    print (" - Creating Folder of Test-", UserId)
                except FileExistsError:
                    print (" - Folder Exists")
                    dir = "C:/Pruebas/"  +str(UserId) + "/"
                
                

                with open(os.path.join(dir, file_name), 'w') as file:
                    json.dump(r.json(), file)

                return jsonify(r.json())
                
            except:
                Message = "Error Pericion Invalida, Verify the Token and Url Environment"
                return jsonify([{'Message': Message}])
            
                 
        

    finally:
        connection.close()

#//////////////////////////////////////////////////////////////////////////
# Get Data List
#//////////////////////////////////////////////////////////////////////////
@app.route('/DataList/<UserId>')
def GetDataList(UserId):
    Path = "C:/Pruebas/" + str(UserId) + "/"
    dirs = os.listdir(Path)
    dirs.sort(reverse=True) 
    print (Path)
    print (len(dirs))
    DataList = []

    for file in dirs:
        
        File = Path + file
        print ("file: ", file)
        print ("Path: ", File)

        with open(File) as contenido:
            DataFile = json.load(contenido)

            #encoded
            data_string = json.dumps(DataFile)

            #Decoded
            decoded = json.loads(data_string)

            Image = str(decoded["CapturedImageURL"])
            Name = str(decoded["EndpointData"]["IdentityName"])
            Match = str(decoded["EndpointData"]["Confidence"])
            Age = str(decoded["EndpointData"]["Age"])
            Gender = str(decoded["EndpointData"]["Gender"])
            FrameTime = str(decoded["EndpointData"]["FrameTime"])
            #print (Image)
            print (Image)
            
            GetDataFile = {
                    "file":file,
                    "Image":Image,
                    "Name":Name,
                    "Match":Match,
                    "Age":Age,
                    "Gender":Gender,
                    "FrameTime":FrameTime,
                    }
            
            DataList.append(GetDataFile)


    return jsonify(DataList)

#//////////////////////////////////////////////////////////////////////////
# Delete Data List
#//////////////////////////////////////////////////////////////////////////
@app.route('/Delete/<UserId>/<Id>', methods=[ 'DELETE'])
def Deletedata(UserId, Id):
    
    # Remove path Folder KingSalmon
    Filepath = "C:/Pruebas/"+ UserId + "/"+ Id
    print (Filepath)
    remove(Filepath)
    return jsonify("Eliminado Correctamente")

#//////////////////////////////////////////////////////////////////////////
# Delete all Data List
#//////////////////////////////////////////////////////////////////////////
@app.route('/Delete/<UserId>/all', methods=[ 'DELETE'])
def DeleteAlldata(UserId):
    
    # Remove path Folder KingSalmon
    Filepath = "C:/Pruebas/"+ UserId 
    print (Filepath)
    rmtree(Filepath)
    return jsonify("Eliminado Correctamente")

if __name__ == '__main__':
    app.run(host='192.168.100.233', port=5080, debug=True)
    
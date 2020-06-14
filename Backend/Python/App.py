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

# Cors access
app=Flask(__name__,template_folder='templates')
cors = CORS(app)

# Numero Random
import random2

# Email 
import smtplib

#///////////////////////////////////////////////////////
# FUncion Email
#//////////////////////////////////////////////////////
def SendEmail (EmailUser, TokenUser, Text, ProcessId):
    # datos del Email
        asunto = str(Text) + str(TokenUser)
        subject =  asunto 
        message =  "External-APP: \n" + "-- User: " + str(EmailUser) + "\n-- Validation Code: "+ str(TokenUser) +"\n Please confirm the code"
        message = "Subject: {}\n\n{}".format(subject, message)

        #Servidor de Email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("mijail.test4@gmail.com", "58722191")

        # Destinatarios    
        #server.sendmail("mijail.test4@gmail.com", "mijail.test7@gmail.com", message)
        server.sendmail("mijail.test4@gmail.com", str(EmailUser), message)

        server.quit()
        print (ProcessId, " -Correo enviado correctamente! Funcion Email")

#//////////////////////////////////////////////////////////////////////////
# Index
#//////////////////////////////////////////////////////////////////////////
@app.route('/')
def home():
    return 'Api Rest External (App V3)'

#***************************************************************************
#//////////////////////////////////////////////////////////////////////////
# LOGIN
#//////////////////////////////////////////////////////////////////////////
#***************************************************************************
#######################################
# Login User
#######################################
@app.route('/Login', methods=[ 'POST'])
def Login():
    # Process Id 
    ProcessId = "(A-01)"

    try:
        # Capturamos la Variable Email Enviada
        EmailUser = request.form['Email']
        Code = request.form['Code']  
          

        # Conexion DB
        connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
                    
        with connection.cursor() as cursor:
            # Validar Usuario Existente
            # Read a single record
            sql = "SELECT `User`, CodeUser, Status FROM `User` WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            result = cursor.fetchone()
            connection.commit()
            try:
                User = str(result.get('User'))
                CodeUser = str(result.get('CodeUser'))
                Status = int(result.get('Status'))
            except:
                User = "undefined"
            
            if (User == EmailUser and Code == CodeUser):
                
                print (ProcessId, " -OK: User is logged in:", EmailUser)
                
                if (Status == 3):
                    sql_update_query = """UPDATE User set  Status = %s where User = %s"""
                    data_tuple = (1, EmailUser)
                    cursor.execute(sql_update_query, data_tuple)
                    connection.commit()
                    print (ProcessId, " -OK: the user's status was updated:", EmailUser)
                return jsonify({ "Session": "satisfactory"})
            else:

                print (ProcessId, " -ERROR: The user has tried to login with invalid parameters: ", EmailUser)
                return jsonify({ "Session": "Failed", "message": "Session data is Incorrect, check and try again"})

    except Exception as e:
        print(ProcessId, " -", e)
        return jsonify({ "Session": "Ocurrio Un Error verifique los Parametros enviados, Intente Nuevamente"})
    finally:
        connection.close()

#***************************************************************************
#//////////////////////////////////////////////////////////////////////////
# USER
#//////////////////////////////////////////////////////////////////////////
#***************************************************************************
#######################################
# New User [POST]
#######################################
@app.route('/User', methods=[ 'POST'])
def NewUser():

    # Process Id 
    ProcessId = "(B-01)"
    try:
        # Capturamos la Variable Email Enviada
        EmailUser = request.form['Email']

        # Generamos Un User-Code Aleatorio (Password), Basado en 4 digitos Numericos de 1000 al 9999.
        CodeUser = random2.randint(1000, 9999)
        # Para cada Usuario Nuevo, se define el Status Como "0", esto para identificar que fue creado pero no ha ingresado nunca.
        Status = 0

        # Conexion DB
        connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
                    
        with connection.cursor() as cursor:
            # Validar si el Usuario Existente
            sql = "SELECT `User` FROM `User` WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            result = cursor.fetchone()
            connection.commit()
            try:
                User = str(result.get('User'))
            except:
                User = "undefined"
            
            if (User == EmailUser):
                # Si el User existe en la DB, se devuelve un error
                # Log Server y respuesta en formato Json 
                Email = False
                print (ProcessId, " -ERROR: The User is already Registered, User was not Created", EmailUser)
                return jsonify({ "Error": "The user is already Registered"})
            else:
                # Si el Usuario no existe en la DB, procede a Crear el registro 
                sql = "INSERT INTO `User` (User, CodeUser, Status) Values (%s,%s,%s)"
                cursor.execute(sql, (EmailUser, CodeUser, Status))
                connection.commit()
                Email = True

                #////////////////////////////    
                # Send Email
                #////////////////////////////  
                if (Email == True):
                    # subject
                    Text  = "Successful Registration - Code: "
                    # call Email Funtion
                    SendEmail (EmailUser, CodeUser, Text, ProcessId)
                    print (ProcessId, " -Validation Email, was sent successfully for: ", EmailUser)
                else:
                    print (ProcessId, " -ERROR:, the email was not sent SendEmail =: ", Email, "- ",EmailUser)
                    
                # Log Server y respuesta en formato Json
                print (ProcessId, " -OK: User was successfully created: ", EmailUser)
                return jsonify({"User": EmailUser, "Mensaje": "Successful Registration, Verify your Email and Validate the Code"})
            
    except Exception as e:
        print(ProcessId, " -", e)
        return jsonify({ "Error": "An error occurred creating the user. try again"})
    finally:
        connection.close()

#######################################
# Geta Data User [GET]
#######################################
@app.route('/User/<user>', methods=[ 'GET'])
def UserData(user):
    # process ID
    ProcessId = "(B-02)"

    # capturamos el User que realiza la Peticion
    EmailUser = user
    
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
           
            sql2 = "SELECT `User`, `Endpoint_Id`, Notification, `Environment`, Intervalo, Status, RegistrationDate, grant_type, client_id, client_secret  FROM `User` WHERE `User`=%s"
            cursor.execute(sql2, (EmailUser))
            result = cursor.fetchone()
            connection.commit()
           
            # Si el usuario esta registrado en la DB
            try:
                User = str(result.get('User'))
                RegistrationDate = str(result.get('RegistrationDate'))
                Status = int(result.get('Status'))
                Intervalo = int(result.get('Intervalo'))
                Environment = int(result.get('Environment'))
                Notification= int(result.get('Notification'))                
                # Verificar si las variables de Token existen
                try:
                    grant_type = str(result.get('grant_type'))
                    client_id = str(result.get('client_id'))
                    client_secret = str(result.get('client_secret'))
                    Endpoint_Id = str(result.get('Endpoint_Id'))
                # Si las variables del token son null, sustituimos
                except:
                    grant_type = "undefined"
                    client_id = "undefined" 
                    client_secret = "undefined" 
                    Endpoint_Id = "undefined" 
                    
                # Segun el valor de Environment, definimos la Url
                if (Environment == 1):
                    Url = "https://apivnext.vsblty.net/"
                else:
                    Url = "https://vsblty-apiv2-qa.azurewebsites.net/"

                # Log Server y respuesta en formato Json 
                print (ProcessId, " -User: ", EmailUser, " -Realizo Una peticion Get Para Obtener los datos Satisfactoriamente")
                return jsonify([{'Notification': Notification,'GrantType': grant_type, 'APIKey': client_id, 'APISecret': client_secret, 'EndpointId': Endpoint_Id, 'Environment': Url, 'Message': "Data Successfully", 'User': User, 'Intervalo': Intervalo, 'Status': Status, 'RegistrationDate': RegistrationDate}])
            
            # Si el usuario esta NO registrado en la DB
            except Exception as e:
                print(ProcessId, " -", e)
                # Log Server y respuesta en formato Json  
                print (ProcessId, " -Error: - User: ", EmailUser, "Realizo Una peticion Get Fallida (User Not Fount)")
                return jsonify({"Error": "User not found"})

    finally:
        connection.close()

#######################################
# Update Data User [PUT]
#######################################
@app.route('/User', methods=[ 'PUT'])
def UpdateUser():

    # Process Id 
    ProcessId = "(B-03)"

    if request.method == 'PUT':
        # Capturar Parametros Enviados
        EmailUser = request.form['Email']
        GrantType = request.form['GrantType']
        ClientId = request.form['ClientId']
        ClientSecret = request.form['ClientSecret']
        EndpointId = request.form['EndpointId']
        Environment = request.form['Environment']
        Intervalo = request.form['Intervalo']
        Notification = request.form['Notification']
        

        # convertimos a String 
        Intervalo = int(Intervalo)
    
        connection = pymysql.connect(host='192.168.100.51',
            user='Qatest',
            password='Quito.2019',
            db='External-Api',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
            
        try:
            with connection.cursor() as cursor:
                # Verificar si el usuariop existe
                sql = "SELECT `User` FROM `User` WHERE `User`=%s"
                cursor.execute(sql, (EmailUser))
                result = cursor.fetchone()
                connection.commit()
                try:
                    User = str(result.get('User'))
                except:
                    User = "undefined"
                
                # Si el user existe procedemos a realizar el Update
                if (User == EmailUser):
                    # Actualizar todos los registos del Usuario
                    sql_update_query = """UPDATE User set  grant_type = %s, client_id = %s, client_secret = %s, Endpoint_Id = %s, Environment = %s, Intervalo = %s, Notification= %s  where User = %s"""
                    data_tuple = (GrantType, ClientId, ClientSecret, EndpointId, Environment, Intervalo, Notification, EmailUser)
                    cursor.execute(sql_update_query, data_tuple)
                    connection.commit()

                    # Log Server y respuesta en formato Json
                    print (ProcessId, " -(OK) Datos Del usuario actualizados Correctamente", EmailUser)
                    return jsonify({"Message": "User data updated correctly"})
                else: 
                    # Log Server y respuesta en formato Json
                    print (ProcessId, " -ERROR Usuario no encontrado", EmailUser)
                    return jsonify({ "Error": "the user is not registered"})
        finally:
            connection.close()

    else:
        return jsonify({ "Error": "No se Puedieron Actualizar los datos"})

#######################################
# Update Data User [PUT]
#######################################
@app.route('/User', methods=[ 'DELETE'])
def DeleteUser():
    # Process Id 
    ProcessId = "(B-04)"
    
    # capturamos el User que realiza la Peticion
    EmailUser = request.form['Email']
    
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        # Verificamos que el usuario existe
        sql = "SELECT `User`, Id FROM `User` WHERE `User`=%s"
        cursor.execute(sql, (EmailUser))
        result = cursor.fetchone()
        connection.commit()
        try:
            Id = str(result.get('Id'))
            User = str(result.get('User'))
        except:
            User = "undefined"
            Id = "undefined"
            
        # Si el usuario Existe, Se procede a Eliminar los registros de User y Token
        if (User == EmailUser):

            # Delete data User
            sql = "DELETE FROM `User`  WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            connection.commit()

            # Delete data Token
            sql = "DELETE FROM `Token`  WHERE `User_Id`=%s"
            cursor.execute(sql, (Id))
            connection.commit()

            # Log Server y respuesta en formato Json
            print (ProcessId, " -OK: The user has been deleted: ", EmailUser)
            return jsonify({ "Mensaje": "The user has been deleted"})

        # usuario no Registrado    
        else:
            # Log Server y respuesta en formato Json
            print (ProcessId, " -ERROR: User trying to delete does not exist", EmailUser)
            return jsonify({ "Error": "User trying to delete does not exist"})

#***************************************************************************
#//////////////////////////////////////////////////////////////////////////
# Actuallizaciuon de Codigo Acceso
#//////////////////////////////////////////////////////////////////////////
#***************************************************************************
@app.route('/Code', methods=[ 'PUT'])
def CodeUpdate():

    # Process ID
    ProcessId = "(C-01)"

    # Capturamos la Variable Email Enviada
    EmailUser = request.form['Email']
    Code = random2.randint(1000, 9999)
    
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    try:
        try:
            with connection.cursor() as cursor:
                # Verificamos Si el Usuario Existe
                sql = "SELECT `User` FROM `User` WHERE `User`=%s"
                cursor.execute(sql, (EmailUser))
                result = cursor.fetchone()
                connection.commit()

                try:
                    User = str(result.get('User'))
                except:
                    
                    User = "undefined"

                # Si el Usuario Existe
                if (User == EmailUser):

                    # Actualizamos la Variable CodeUser
                    sql_update_query = """UPDATE User set CodeUser = %s where User = %s"""
                    data_tuple = (Code, EmailUser)
                    cursor.execute(sql_update_query, data_tuple)
                    connection.commit()
                    #////////////////////////////    
                    # Send Email
                    #////////////////////////////  
                    # subject
                    Text  = "Actualizacion - Code: "
                    # call Email Funtion
                    SendEmail (EmailUser, Code, Text, ProcessId)

                    # Log Server y respuesta en formato Json
                    print (ProcessId, " -Validation Email, was sent successfully for: ", EmailUser)
                    print (ProcessId, " -Verification Code was updated to", EmailUser)
                    return jsonify([{"Email": EmailUser, "Mensaje": "Verification Code was updated verify your email"}])
                else:
                    # Log Server y respuesta en formato Json
                    print (ProcessId, " -ERROR User not found", EmailUser)
                    return jsonify({"Error":"User not found"}) 
                
        finally:
            connection.close()
        
            
    except:
        print (ProcessId, " -Error En el proceso de Actualizacion del Codigo de Acceso")    

#***************************************************************************
#//////////////////////////////////////////////////////////////////////////
# Token Api
#//////////////////////////////////////////////////////////////////////////
#***************************************************************************
#///////////////////////////////////////
# Token Generation
#///////////////////////////////////////
@app.route('/Token', methods=[ 'PUT'])
def TokenGeneration():

    # Process ID
    ProcessId = "(D-01)"
    
    # Capturamos El Email enviado en la peticion
    EmailUser = request.form['Email']
    
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # Verificamos Si el Usuario Existe
            sql = "SELECT `User` FROM `User` WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            result = cursor.fetchone()
            connection.commit()

            try:
                User = str(result.get('User'))
            except:
                User = "undefined"
                
            if (User == EmailUser):
                # Obtener los datos para generar Token del Usuario
                sql = "SELECT `Id`, `grant_type`, `client_id`, `client_secret`, `Environment` FROM `User` WHERE `User`=%s"
                cursor.execute(sql, (EmailUser))
                result = cursor.fetchone()
                connection.commit()

                try:
                    User_Id = str(result.get('Id'))
                    grant_type = str(result.get('grant_type'))
                    client_id = str(result.get('client_id'))
                    client_secret = str(result.get('client_secret'))
                    Environment = int(result.get('Environment'))
                    
                    # Definimos la Url del Environment
                    if (Environment == 1):
                        Url = "https://apivnext.vsblty.net/"
                    else:
                        Url = "https://vsblty-apiv2-qa.azurewebsites.net/"
                    
                    # Url del Token de VSBLTY 
                    Environment_Url = Url + "token"
                
                # Si los datos son Null asignamos valor "undefined"
                except:
                    User_Id = "undefined"
                    grant_type = "undefined"
                    client_id = "undefined"
                    client_secret = "undefined"
                    Environment = "undefined"

                #Realizamos peticion Http
                pload = {'grant_type':grant_type,'client_id':client_id,'client_secret':client_secret}
                r = requests.post(Environment_Url, data = pload)

                #encoded respuesta
                data_string = json.dumps(r.json())

                #Decoded respuesta
                decoded = json.loads(data_string)

                # capturamos propiedades del Token generado en la API de VSBLTY
                try:
                    Token = str(decoded["access_token"])
                    Generado = str(decoded[".issued"])
                    Expira = str(decoded[".expires"])
                    Message = "Token generated correctly... (Expires in 1 Hour)"
                    error = ""
                    print ("Token generated correctly... ", EmailUser)
                
                # si no se puede Generar Token, capturamos el Error devuelto por VSBLTY
                except:
                    error = str(decoded["error"])

                # Si Vsblty devuelve error devolvemos en json de error
                if len(error) > 0:
                    # Log Server y respuesta en formato Json
                    print (ProcessId, " - Error generando Token", EmailUser)
                    return jsonify({'Error': error, "Mensaje":"Ocurrio un error al generar el Token verifique las Keys"})

                # Si el token, se genero Correctamente Actualizamos los datos    
                else:

                    # Actualizar todos los registos del Usuario
                    sql_update_query = """DELETE FROM Token where User_Id = %s"""
                    data_tuple = (User_Id)
                    cursor.execute(sql_update_query, data_tuple)
                    connection.commit()
                    print (ProcessId, " -(OK) previous tokens associated with the user have been removed", EmailUser)

                    # Insertar 
                    sql = "INSERT INTO `Token` (`User_Id`, `Token`, `Toke_Generated`, `Token_Expiration`) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (User_Id, Token, Generado, Expira))
                    connection.commit()
                    print (ProcessId, " -(OK) New token successfully registered", EmailUser)
                    
                    # Log Server y respuesta en formato Json
                    print (ProcessId, " - A new token was generated and the data was updated", EmailUser)
                    return jsonify([{'Environment': Url, 'Message': Message, 'Token': Token, 'Generated': Generado, 'Expires': Expira}])
                    # Actualizar todos los registos del Usuario
           
            connection.commit() 

    except:
        # Log Server y respuesta en formato Json
        print (ProcessId, " -Could Not Generate Token From VSBLTY", EmailUser)
        return jsonify({"Error":"Could Not Generate Token From VSBLTY"})

#///////////////////////////////////////
# Token Get
#///////////////////////////////////////
@app.route('/Token', methods=[ 'GET'])
def TokenData():

    # Process ID
    ProcessId = "(D-02)"
    
    # Capturamos El Email enviado en la peticion
    EmailUser = request.form['Email']

    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            
            # obtenemos el Id del Usuario recibido en la Peticion
            sql = "SELECT `Id` FROM `User` WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            result = cursor.fetchone()
            connection.commit()
            User_Id = str(result.get('Id'))
            
            # de la Tabla Token obtenemos los datos del Token Actual
            sql = "SELECT `Token`, `Toke_Generated`, `Token_Expiration` FROM `Token` WHERE `User_Id`=%s"
            cursor.execute(sql, (User_Id))
            result = cursor.fetchone()
            connection.commit()

            try:
                # capturamos variables de la Consulta
                Token = str(result.get('Token'))
                Toke_Generated = str(result.get('Toke_Generated'))
                Token_Expiration = str(result.get('Token_Expiration'))
                
                # Log Server y respuesta en formato Json
                print (ProcessId, " -(OK) token data successfully obtained", EmailUser)
                return jsonify([{'Message': "Data Succesful", 'Token': Token, 'Generated': Toke_Generated, 'Expires': Token_Expiration}])
            except:
                # Log Server y respuesta en formato Json
                print (ProcessId, " -(ERROR) Perition Invalid Error, current token data is null", EmailUser)
                return jsonify([{'Message': "Perition Invalid Error, current token data is null"}])

    finally:
        connection.close()

#***************************************************************************
#//////////////////////////////////////////////////////////////////////////
# Get Data LiveEndpointData
#//////////////////////////////////////////////////////////////////////////
#***************************************************************************
@app.route('/LiveEndpointData', methods=[ 'POST'])
def GetData():

    # Process ID
    ProcessId = "(E-01)"
    
    # Capturamos El Email enviado en la peticion
    EmailUser = request.form['Email']

    #///////////////////////////////////////////
    # Generamos Un GUID 
    #///////////////////////////////////////////
    IdUnico = uuid.uuid4()
    Guid = str(IdUnico)
    
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:

            # get User Id, del User Recibido en la peticion
            sql = "SELECT `Id`, User, `Endpoint_Id`, `Environment` FROM `User` WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            result = cursor.fetchone()
            connection.commit()

            try:
                User_Id = str(result.get('Id'))
                User = str(result.get('User'))
            except:    
                User_Id = "undefined"
                User = "undefined"

            try:
                Endpoint_Id = str(result.get('Endpoint_Id'))
                Environment = int(result.get('Environment'))
            except:    
                Endpoint_Id = "undefined"
                Environment = "undefined"

            # Si el Usuario Existe
            if (User == EmailUser):
                try:
                    
                    # Read a single record
                    sql = "SELECT `Token` FROM `Token` WHERE `User_Id`=%s AND IsActive=%s"
                    cursor.execute(sql, (User_Id, 1))
                    result = cursor.fetchone()
                    Token = str(result.get('Token'))
                    
                    # Armamos el Token
                    Token = 'Bearer ' + Token
                    headers = {'Authorization' :  Token  }

                    if (Environment == 1):
                        Environment = "https://apivnext.vsblty.net/"
                    else:
                        Environment = "https://vsblty-apiv2-qa.azurewebsites.net/"

                    Url = Environment + 'api/LiveEndpointData/'+ Endpoint_Id
                    print(Url)

                    now = datetime.now() 
                    Fecha=str(now.strftime("%Y-%m-%d-%H-%M-%S"))
            
                    file_name =Fecha + "---" + Guid +".json"
            
                    try:
                        #pload = {'Authorization' : 'Bearer' + 'Token 90JATsV1lIYYXuH44jyfwkrpTiPv0eGxo_2FD4aqgKyiNUjzA56D7vXZG25tvV6jFjhoCF8NuoG0SgwzL3PVSPTcRCRT3PbWqULOhpl8FtVfe1whTjolBM-1iafgRiQKaRAO85CfO0x1Mwh9G8HtXZjzTfvylx4ajkzZ8upCD_dXrSXCQg8MHH_nHYDu47-DZ9XyzFOIAt9qJQjHf3jpUiPQNjKHmVwAQy17u3wENUVS4g8VrL0nBo76XEGshVyp7zXR428KnuMgjb4HjP_F1g'}
                        r = requests.post(Url, headers=headers)

                        #encoded respuesta
                        data_string = json.dumps(r.json())

                        #Decoded respuesta
                        decoded = json.loads(data_string)

                        try:
                            # Capturamos la Propiedad EndpointData
                            EndpointData = str(decoded["EndpointData"])
                            print (EndpointData)
                    
                            try:
                                # change the destination path
                                dir = "/home/master/Documents/LiveEndpointData/"  +str(EmailUser) + "/" 
                                os.mkdir(dir)
                                print (" - Creating Folder of Test-", EmailUser)
                            except FileExistsError:
                                print (" - Folder Exists")
                                dir = "/home/master/Documents/LiveEndpointData/"  +str(EmailUser) + "/"

                            with open(os.path.join(dir, file_name), 'w') as file:
                                json.dump(r.json(), file)

                            return jsonify(r.json())
                        except:
                            try:
                                Error = str(decoded["Message"])
                                # Log Server y respuesta en formato Json
                                print (ProcessId, " - Error Live-Endpoint-data Get Data", EmailUser, "-", Error)
                                return jsonify([{'Error': Error}])
                            except:
                                Error = str(decoded["ErrorMessage"])
                                # Log Server y respuesta en formato Json
                                print (ProcessId, " - Error Live-Endpoint-data Get Data", EmailUser, "-", Error)
                                return jsonify([{'Error': Error}])
                                
                    except:
                        return jsonify([{'Message': "Error Pericion Invalida, Verify the Token and Url Environment"}])
                except:
                        return jsonify([{'Message': "Error Pericion Invalida, Verify the Token and Url Environment"}])
            
    finally:
        connection.close()

#***************************************************************************
#//////////////////////////////////////////////////////////////////////////
# Data
#//////////////////////////////////////////////////////////////////////////
#***************************************************************************
@app.route('/Data', methods=[ 'POST'])
def GetDataList():

    ProcessId = "(F-01)"

    EmailUser = request.form['Email']
    
    try:
        Path = "/home/master/Documents/LiveEndpointData/" + str(EmailUser) + "/"
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

        # Log Server y respuesta en formato Json
        print (ProcessId, " OK - The user requested the entire list of people", EmailUser)
        return jsonify(DataList)
    
    except:
        return jsonify([{'Message': "The list of records are empty"}])

#//////////////////////////////////////
# Delete Data List
#//////////////////////////////////////
@app.route('/Data', methods=[ 'DELETE'])
def Deletedata():

    ProcessId = "(F-01)"
    
    EmailUser = request.form['Email']
    Parametro = request.form['Parametro']

    if (Parametro == "all"):
        # Remove path Folder KingSalmon
        Filepath = "/home/master/Documents/LiveEndpointData/"+ EmailUser 
        print (Filepath)
        rmtree(Filepath)
        return jsonify([{'Message': "all files were deleted"}])
    else:
        try:
            # Remove path Folder KingSalmon
            Filepath = "/home/master/Documents/LiveEndpointData/"+ EmailUser + "/"+ Parametro
            print (Filepath)
            remove(Filepath)
            # Log Server y respuesta en formato Json
            print (ProcessId, " - the record was successfully deleted", EmailUser)
            return jsonify([{'Message': "the record was successfully deleted"}])
        except:
            # Log Server y respuesta en formato Json
            print (ProcessId, " - the file you are trying to delete was not found", EmailUser)
            return jsonify([{'Error': "the file you are trying to delete was not found"}])
        


#***************************************************************************
#//////////////////////////////////////////////////////////////////////////
# Host Api
#//////////////////////////////////////////////////////////////////////////
#***************************************************************************
if __name__ == '__main__':
    app.run(host='192.168.100.51', port=5080, debug=True)
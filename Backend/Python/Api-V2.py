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
    return 'Api Rest External'

#***************************************************************************
#//////////////////////////////////////////////////////////////////////////
# User
#//////////////////////////////////////////////////////////////////////////
#***************************************************************************
#///////////////////////////////////////
# Get-Data User
#///////////////////////////////////////
@app.route('/User', methods=[ 'GET'])
def UserData():
    # process ID
    ProcessId = "(A-02)"

    # capturamos el User que realiza la Peticion
    EmailUser = request.form['Email']
    
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


    try:
        with connection.cursor() as cursor:
           
            sql2 = "SELECT `User`, `Endpoint_Id`, `Environment`, Intervalo, Status, RegistrationDate FROM `User` WHERE `User`=%s"
            cursor.execute(sql2, (EmailUser))
            result = cursor.fetchone()
            connection.commit()
           
            try:

                User = str(result.get('User'))
                try:
                    Endpoint_Id = str(result.get('Endpoint_Id'))
                    Environment = int(result.get('Environment'))
                    Intervalo = int(result.get('Intervalo'))
                    Status = int(result.get('Status'))
                    RegistrationDate = str(result.get('RegistrationDate'))
                except:
                    Endpoint_Id = "undefined"
                    Environment = "undefined" 
                    Intervalo = "undefined" 
                    Status = "undefined" 
                    RegistrationDate = "undefined"

                if (Environment == 1):
                    Url = "https://api.vsblty.net/"
                else:
                    Url = "https://vsblty-apiv2-qa.azurewebsites.net/"

                print (ProcessId, " -User: ", EmailUser, "Realizo Una peticion Get Para Obtener los datos Satisfactoriamente")
                Message = "Data Successfully"
                return jsonify([{'Environment': Url, 'Message': Message, 'User': User, 'Endpoint_Id': Endpoint_Id, 'Intervalo': Intervalo, 'Status': Status, 'RegistrationDate': RegistrationDate}])

            except:
                
                print (ProcessId, " -Error: - User: ", EmailUser, "Realizo Una peticion Get Fallida")
                Message = "Error, Peticion Negada"
                return jsonify({"Error": "User not found"})

    finally:
        connection.close()

#///////////////////////////////////////
# Registrar Nuevo User
#///////////////////////////////////////
@app.route('/User', methods=[ 'POST'])
def NewUser():
    # Process Id 
    ProcessId = "(A-01)"

    try:
        # Capturamos la Variable Email Enviada
        EmailUser = request.form['Email']
        #Contrasena = request.form['Contrasena']
        #Peticion = request.form['Peticion']
        print (EmailUser)


        # Generamos Un Token Aleatorio
        CodeUser = random2.randint(1000, 9999)
        Status = 3

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
            sql = "SELECT `User` FROM `User` WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            result = cursor.fetchone()
            connection.commit()
            try:
                User = str(result.get('User'))
            except:
                print (ProcessId, " -Usuario no encontrado")
                User = "undefined"
            
            if (User == EmailUser):
                print (ProcessId, " -ERROR: The User is already Registered, User was not Created", EmailUser)
                return jsonify({ "Error": "The user is already Registered"})
            else:
                # Read a single record
                
                sql = "INSERT INTO `User` (User, CodeUser, Status) Values (%s,%s,%s)"
                cursor.execute(sql, (EmailUser, CodeUser, Status))
                connection.commit()
                print (ProcessId, " -OK: User was successfully created: ", EmailUser)

                
                return jsonify({"User": EmailUser, "Mensaje": "Successful Registration, Verify your Email and Validate the Code"})
            # Send Email
            # subject
            Text  = "Successful Registration - Code: "
            # call Email Funtion
            SendEmail (EmailUser, CodeUser, Text, ProcessId)
            print (ProcessId, " -Validation Email, was sent successfully for: ", EmailUser)
    except Exception as e:
        print(e)
        return jsonify({ "Error": "Ocurrio Un Error Intente Nuevamente"})
    finally:
        connection.close()

#///////////////////////////////////////
# Actualizacion de Datos User
#///////////////////////////////////////
@app.route('/User', methods=[ 'PUT'])
def UpdateUser():
    # Process Id 
    ProcessId = "(A-03)"

    if request.method == 'PUT':
        EmailUser = request.form['Email']
        GrantType = request.form['GrantType']
        ClientId = request.form['ClientId']
        ClientSecret = request.form['ClientSecret']
        EndpointId = request.form['EndpointId']
        Environment = request.form['Environment']
        Intervalo = request.form['Intervalo']

        """print (EmailUser)
        print (GrantType)
        print (ClientId)
        print (ClientSecret)
        print (EndpointId)
        print (Environment)
        print (Intervalo)
        print (Email)"""
        
        UserId = str(EmailUser)
        Intervalo = int(Intervalo)
    
        connection = pymysql.connect(host='192.168.100.51',
            user='Qatest',
            password='Quito.2019',
            db='External-Api',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
            
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `User` FROM `User` WHERE `User`=%s"
                cursor.execute(sql, (EmailUser))
                result = cursor.fetchone()
                connection.commit()
                try:
                    User = str(result.get('User'))
                except:
                    
                    User = "undefined"
                
                if (User == EmailUser):
                    # Actualizar todos los registos del Usuario
                    sql_update_query = """UPDATE User set  grant_type = %s, client_id = %s, client_secret = %s, Endpoint_Id = %s, Environment = %s, Intervalo = %s  where User = %s"""
                    data_tuple = (GrantType, ClientId, ClientSecret, EndpointId, Environment, Intervalo, UserId)

                    #print (data_tuple)
                    cursor.execute(sql_update_query, data_tuple)
                    connection.commit()
                    print (ProcessId, " -(OK) Datos Del usuario actualizados Correctamente", EmailUser)
                    Message = "User data updated correctly"
                    return jsonify({"Message": Message})
                else: 
                    print (ProcessId, " -ERROR Usuario no encontrado", EmailUser)
                    return jsonify({ "Error": "El usuario No esta Registrado"})
        finally:
            connection.close()

    else:
        return jsonify({ "Error": "No se Puedieron Actualizar los datos"})

#///////////////////////////////////////
# Delete  User
#///////////////////////////////////////
@app.route('/User', methods=[ 'DELETE'])
def DeleteUser():
    # Process Id 
    ProcessId = "(A-04)"
    
    # capturamos el User que realiza la Peticion
    EmailUser = request.form['Email']
    
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


    
    with connection.cursor() as cursor:
        # Validar Usuario Existente
        # Read a single record
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
            
        
        if (User == EmailUser):
            
            sql = "DELETE FROM `User`  WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            connection.commit()
            sql = "DELETE FROM `Token`  WHERE `User_Id`=%s"
            cursor.execute(sql, (Id))
            connection.commit()
            print (ProcessId, " -OK: The user has been deleted: ", EmailUser)
            return jsonify({ "Mensaje": "The user has been deleted"})
            
        else:
            print (ProcessId, " -ERROR: User trying to delete does not exist", EmailUser)
            return jsonify({ "Error": "User trying to delete does not exist"})






#///////////////////////////////////////
# Registrar Nuevo User
#///////////////////////////////////////
@app.route('/Login', methods=[ 'POST'])
def Login():
    # Process Id 
    ProcessId = "(A-01)"

    try:
        # Capturamos la Variable Email Enviada
        EmailUser = request.form['Email']
        Contrasena = request.form['Contrasena']
        #Peticion = request.form['Peticion']
        print (EmailUser)
        print (Contrasena)
        

        # Generamos Un Token Aleatorio
        CodeUser = random2.randint(1000, 9999)
        Status = 3

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
            sql = "SELECT `User` FROM `User` WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            result = cursor.fetchone()
            connection.commit()
            try:
                User = str(result.get('User'))
            except:
                print (ProcessId, " -Usuario no encontrado")
                User = "undefined"
            
            if (User == EmailUser):
                print (ProcessId, " -ERROR: The User is already Registered, User was not Created", EmailUser)
                return jsonify({ "Error": "The user is already Registered"})
            else:
                # Read a single record
                
                sql = "INSERT INTO `User` (User, CodeUser, Status) Values (%s,%s,%s)"
                cursor.execute(sql, (EmailUser, CodeUser, Status))
                connection.commit()
                print (ProcessId, " -OK: User was successfully created: ", EmailUser)

                # Send Email
                # subject
                Text  = "Successful Registration - Code: "
                # call Email Funtion
                SendEmail (EmailUser, CodeUser, Text, ProcessId)
                print (ProcessId, " -Validation Email, was sent successfully for: ", EmailUser)
                return jsonify([{"User": EmailUser, "Code": CodeUser, "Mensaje": "Successful Registration, Verify your Email and Validate the Code"}])

    except Exception as e:
        print(e)
        return jsonify({ "Error": "Ocurrio Un Error Intente Nuevamente"})
    finally:
        connection.close()




#***************************************************************************
#//////////////////////////////////////////////////////////////////////////
# Codigo Validacion
#//////////////////////////////////////////////////////////////////////////
#***************************************************************************
#///////////////////////////////////////
# Validacion Codigo Acceso
#///////////////////////////////////////
@app.route('/Validacion', methods=[ 'POST'])
def Validacion():
    # Process ID
    ProcessId = "(B-01)"
    # Capturamos la Variable Email Enviada
    EmailUser = request.form['Email']
    Code = request.form['Code']

    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `CodeUser` FROM `User` WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            result = cursor.fetchone()
            connection.commit()
            TokenUser = str(result.get('CodeUser'))
       

        # Validamos el Codigo con el Token de la DB    
        if (TokenUser == Code):
            # Update Status User
            Status = 1
            try:
                with connection.cursor() as cursor:
                    sql_update_query = """UPDATE User set  Status = %s where User = %s"""
                    data_tuple = (Status, EmailUser)
                    cursor.execute(sql_update_query, data_tuple)
                    connection.commit()
                    # Respuesta Json
                    print (ProcessId, " -OK validacion de Usuario Fue Exitosa: ", EmailUser)
                    return jsonify({ "Mensaje": "Successful Validation"})
            finally:
                connection.close()
        else:
            print (ProcessId, " -ERROR validacion de Usuario: ", EmailUser)
            return jsonify( {"Error": "Invalid validation code Verify your Email and try again"})
            
    except:
        print (ProcessId, " -ERROR En el proceso de validacion")

#///////////////////////////////////////
# Actuallizaciuon de Codigo Acceso
#///////////////////////////////////////
@app.route('/Validacion', methods=[ 'PUT'])
def CodeUpdate():
    # Process ID
    ProcessId = "(B-02)"
    # Capturamos la Variable Email Enviada
    EmailUser = request.form['Email']
    TokenUser = random2.randint(1000, 9999)
    

    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    try:
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT `User` FROM `User` WHERE `User`=%s"
                cursor.execute(sql, (EmailUser))
                result = cursor.fetchone()
                connection.commit()
                try:
                    User = str(result.get('User'))
                except:
                    
                    User = "undefined"

                if (User == EmailUser):

                    # Read a single record
                    sql_update_query = """UPDATE User set CodeUser = %s where User = %s"""
                    data_tuple = (TokenUser, EmailUser)
                    cursor.execute(sql_update_query, data_tuple)
                    connection.commit()
                    
                    # Send Email
                    Text  = "Actualizacion - Code: "
                    SendEmail (EmailUser, TokenUser, Text, ProcessId)
                    print (ProcessId, " -Verification Code was updated to", EmailUser)
                    return jsonify([{"Email": EmailUser, "Code": TokenUser, "Mensaje": "Verification Code was updated verify your email"}])
                else:
                    print (ProcessId, " -ERROR User not found", EmailUser)
                    return jsonify({"Error":"User not found"}) 
        finally:
            connection.close()
        
            
    except:
        print ("error En el proceso de Actualizacion del Codigo de Acceso")    

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

    EmailUser = request.form['Email']
    
    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `Id`, `grant_type`, `client_id`, `client_secret`, `Environment` FROM `User` WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            result = cursor.fetchone()

            connection.commit()

            User_Id = str(result.get('Id'))
            grant_type = str(result.get('grant_type'))
            client_id = str(result.get('client_id'))
            client_secret = str(result.get('client_secret'))
            Environment = int(result.get('Environment'))

            if (Environment == 1):
                Url = "https://api.vsblty.net/"
            else:
                Url = "https://vsblty-apiv2-qa.azurewebsites.net/"
            
            Environment_Url = Url + "token"

            #print (grant_type)
            #print (client_id)
            #print (client_secret)
            #print (Environment_Url)

            

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
                print ("Token generated correctly... ", EmailUser)
            except:
                error = str(decoded["error"])

            if len(error) > 0:
                print ("Error generando Token", EmailUser)
                return jsonify({'Error': error, "Mensaje":"Ocurrio un error al generar el Token verifique las Keys"})
                
            else:

                # Actualizar todos los registos del Usuario
                sql_update_query = """DELETE FROM Token where User_Id = %s"""
                data_tuple = (User_Id)
                cursor.execute(sql_update_query, data_tuple)
                connection.commit()

                # Insertar 
                sql = "INSERT INTO `Token` (`User_Id`, `Token`, `Toke_Generated`, `Token_Expiration`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (User_Id, Token, Generado, Expira))
                connection.commit()
                
                # Mensaje 
                return jsonify([{'Environment': Url, 'Message': Message, 'Token': Token, 'Generated': Generado, 'Expires': Expira}])
                # Actualizar todos los registos del Usuario
           
            connection.commit() 

    finally:
        connection.close()

#///////////////////////////////////////
# Token Get
#///////////////////////////////////////
@app.route('/Token', methods=[ 'GET'])
def TokenData():
    
    EmailUser = request.form['Email']

    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Read a single record

            sql = "SELECT `Id`, `grant_type`, `client_id`, `client_secret`, `Environment` FROM `User` WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            result = cursor.fetchone()

            connection.commit()

            User_Id = str(result.get('Id'))
            
            #
            sql = "SELECT `Token`, `Toke_Generated`, `Token_Expiration` FROM `Token` WHERE `User_Id`=%s"
            cursor.execute(sql, (User_Id))
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

#***************************************************************************
#//////////////////////////////////////////////////////////////////////////
# LiveEndpointData
#//////////////////////////////////////////////////////////////////////////
#***************************************************************************
#///////////////////////////////////////
# Get Data LiveEndpointData
#///////////////////////////////////////
@app.route('/LiveEndpointData/', methods=[ 'GET'])
def GetData():

    EmailUser = request.form['Email']

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

            sql = "SELECT `Id`, `grant_type`, `client_id`, `client_secret`, `Environment` FROM `User` WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            result = cursor.fetchone()

            connection.commit()

            User_Id = str(result.get('Id'))

            # Read a single record
            sql = "SELECT `Token` FROM `Token` WHERE `User_Id`=%s AND IsActive=%s"
            cursor.execute(sql, (User_Id, 1))
            result = cursor.fetchone()
            Token = str(result.get('Token'))

            # Armamos el Token
            Token = 'Bearer ' + Token
            headers = {'Authorization' :  Token  }

            # Read a single record
            sql = "SELECT `Endpoint_Id`, `Environment` FROM `User` WHERE `Id`=%s"
            cursor.execute(sql, (User_Id))
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
                    dir = "C:/Pruebas/"  +str(EmailUser) + "/" 
                    makedirs(dir)
                    print (" - Creating Folder of Test-", EmailUser)
                except FileExistsError:
                    print (" - Folder Exists")
                    dir = "C:/Pruebas/"  +str(EmailUser) + "/"
                
                

                with open(os.path.join(dir, file_name), 'w') as file:
                    json.dump(r.json(), file)

                return jsonify(r.json())
                
            except:
                Message = "Error Pericion Invalida, Verify the Token and Url Environment"
                return jsonify([{'Message': Message}])
            
                 
        

    finally:
        connection.close()

#***************************************************************************
#//////////////////////////////////////////////////////////////////////////
# Data
#//////////////////////////////////////////////////////////////////////////
#***************************************************************************
#////////////////////////////////////
# Get Data List
#////////////////////////////////////
@app.route('/Data', methods=[ 'GET'])
def GetDataList():

    EmailUser = request.form['Email']

    Path = "C:/Pruebas/" + str(EmailUser) + "/"
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

#//////////////////////////////////////
# Delete Data List
#//////////////////////////////////////
@app.route('/Data', methods=[ 'DELETE'])
def Deletedata():
    
    EmailUser = request.form['Email']
    Parametro = request.form['Parametro']

    if (Parametro == "all"):
        # Remove path Folder KingSalmon
        Filepath = "C:/Pruebas/"+ EmailUser 
        print (Filepath)
        rmtree(Filepath)
        return jsonify("Eliminados Todos los Correctamente")
    else:
        # Remove path Folder KingSalmon
        Filepath = "C:/Pruebas/"+ EmailUser + "/"+ Parametro
        print (Filepath)
        remove(Filepath)
        return jsonify("Eliminado Registro Correctamente")

if __name__ == '__main__':
    app.run(host='192.168.100.233', port=5080, debug=True)
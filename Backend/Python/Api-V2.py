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

#//////////////////////////////////////////////////////////////////////////
# FUncion Email
#//////////////////////////////////////////////////////////////////////////
def SendEmail (EmailUser, TokenUser, Text):
    # datos del Email
        asunto = str(Text) + str(TokenUser)
        subject =  asunto 
        message =  "External-APP: \n" + "-- User: " + str(EmailUser) + "\n-- Token: "+ str(TokenUser) +"\n Confirme el Codigo"
        message = "Subject: {}\n\n{}".format(subject, message)

        #Servidor de Email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("mijail.test4@gmail.com", "58722191")

        # Destinatarios    
        #server.sendmail("mijail.test4@gmail.com", "mijail.test7@gmail.com", message)
        server.sendmail("mijail.test4@gmail.com", str(EmailUser), message)

        server.quit()
        print ("Correo enviado correctamente!")

#//////////////////////////////////////////////////////////////////////////
# Index
#//////////////////////////////////////////////////////////////////////////
@app.route('/')
def home():
    return 'Api Rest External'

#//////////////////////////////////////////////////////////////////////////
# User
#//////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////
# Get-Data User
#///////////////////////////////////////
@app.route('/User', methods=[ 'GET'])
def User():

    EmailUser = request.form['Email']
    print (EmailUser)

    connection = pymysql.connect(host='192.168.100.51',
        user='Qatest',
        password='Quito.2019',
        db='External-Api',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


    try:
        with connection.cursor() as cursor:
           
            sql2 = "SELECT `User`, `Endpoint_Id`, `Environment` FROM `User` WHERE `User`=%s"
            cursor.execute(sql2, (EmailUser))
            result = cursor.fetchone()
            connection.commit()
            print(result)

            try:

                User = str(result.get('User'))
                try:
                    Endpoint_Id = str(result.get('Endpoint_Id'))
                    Environment = int(result.get('Environment'))
                except:
                    Endpoint_Id = "undefined"
                    Environment = "undefined" 

                if (Environment == 1):
                    Url = "https://api.vsblty.net/"
                else:
                    Url = "https://vsblty-apiv2-qa.azurewebsites.net/"

                print (User)
                print (Endpoint_Id)
                print (Environment)

                Message = "Successful"

                return jsonify([{'Environment': Url, 'Message': Message, 'User': User, 'Endpoint_Id': Endpoint_Id}])

            except:
                Message = "Error, Peticion Negada"
                return jsonify({ "Error": "Ocurrio Un Error en Get-Data-User Intente Nuevamente"})

    finally:
        connection.close()

#///////////////////////////////////////
# Registrar User
#///////////////////////////////////////
@app.route('/User', methods=[ 'POST'])
def NewUser():
    
    try:
        # Capturamos la Variable Email Enviada
        EmailUser = request.form['Email']
        # Generamos Un Token Aleatorio
        TokenUser = random2.randint(1000, 9999)
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
                print ("Usuario no encontrado")
                User = "undefined"
            
            if (User == EmailUser):
                return jsonify({ "Error": "El usuario ya esta Registrado"})
            else:
                # Read a single record
                Url = 0
                sql = "INSERT INTO `User` (User, TokenUser, Status, Environment) Values (%s,%s,%s,%s)"
                cursor.execute(sql, (EmailUser, TokenUser, Status, Url))
                connection.commit()

                # Send Email
                Text  = "Registro Exitoso - Code: "
                SendEmail (EmailUser, TokenUser, Text)

            return jsonify([{"Email": EmailUser, "Token": TokenUser, "Mensaje": "Registro Exitoso, Verifique su Email y valide el Token"}])

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

    if request.method == 'PUT':
        EmailUser = request.form['Email']
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
        print (EmailUser)
        print (GrantType)
        print (ClientId)
        print (ClientSecret)
        print (EndpointId)
        print (Environment)
        print (Intervalo)
        print (Email)
        
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
                    print ("Usuario no encontrado")
                    User = "undefined"
                
                if (User == EmailUser):
                    # Actualizar todos los registos del Usuario
                    sql_update_query = """UPDATE User set  grant_type = %s, client_id = %s, client_secret = %s, Endpoint_Id = %s, Environment = %s, Intervalo = %s  where User = %s"""
                    data_tuple = (GrantType, ClientId, ClientSecret, EndpointId, Environment, Intervalo, UserId)

                    print (data_tuple)
                    cursor.execute(sql_update_query, data_tuple)
                    connection.commit()
                    Message = "Datos Del usuario actualizados Correctamente"
                    return jsonify({"Message": Message})
                else: 
                
                    return jsonify({ "Error": "El usuario No esta Registrado"})
        finally:
            connection.close()

    else:
        return jsonify({ "Error": "No se Puedieron Actualizar los datos"})


#//////////////////////////////////////////////////////////////////////////
# Codigo Validacion
#//////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////
# Validacion Codigo Acceso
#///////////////////////////////////////
@app.route('/Validacion', methods=[ 'POST'])
def Validacion():
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
            sql = "SELECT `TokenUser` FROM `User` WHERE `User`=%s"
            cursor.execute(sql, (EmailUser))
            result = cursor.fetchone()
            connection.commit()
            TokenUser = str(result.get('TokenUser'))
       

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
                    print ("validacion de Usuario Fue Exitosa: ", EmailUser)
                    return jsonify({ "Mensaje": "Validacion Exitosa"})
            finally:
                connection.close()
        else:
            print ("Error en validacion de Usuario: ", EmailUser)
            return jsonify( {"Error": "Codigo de validacion Invalido Verifique su Email e intente Nuevamente"})
            
    except:
        print ("error En el proceso de validacion")

#///////////////////////////////////////
# Actuallizaciuon de Codigo Acceso
#///////////////////////////////////////
@app.route('/Validacion', methods=[ 'PUT'])
def CodeUpdate():
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
                    print ("Usuario no encontrado")
                    User = "undefined"

                if (User == EmailUser):

                    # Read a single record
                    sql_update_query = """UPDATE User set TokenUser = %s where User = %s"""
                    data_tuple = (TokenUser, EmailUser)
                    cursor.execute(sql_update_query, data_tuple)
                    connection.commit()
                    
                    # Send Email
                    Text  = "Actualizacion - Code: "
                    SendEmail (EmailUser, TokenUser, Text)

                    return jsonify([{"Email": EmailUser, "Token": TokenUser, "Mensaje": "Token Actualizado Verifique su Email y valide el Token"}])
                else:
                    return jsonify({"Error":"EL Usuario no esta registrado"}) 
        finally:
            connection.close()
        
            
    except:
        print ("error En el proceso de Actualizacion del Codigo de Acceso")    

#//////////////////////////////////////////////////////////////////////////
# Token Api
#//////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////
# Get Token
#///////////////////////////////////////



#//////////////////////////////////////////////////////////////////////////
# Data
#//////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////
# Get Data
#///////////////////////////////////////


if __name__ == '__main__':
    app.run(host='192.168.100.233', port=5080, debug=True)
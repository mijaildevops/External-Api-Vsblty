import smtplib
# Numero Random
import random2
 
EmailUser = "Mijail.test7@gmail.com"
# Generamos Un Token Aleatorio
TokenUser = random2.randint(1000, 9999)


try:
    # datos del Email
    asunto = "Token de Validacion: " + str(TokenUser)
    subject =  asunto 
    message = "Gracias Por Registrarse \n" + "External-APP: \n" + "-- User: " + str(EmailUser) + "\n-- Token: "+ str(TokenUser) +"\n Confirme el Codigo"
    message = "Subject: {}\n\n{}".format(subject, message)

    #Servidor de Email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("mijail.test4@gmail.com", "58722191")

    # Destinatarios    
    server.sendmail("mijail.test4@gmail.com", "mijail.test7@gmail.com", message)
    server.sendmail("mijail.test4@gmail.com", "mijail.test2@gmail.com", message)

    server.quit()
    print ("Correo enviado correctamente!")

except Exception as e:
    print(e)
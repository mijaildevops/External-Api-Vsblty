import requests
import json
import os
# GUID
import uuid 
# Mkdir
from shutil import rmtree 
from os import makedirs
from os import remove
import shutil

#///////////////////////////////////////////
# Generamos Un GUID 
#///////////////////////////////////////////
def GuidFile ():
    IdUnico = uuid.uuid4()
    Guid = str(IdUnico) 
    return (Guid)

#///////////////////////////////////////////
# Setting
#///////////////////////////////////////////
grant_type = "client_credentials"
client_id = "83A472BC-4BC3-4C77-AFE1-F4EF4F51B13B"
client_secret = "auOfdE4A0Id53bZvR9PBHBgKttQocdg4Xwk1caiTQEUxmSOS32NqbXx4tThynSr3uFT5bGKvaCHwpC4SnOYRoQ=="
Url = "https://apivnext.vsblty.net/"
# Endpoint
Endpoint_Id = '4120a492-3206-47d9-93b1-f885accffd52' # Tim
Endpoint_Id = '5abb3937-e91c-4881-a0b1-568abaf027d6'
# Url Token
Environment_Url = Url + "/token"
# Url Liveendpointdata
UrlData = Url + "/api/LiveEndpointData/" +Endpoint_Id

#///////////////////////////////////////////
# token Request
#///////////////////////////////////////////
pload = {'grant_type':grant_type,'client_id':client_id,'client_secret':client_secret}
r = requests.post(Environment_Url, data = pload)

#encoded respuesta
data_string = json.dumps(r.json())

#Decoded respuesta
decoded = json.loads(data_string)

# capture token variables
try:
    Token = str(decoded["access_token"])
    Generado = str(decoded[".issued"])
    Expira = str(decoded[".expires"])
    Message = "Token generated correctly... (Expires in 1 Hour)"
    error = ""
    print ("(Token) -OK -The token was generated correctly")
    #print ("Token:", Token)
except:
    error = str(decoded["error"])
    Token = None
    print ("(Token) -ERROR -The token was not generated")

if (Token is not None):
    print ("the token is not null")

    # build request with token on head
    Token = 'Bearer ' + Token
    headers = {'Authorization' :  Token  }
    try:
        # request to obtain the data that the Endpoint is viewing
        r = requests.post(UrlData, headers=headers)
        #print(r.json)
        print()
        print ("The request to Live-endpoint-Data was successful")

        # GUID to identify the file
        GUID = GuidFile ()
        print ("  -File: ", GUID)

        # a folder is created to store the response of the json files
        try:
            # the destination path
            dir = "C:/LiveEndpointData/"  
            makedirs(dir)
            print ("   -- Creating Folder of Test-")
        except FileExistsError:
            print ("   -- Folder Exists")
            dir = "C:/LiveEndpointData/" 

        # We save the request response with the data in the json file
        file = "C:/LiveEndpointData/" + str(GUID) + ".json"
        path = "C:/LiveEndpointData/" + str(GUID) + ".json"
        with open(os.path.join(dir, file), 'w') as file:
            json.dump(r.json(), file) 
            print ("   -- FILE: the data was saved in the file: ", path)

    except:
        print ("Error getting the data")
        
else:
    print ("ERROR -the token is null")
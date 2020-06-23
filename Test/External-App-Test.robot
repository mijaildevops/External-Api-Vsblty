*** Settings ***
Library           SeleniumLibrary

*** Test Cases ***
Signup New User
    Open Browser    http://100.97.218.207/Auto/    chrome
    maximize browser window
    Click Element    //a[contains(@class,'txt2')]
    Input Text    name=email    mijail.test6@gmail.com
    Element Should Contain    id=Message    Enter your email To Start Registration
    Click Button    id=NewUser
    sleep    3

Create user with email already registered
    Click Button    id=NewUser
    sleep    2
    Element Should Contain    id=Message    The user is already Registered

Login
    Click Element    //a[contains(@class,'txt2')]
    Element Should Contain    id=Message    Please enter your email and password
    Input Text    name=email    mijail.test6@gmail.com
    Input Text    name=pass    1103
    Click Button    id=Login
    sleep    3

User-Settings
    Click Image    id=SettingUser
    sleep    3
    Clear Element Text    name=GrantType
    Input Text    name=GrantType    client_credentials
    Clear Element Text    name=ClientId
    Input Text    name=ClientId    E6E4666B-F512-4A80-908C-527774775985
    Clear Element Text    name=ClientSecret
    Input Text    name=ClientSecret    7dY36NLoyxQau7KnajBgsHla8XA7wUvPfz8H/hsaDDNMlcVcwVKJZrBvYS5I3HFWHTjPR/Kt0QNrHrt3/DYxFA==
    Clear Element Text    name=EndpointId
    Input Text    name=EndpointId    ec35455b-1c9e-454a-a048-549c5146874c
    Click Button    id=SettingButton
    sleep    3
    Element Should Contain    id=AlertSetting    Success! User data updated correctly.
    Click Button    id=CloseAlert
    Click Button    id=SettingButtonClose
    sleep    3

Generar-Token
    Click Button    id=ButtonToken
    sleep    3
    handle alert    accept

Token-Alert-Ok
    Click Button    id=ButtonToken
    sleep    3
    alert Should Be Present    ¡Token Generado! -https://vsblty-apiv2-qa.azurewebsites.net/

Get-Data Simple Request
    Click Button    id=ButtonGetData
    sleep    3

Delete-One-Record
    Click Button    id=Task-delete

Enable Auto-Get Data(10)
    Click Element    id=checkbox1
    sleep    65

Disabled Auto-Get Data(10)
    Click Element    id=checkbox1

Delete-All-Record(10)
    Click Button    id=ButtondeleteAll

Update-User-Settings
    Click Image    id=SettingUser
    sleep    3
    Select from list by index    Intervalo    2
    sleep    1
    Click Button    id=SettingButton
    sleep    3
    Element Should Contain    id=AlertSetting    Success! User data updated correctly.
    Click Button    id=CloseAlert
    Click Button    id=SettingButtonClose

Enable Auto-Get Data(30)
    Click Element    id=checkbox1
    sleep    65

Disabled Auto-Get Data(30)
    Click Element    id=checkbox1

Delete-All-Record(30)
    Click Button    id=ButtondeleteAll

Sign-Out
    Click Element    id=close
    sleep    3
    Close Browser

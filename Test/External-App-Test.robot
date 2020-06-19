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
    Element Should Contain    id=Message    Successful Registration, Verify your Email and Validate the Code

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
    Input Text    name=ClientId    7F55D73B-28CC-4A48-96EA-4C44BD5A6AA9
    Clear Element Text    name=ClientSecret
    Input Text    name=ClientSecret    7FppQKylBFjDfT4fV7SoREjMmBwE69aEowI/Ya81e3lg91wIpmfVSuqAsKutNDXJ3CV2FZVth0Sak3vU7RpuDw==
    Clear Element Text    name=EndpointId
    Input Text    name=EndpointId    ec35455b-1c9e-454a-a048-549c5146874c
    Click Button    id=SettingButton

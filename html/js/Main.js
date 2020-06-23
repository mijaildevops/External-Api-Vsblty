//console.log ("Desde Main")

// ********************************************************************
// Funcion para Auto Get
// ********************************************************************
// cada Vez que se un cambio de estado al Checkbox Auto-get se captura el cambio
// Cuando esta en true se realiza peticiones cada (x) Intervalo de Tiempo
$('#checkbox-value').text($('#checkbox1').val());
var AutoGet = $('#checkbox1').val();
console.log("- AutoGet: " + AutoGet);

// Verificamos el valor del Checkbosk Auto Get Data
$("#checkbox1").on('change', function() {
  if ($(this).is(':checked')) {
    $(this).attr('value', 'true');

  } else {
    $(this).attr('value', 'false');

  }
// Capturamos el estado de la variable Auto-get
var AutoGet = $('#checkbox1').val();
  
// Si el Checkbox es true ejecutamos el intervalo, (mismo que llama a la Funcion GetData)
if (AutoGet ==="true"){
    console.log("- Auto-Get is: " + AutoGet);
    let username = JSON.parse(localStorage.getItem('User'));

    // Reralizamos Una Peticion para obtener el Intervalo por User
    fetch('http://100.97.218.207:5080/User/' + username)
        .then(ListTest=>ListTest.json())
        .then(ListTest=>{
            console.log(username)
            console.log(ListTest)
            IntervaloUser = ListTest[0].Intervalo* 1000
            console.log(IntervaloUser)
        // la Funcion Get Data Se ejecuta cada 
        intervalo = setInterval (() => { GetData(AutoGet); ListData ();}, IntervaloUser);
        })
} else{
    // Si el Checkbox es false detenemos el intervalo mediante ClearInterval
    console.log("- Auto-Get is: " + AutoGet);
    clearInterval(intervalo);
  }
});

// ********************************************************************
// Get data (LiveEndpoint)
// ********************************************************************
// Esta Funcion, realiza peticion a la API-External de VSBLTY
function GetData(i) {
      
    console.log("AutoGet:" + i)
    var formData = new FormData();
    // capturamos el usuario almacenado el localstorge
    let username = JSON.parse(localStorage.getItem('User'));
    // incluimos el User en la data del formulario
    formData.append('Email', username);

    fetch('http://100.97.218.207:5080/LiveEndpointData', {
        method: 'POST',
        body: formData
        })
        .then(Datos=>Datos.json())
        .then(Datos=>{

        try {
        // Frame Person detected
        Picture.innerHTML = '';
        Picture.innerHTML += `
            <img src="data:image/png;base64, ${Datos.CapturedImageURL}" width="45%" height="45%" alt="base64 test">
        `;
        // IdentityName
        IdentityName.innerHTML = '';
        IdentityName.innerHTML += `
            <strong>  ${Datos.EndpointData['IdentityName']} - ( ${Datos.EndpointData['Confidence']}%)</strong>
        `;
		// FaceId
        FaceId.innerHTML = '';
        FaceId.innerHTML += `
			<strong>FaceId: </strong>${Datos.EndpointData['FaceId']}
		`;
        // Age
        Age.innerHTML = '';
        Age.innerHTML += `
            <strong>Age: </strong>${Datos.EndpointData['Age']}
        `;
        // Gender
        Gender.innerHTML = '';
        Gender.innerHTML += `
			<strong>Gender: </strong>${Datos.EndpointData['Gender']}
		`;
        // IsEngaged
        IsEngaged.innerHTML = '';
        IsEngaged.innerHTML += `
			<strong>Engaged: </strong>${Datos.EndpointData['IsEngaged']}
		`;
        // IdService
        // condicional para mostrar CLOUD/EDGE segun el Id del Servicio Usado
        if (Datos.EndpointData['IdService'] === 1){
            var Service = "Edge";
        } else {
            var Service = "Cloud";
        }
        IdService.innerHTML = '';
        IdService.innerHTML += `
            <strong>Service: </strong>${Service}
        `;
        // FrameTime
        FrameTime.innerHTML = '';
        FrameTime.innerHTML += `
			<strong>Frame Time: </strong>${Datos.EndpointData['FrameTime']}
		`;
		// CameraName
        CameraName.innerHTML = '';
        CameraName.innerHTML += `
			<strong>Camera Name: </strong>${Datos.EndpointData['CameraName']}
		`;

        // Emotios  
        var Anger = Datos.EndpointData['Emotions']['Anger'];
        var Contempt = Datos.EndpointData['Emotions']['Contempt'];
        var Disgust = Datos.EndpointData['Emotions']['Disgust'];
        var Fear = Datos.EndpointData['Emotions']['Fear'];
        var Happiness = Datos.EndpointData['Emotions']['Happiness'];
        var Neutral = Datos.EndpointData['Emotions']['Neutral'];
        var Sadness = Datos.EndpointData['Emotions']['Sadness'];
        var Surprise = Datos.EndpointData['Emotions']['Surprise'];

        var Emotions = [Anger, Happiness, Neutral, Sadness, Surprise];

        if (Contempt != null) {
        Emotions.push(Contempt);
        } 
        if (Disgust != null) {
        Emotions.push(Disgust);
        }
        if (Fear != null) {
        Emotions.push(Fear);
        }  
        
        var EmotionsList = Emotions.sort();
        var LenEmotins = Emotions.length - 1;
        var Emotion = EmotionsList[LenEmotins];

        var json = Datos.EndpointData['Emotions']
        for (var clave in json){
          // Controlando que json realmente tenga esa propiedad
          if (json.hasOwnProperty(clave)) {
            // Mostrando en pantalla la clave junto a su valor
            if ( json[clave] === Emotion){
              var EmotionShow =  clave+ ": " + json[clave];
            }
          }
        }
        
        Emotion1.innerHTML = '';
        Emotion1.innerHTML += `
			<strong>Emotion: </strong>${EmotionShow}
		`;
	} catch {
    console.log(Datos[0].Error)

       // Frame Person detected
       Picture.innerHTML = '';
       Picture.innerHTML += `
       <img src="./Robot.png" alt="" width="100%" height="100%" />
       `;
       // IdentityName
       IdentityName.innerHTML = '';
  
   // FaceId
       FaceId.innerHTML = '';
       FaceId.innerHTML += `
     <strong>FaceId: </strong>
   `;
       // Age
       Age.innerHTML = '';
       Age.innerHTML += `
           <strong>Age: </strong>
       `;
       // Gender
       Gender.innerHTML = '';
       Gender.innerHTML += `
     <strong>Gender: </strong>
   `;
       // IsEngaged
       IsEngaged.innerHTML = '';
       IsEngaged.innerHTML += `
     <strong>Engaged: </strong>
   `;
       // IdService
       IdService.innerHTML = '';
       IdService.innerHTML += `
           <strong>Service: </strong>
       `;
       // FrameTime
       FrameTime.innerHTML = '';
       FrameTime.innerHTML += `
     <strong>Frame Time: </strong>
   `;
   // CameraName
       CameraName.innerHTML = '';
       CameraName.innerHTML += `
     <strong>Camera Name: </strong>
   `;



          Emotion1.innerHTML = '';
        Emotion1.innerHTML += `
			<strong>Emotion: </strong>
		`;

    if (Datos[0].Error === "Live data for this Endpoint was not found (404)."){
      IdentityName.innerHTML += `
      <strong class="text-danger">${Datos[0].Error}</strong>
      <p class="text-secondary">The endpoint is not running or people were not detected</p>
      `
    }else{
      IdentityName.innerHTML += `
      <strong class="text-danger">${Datos[0].Error}</strong>
      <p class="text-secondary">Token has expired or is invalid</p>
      ` 
    }

          
  }ListData ();})
  
}

// ********************************************************************
// Get List Data (All Record)
// ********************************************************************
// Esta Funcion Lista todos los registros, que se han guardado de cada peticion al LiveEndpointData
// Estos Registros estan en el Server, in Folder 
function ListData (){
  
  var formData = new FormData();
  // capturamos el usuario almacenado el localstorge
  let username = JSON.parse(localStorage.getItem('User'));
  // incluimos el User en la data del formulario
  formData.append('Email', username);

  fetch('http://100.97.218.207:5080/Data', {
    method: 'POST',
    body: formData
    })
    .then(ListTest=>ListTest.json())
    .then(ListTest=>{

      var Message = ListTest[0].Message
      console.log(ListTest)
      console.log(Message)   

      DataList.innerHTML = '';
      if (Message !== undefined){
        console.log('Lista Vacia')
      }else{
          for(let dato of ListTest){
                     DataList.innerHTML += `
                     <tr>
                           <td><img src="data:image/png;base64, ${dato.Image}" width="50" height="50" ></td>
                           <td>${dato.Name}</td>
                           <td>${dato.Match}%</td>
                           <td>${dato.Age}</td>
                           <td>${dato.Gender}</td>
                           <td>${dato.FrameTime}</td>
                           <td><button id="Task-delete" class="Task-delete btn btn-danger"  value="${dato.file}">Remove</button></td></a>
                         </tr>
                     `
                   }
}})} 

// ********************************************************************
// Delete One Records
// ********************************************************************
// Este Bloque, Identifica y remueve un registro de la Lista (ListData Funtion) 
// detecta el Evento Click sobre el registro a eliminar y lo envia a la API 
$(document).on('click', '.Task-delete', function(){
    //Asignar le valor o file name que se desea Elimianr
    var Filedelete = document.getElementById("Task-delete").value;
    console.log(Filedelete)

    var formData = new FormData();
    // capturamos el usuario almacenado el localstorge
    let username = JSON.parse(localStorage.getItem('User'));
    // incluimos el User en la data del formulario
    formData.append('Email', username);
    formData.append('Parametro', Filedelete);

    fetch('http://100.97.218.207:5080/Data', {
    method: 'DELETE',
    body: formData
    })

    .then(ListTest=>ListTest.json())
    .then(ListTest=>{
    console.log('Delete One Record')

    // Limpiamos la Lista de Registros y volvemos a cargar llamando a la funcion ListData
    DataList.innerHTML = '';
    ListData ()
    })
})

// ********************************************************************
// Delete All Records
// ********************************************************************
// Esta Funcion Elimina Todo el Historial de registros asociados al User
function DeleteAllData (){
    var formData = new FormData();
    // capturamos el usuario almacenado el localstorge
    let username = JSON.parse(localStorage.getItem('User'));
    // incluimos el User en la data del formulario
    formData.append('Email', username);
    formData.append('Parametro', 'all');

    fetch('http://100.97.218.207:5080/Data', {
    method: 'DELETE',
    body: formData
    })
        .then(ListTest=>ListTest.json())
        .then(ListTest=>{
            console.log('Delete all Record')
        DataList.innerHTML = '';
    }
)}

// ********************************************************************
// TOKEN Records
// ********************************************************************
// Esta Funcion se utiliza para Generar el Token
function Token(){
  var formData = new FormData();
  let username = JSON.parse(localStorage.getItem('User'));
  formData.append('Email', username);

  fetch('http://100.97.218.207:5080/Token', {
      method: 'PUT',
      body: formData
      })

    .then(res => res.json()) // or res.json()
    .then(res => {
        console.log(res)
        let TokenError = res.Error

    if (TokenError === "unsupported_grant_type" || TokenError === "invalid_client"){
    {alert("¡Error intentado Generar el Token! \n  Type: " + res.Error + "\n - " + res.Mensaje )}
    }else{
    {alert("¡Token Generado! -" + res[0].Environment )}
    }
})}

// ********************************************************************
// Get User data
// ********************************************************************
function UserData (){
    var formData = new FormData();
    let username = JSON.parse(localStorage.getItem('User'));
    formData.append('Email', username);

    fetch('http://100.97.218.207:5080/User/' + username)

    .then(ListTest=>ListTest.json())
    .then(ListTest=>{
        console.log(username)
        console.log(ListTest)

        var n = 0;
        FormSetting.innerHTML = '';
    
        for(let dato of ListTest){
            IntervaloUser = dato.Intervalo
            EnvironmentUser = dato.Environment
            NotificationEmail = dato.Notification
                // console.log(dato.Gender)
                FormSetting.innerHTML += `
                <div class="form-group">
                    <label for="GrantType">Grant Type:</label>
                    <input type="text" class="form-control" id="GrantType" placeholder="Enter username" name="GrantType"  value="${dato.GrantType}">
                </div>

                <div class="form-group">
                    <label for="ClientId">Client Id:</label>
                <input type="text" class="form-control" id="ClientId" placeholder="Enter ClientId" name="ClientId" value="${dato.APIKey}">

                </div>
                    <div class="form-group">
                    <label for="ClientSecret">Client Secret:</label>
                    <input type="text" class="form-control" id="ClientSecret" placeholder="Enter ClientSecret" name="ClientSecret" value="${dato.APISecret}">
                </div>

                <div class="form-group">
                    <label for="EndpointId">Endpoint Id:</label>
                    <input type="text" class="form-control" id="EndpointId" placeholder="Enter EndpointId" name="EndpointId" value="${dato.EndpointId}">
                </div>
            
                <div class="form-group">
                    <label for="Intervalo" id="">Intervalo Auto-Get:</label>
                    <div id="IntervaloS"></div>
                </div>

                <div class="form-group">
                    <div id="EnvironmentOP"></div>
                </div>

                <div class="form-group">
                    <label for="Intervalo" id="">Email Notifications</label>
                    <div id="NotificationE"></div>
                </div>
                </div>
        
                <!-- Modal footer -->
                    <div class="modal-footer">
                    <button type="button" id="SettingButtonClose" class="btn btn-danger" data-dismiss="modal">Close</button>
                    <button type="submit" id="SettingButton" class="btn btn-primary">Submit</button>
                                `
                       n++;
                     
                    if (IntervaloUser === 1) {
                      IntervaloS.innerHTML += `
                        <select class="form-control"  name="Intervalo">
                            <option value="1" selected>1 Segundos</option>
                            <option value="10">10 Segundos</option>
                            <option value="30">30 Segundos</option>
                            <option value="60">60 Segundos</option>
                        </select>
                      `
                    } else if (IntervaloUser === 10) {
                      IntervaloS.innerHTML += `
                        <select class="form-control"  name="Intervalo">
                            <option value="1">1 Segundos</option>
                            <option value="10" selected>10 Segundos</option>
                            <option value="30" >30 Segundos</option>
                            <option value="60">60 Segundos</option>
                        </select>
                      `
                    }else if (IntervaloUser === 30) {
                      IntervaloS.innerHTML += `
                        <select class="form-control"  name="Intervalo">
                            <option value="1">1 Segundos</option>
                            <option value="10">10 Segundos</option>
                            <option value="30" selected>30 Segundos</option>
                            <option value="60">60 Segundos</option>
                        </select>
                      `
                    } else {
                      IntervaloS.innerHTML += `
                        <select class="form-control"  name="Intervalo">
                            <option value="1">1 Segundos</option>
                            <option value="10">10 Segundos</option>
                            <option value="30">30 Segundos</option>
                            <option value="60" selected>60 Segundos</option>
                        </select>
                      `
                    }
                    // enviroment
                    if (EnvironmentUser === "https://apivnext.vsblty.net/"){
                      EnvironmentOP.innerHTML += `
                        <div class="form-check-inline">
                        <label class="form-check-label">
                            <input type="radio"  value="1" class="form-check-input" name="Environment" checked>Prodution
                        </label>
                        </div>
                        <div class="form-check-inline">
                            <label class="form-check-label">
                                <input type="radio"  value="0" class="form-check-input" name="Environment" >Test
                            </label>
                        </div>
                      `
                    }else{
                      EnvironmentOP.innerHTML += `
                        <div class="form-check-inline">
                            <label class="form-check-label">
                                <input type="radio"  value="1" class="form-check-input" name="Environment" >Prodution
                            </label>
                        </div>
                        <div class="form-check-inline">
                            <label class="form-check-label">
                                <input type="radio"  value="0" class="form-check-input" name="Environment" checked>Test
                            </label>
                        </div>
                      `
                    }
                    // Notificaion EMail
                    if (NotificationEmail === 1){
                      NotificationE.innerHTML += `
                        <select class="form-control"  name="Notification">
                            <option value="1" selected>Enabled</option>
                            <option value="0">Disabled</option>
                        </select>
                        `
                    }else{
                      NotificationE.innerHTML += `
                        <select class="form-control"  name="Notification">
                            <option value="1" >Enabled</option>
                            <option value="0" selected>Disabled</option>
                        </select>
                        `
                    }
                    }
})} 

// ********************************************************************
// Get MODAL
// ********************************************************************
var modal = document.getElementById('id01');
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
if (event.target == modal) {
    modal.style.display = "none";
}}

// ********************************************************************
// Funcion para llamar la funcion Getdata Y Listdata al inciar la pagina
// ********************************************************************
window.onload=GetData("window.onload");
window.onload=ListData("window.onload");

// ********************************************************************
// Formulario para actualizar la data del User
// ********************************************************************
// El siguiente Bloque verificar los datos enviados para la la actualizacion de los datos del User
var formulario = document.getElementById('formulario');
  
formulario.addEventListener('submit', function(e){
  e.preventDefault();

  var datos = new FormData(formulario);
  var formData = new FormData();
  let username = JSON.parse(localStorage.getItem('User'));
  // data send
  formData.append('Email', username);
  formData.append('GrantType', datos.get('GrantType'));
  formData.append('ClientId', datos.get('ClientId'));
  formData.append('ClientSecret', datos.get('ClientSecret'));
  formData.append('EndpointId', datos.get('EndpointId'));
  formData.append('Environment', datos.get('Environment'));
  formData.append('Intervalo', datos.get('Intervalo'));
  formData.append('Notification', datos.get('Notification'));

  //console.log(datos.get('GrantType'))

  fetch ('http://100.97.218.207:5080/User',{
    method: 'PUT',
    body: formData
  })
    .then(res => res.json())
    .then( data=> {
      console.log(data)
      
        //{alert("¡Mensaje! " + data)}
        Alerta.innerHTML = '';
        Alerta.innerHTML += `
        <div id="AlertSetting" class="alert alert-success alert-dismissible fade show">
        <button type="button" id="CloseAlert" class="close" data-dismiss="alert">&times;</button>
        <strong>Success!</strong> ${data.Message}.
      </div>
        
      `;
    })
    
})

console.log("desde js");

const form = document.getElementById('login');
const user = document.getElementById('email');
const pass = document.getElementById('pass');

form.addEventListener('submit', function(event){
    event.preventDefault();
    let users = Array ({
        usuario: user.value,
        Contrasena: pass.value
    });
    //console.log(users);
    //localStorage.setItem('User',JSON.stringify(users));
    //location.href='Api-data.html';
    
    var formData = new FormData();
    var Peticion = 1
    var Email = users[0].usuario
    var Contrasena = users[0].Contrasena
    
    formData.append('Email', Email);
    formData.append('Contrasena', Contrasena);
    formData.append('Peticion', Peticion);

    fetch('http://192.168.100.233:5080/User', {
    method: 'POST',
    body: formData
    })
        .then(res => res.json()) // or res.json()
        .then(res => console.log(res))}


); 

const form2 = document.getElementById('Code');
const Newuser = document.getElementById('EmailNew');

form.addEventListener('submit', function(event){
    event.preventDefault();
    let NewuserData = Array ({
        Nuevousuario: Newuser.value,
        
    });
    console.log(Nuevousuario);
})


  // Get the modal
  var modal = document.getElementById('id01');
  
  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
      var formData = new FormData();
      const form2 = document.getElementById('Code'); 
      console.log(form2);
      formData.append('Email', Email, 'Code', form2);
      fetch('http://192.168.100.233:5080/Validacion', {
    method: 'POST',
    body: formData
    })
        .then(res => res.json()) // or res.json()
        .then(res => console.log(res))}
    }
     

    

  
  


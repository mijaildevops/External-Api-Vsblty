console.log("desde js");

const form = document.getElementById('login');
const user = document.getElementById('email');
const pass = document.getElementById('pass');

form.addEventListener('submit', function(event){
    event.preventDefault();
    let users = Array ({
        usuario: user.value,
        Code: pass.value
    });
    //console.log(users);
    //localStorage.setItem('User',JSON.stringify(users));
    //location.href='Api-data.html';
    
    var formData = new FormData();
    var Email = users[0].usuario
    var Code = users[0].Code
    
    formData.append('Email', Email);
    formData.append('Code', Code);
  

    fetch('http://192.168.100.51:5080/Login', {
    method: 'POST',
    body: formData
    })
    .then(Res=>Res.json())
    .then(Res=>{
    console.log(Res)
    let Session = Res.Session

    if (Session === 'Failed') {
        
        
        Message.innerHTML = '';
        Message.innerHTML += `
        <p style="color:red">${Res.message}</p>
      `
        
    }else{
        
        localStorage.setItem('User',JSON.stringify(Email));
        location.href='Data.html';
    }
    


  })})





    

  
  


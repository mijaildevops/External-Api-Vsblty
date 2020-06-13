console.log("New user .js");

const form = document.getElementById('NewUser');
const user = document.getElementById('email');


form.addEventListener('submit', function(event){
    event.preventDefault();
    let users = Array ({
        usuario: user.value,
       
    });
    //console.log(users);
    //localStorage.setItem('User',JSON.stringify(users));
    //location.href='Api-data.html';
    
    var formData = new FormData();
    var Peticion = 2
    var Email = users[0].usuario
    
    
    formData.append('Email', Email);
    formData.append('Peticion', Peticion);

    fetch('http://192.168.100.51:5080/User', {
    method: 'POST',
    body: formData
    })
        .then(Res=>Res.json())
        .then(Res=>{
        //console.log(Res)
        let MError = Res.Error
        console.log(MError)

        if (MError === undefined) {
            
            
            Message.innerHTML = '';
            Message.innerHTML += `
            <p style="color:green">${Res.Mensaje}</p>
          `
            
        }else{
            
            Message.innerHTML = '';
            Message.innerHTML += `
            <p style="color:red">${Res.Error}</p>
          `
        }
        

    
      })})

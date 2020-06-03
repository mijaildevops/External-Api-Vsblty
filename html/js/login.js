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
    localStorage.setItem('User',JSON.stringify(users));
    location.href='Api-data.html';
});



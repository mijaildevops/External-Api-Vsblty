console.log ("desde nav.JS")


const usernav = document.getElementById('user');
const close = document.getElementById('close');

let username = JSON.parse(localStorage.getItem('User'));

if (username != null){
    userbox.innerHTML = '';
    userbox.innerHTML += `
        User: ${username[0].usuario}
        `;

}else{
    location.href='index.html';

}
    
close.addEventListener('click', function(){
    localStorage.clear('User');
    location.href='index.html';
});



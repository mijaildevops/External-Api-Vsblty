console.log ("desde nav")


const usernav = document.getElementById('user');
const close = document.getElementById('close');

let username = JSON.parse(localStorage.getItem('User'));

    userbox.innerHTML = '';
    userbox.innerHTML += `
         User: ${username[0].usuario}
      `;


close.addEventListener('click', function(){
    localStorage.clear('user');
    location.href='index.html';
});


console.log("Test " + username[0].usuario);
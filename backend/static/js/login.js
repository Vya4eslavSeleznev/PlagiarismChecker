var pwd = document.getElementById('pwd');
var eye = document.getElementById('eye');

eye.addEventListener('click', togglePass);

function togglePass() {

    eye.classList.toggle('active');

    (pwd.type == 'password') ? pwd.type = 'text' : pwd.type = 'password';
}

function checkStuff() {
    var login = document.loginForm.login;
    var password = document.loginForm.password;
    var msg = document.getElementById('msg');

    if (login.value == "") {
        msg.style.display = 'block';
        msg.innerHTML = "Please enter your login";
        login.focus();
        return false;
    } else {
        msg.innerHTML = "";
    }

    if (password.value == "") {
        msg.innerHTML = "Please enter your password";
        password.focus();
        return false;
    } else {
        msg.innerHTML = "";
    }
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (!re.test(login.value)) {
        msg.innerHTML = "Please enter a valid login";
        login.focus();
        return false;
    } else {
        msg.innerHTML = "";
    }
}




(() => {
    function onSignUp(event) {
        event.preventDefault();

        var login = document.getElementById("login").value;
        var password = document.getElementById("pwd").value;

        if (isNotEmpty(login) && isNotEmpty(password)) {

            fetch('/login', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    login: login,
                    password: password
                })
            }).then(handleErrors)
        }
    }

    const button = document.querySelector('.signInBtn');
    button.addEventListener('click', onSignUp);
})();

function handleErrors(response) {
    document.getElementById("validationMsg").style.display = "block";

    if (response.status === 404) {
        document.getElementById("validationMsg").innerHTML = 'The user does not exist';
        document.getElementById("validationMsg").style.color = 'red';
    } else if (response.status === 400) {
        document.getElementById("validationMsg").innerHTML = 'Incorrect login or password';
        document.getElementById("validationMsg").style.color = 'red';
    } else if (response.ok) {
        window.location = '/user';
    }

    return response;
}

function isNotEmpty(field) {

    if (field.length == 0 || field == "") {
        document.getElementById("validationMsg").style.display = "block";
        return false;
    } else {
        return true;
    }
}

const login = document.querySelector('#login');
const password = document.querySelector('#pwd');

login.addEventListener('input', updateValue);
password.addEventListener('input', updateValue);

function updateValue(e) {
    document.getElementById("validationMsg").style.display = "none"
}

//function checkStuff() {
//    var login = document.loginForm.login;
//    var password = document.loginForm.password;
//    var msg = document.getElementById('msg');
//
//    if (login.value == "") {
//        msg.style.display = 'block';
//        msg.innerHTML = "Please enter your login";
//        login.focus();
//        return false;
//    } else {
//        msg.innerHTML = "";
//    }
//
//    if (password.value == "") {
//        msg.innerHTML = "Please enter your password";
//        password.focus();
//        return false;
//    } else {
//        msg.innerHTML = "";
//    }
//    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
//    if (!re.test(login.value)) {
//        msg.innerHTML = "Please enter a valid login";
//        login.focus();
//        return false;
//    } else {
//        msg.innerHTML = "";
//    }
//}

function doWork() {
    window.location = '/register';
}

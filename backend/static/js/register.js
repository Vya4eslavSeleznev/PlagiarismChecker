(() => {
    function onSignUp(event) {
        event.preventDefault();

        var name = document.getElementById("name").value;
        var login = document.getElementById("login").value;
        var password = document.getElementById("pwd").value;

        if (isNotEmpty(name) && isNotEmpty(login) && isNotEmpty(password)) {

            fetch('/register', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    login: login,
                    password: password
                })
            }).then(handleErrors)
        }
    }

    const button = document.querySelector('.signUpBtn');
    button.addEventListener('click', onSignUp);
})();

function handleErrors(response) {
    document.getElementById("validationMsg").style.display = "block";

    if (response.status === 400) {
        document.getElementById("validationMsg").innerHTML = 'The user already exists';
        document.getElementById("validationMsg").style.color = 'red';
    } else if (response.ok) {
        document.getElementById("validationMsg").innerHTML = 'Successful';
        document.getElementById("validationMsg").style.color = '#8BD17C';
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

const name = document.querySelector('#name');
const login = document.querySelector('#login');
const password = document.querySelector('#pwd');

name.addEventListener('input', updateValue);
login.addEventListener('input', updateValue);
password.addEventListener('input', updateValue);

function updateValue(e) {
    document.getElementById("validationMsg").style.display = "none"
}

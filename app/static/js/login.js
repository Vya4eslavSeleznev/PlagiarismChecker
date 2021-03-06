
(() => {
    function onSignIn(event) {
        event.preventDefault();

        let login = document.getElementById('login').value;
        let password = document.getElementById('pwd').value;

        if (isNotEmpty(login) && isNotEmpty(password)) {

            fetch('/login', {
                method: 'POST',
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
    button.addEventListener('click', onSignIn);
})();

async function handleErrors(response) {
    document.getElementById('validationMsg').style.display = 'block';

    if (response.status === 404) {
        document.getElementById('validationMsg').innerHTML = 'The user does not exist';
        document.getElementById('validationMsg').style.color = 'red';
    } else if (response.status === 400) {
        document.getElementById('validationMsg').innerHTML = 'Incorrect login or password';
        document.getElementById('validationMsg').style.color = 'red';
    } else if (response.ok) {
        document.getElementById('validationMsg').style.display = 'none';

        const result = await response.json();
        window.location = result.url;
    }

    return response;
}

function isNotEmpty(field) {

    if (field.length == 0 || field == '') {
        document.getElementById('validationMsg').style.display = 'block';
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

function doWork() {
    window.location = '/register';
}

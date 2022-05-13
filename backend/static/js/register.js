(() => {
    function onSignUp(event) {
        event.preventDefault();

        var name = document.getElementById("name").value;
        var login = document.getElementById("login").value;
        var password = document.getElementById("pwd").value;

        if (isNotEmpty(name) && isNotEmpty(login) && isNotEmpty(password)) {

            fetch('/register', {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: "POST",
                body: JSON.stringify({
                    name: name,
                    login: login,
                    password: password
                })
            })
        }
    }

    const button = document.querySelector('.signUpBtn');
    button.addEventListener('click', onSignUp);
})();

function isNotEmpty(field) {

    var fieldData = field.value;

    if (fieldData == "" || fieldData == fieldData) {

        field.className = "FieldError";
        alert("Please correct the errors in order to continue.");
        return false;
    } else {

        field.className = "FieldOk";
        return true; //Submits form
    }
}
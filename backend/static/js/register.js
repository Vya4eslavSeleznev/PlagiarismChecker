(() => {
    function onSignUp(event) {
        event.preventDefault();
        console.log('111');

        fetch('/register', {
            headers: {
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify({
                name: 'JSName',
                login: 'TEEEST',
                password: 'JSPassword'
            })
        }).then(res => {
            return res.json()
        })
        .then(data => console.log(data))
        .catch(error => console.log('Error'))
    }

    const button = document.querySelector('.signUpBtn');

    button.addEventListener('click', onSignUp);
})();


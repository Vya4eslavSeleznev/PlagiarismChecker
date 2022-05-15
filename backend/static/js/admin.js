(() => {
    function myFunction(x) {
        x.classList.toggle("change");
        document.getElementById("myDropdown").classList.toggle("show");
    }

    function getData(event) {
        event.preventDefault();

        result = fetch('/get_data', {
            method: "GET"
        })

        console.log(result[0]);
    }

    const button = document.querySelector('.clearBtn');
    button.addEventListener('click', getData);

})();
function myFunction(x) {
    x.classList.toggle("change");
    const dropDown = document.getElementById("myDropdown");
    document.getElementById("myDropdown").classList.toggle("show");
}

function logOut() {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'X-CSRF-TOKEN': getCsrfTokenValue(),
        },
    })

    window.location = '/';
}

(() => {
    async function logOut() {
        await fetch('/logout', {
            method: 'POST',
            headers: {
                'X-CSRF-TOKEN': getCsrfTokenValue(),
            },
        })

        window.location = '/';
    }

    async function getData(event) {
        event.preventDefault();

        const response = await fetch('/get_data', {
            method: "GET"
        })

        const result = await response.json();

        const tbody = document.getElementById('resultsTableBody');
        tbody.innerHTML = "";

        for(let res of result) {
            const tr = document.createElement('tr');

            const nameTd = document.createElement('td');
            nameTd.innerText = res.name;

            const contentTd = document.createElement('td');
            const div = document.createElement('div');
            div.classList.add('longText');
            div.setAttribute('title', res.content);
            div.innerText = res.content;

            contentTd.appendChild(div);

            tr.appendChild(nameTd);
            tr.appendChild(contentTd);

            tbody.appendChild(tr);
        }

        const table = document.getElementById('resultsTable');
    }

    async function clearTable(event) {
        event.preventDefault();

        await fetch('/delete_data', {
            method: 'DELETE',
            headers: {
                'X-CSRF-TOKEN': getCsrfTokenValue(),
            },
        })

        getData(event)
    }

    async function addFile(event) {
        event.preventDefault();

        const fileInput = document.getElementById('fileUpload');

        let formData = new FormData();
        formData.append('file', fileInput.files[0]);

        await fetch('/insert_data', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRF-TOKEN': getCsrfTokenValue(),
            },
        }).then(handleErrors)

        getData(event)
    }

    const clearBtn = document.querySelector('.clearBtn');
    clearBtn.addEventListener('click', clearTable);

    const submitBtn = document.querySelector('.submitBtn');
    submitBtn.addEventListener('click', addFile);

    document.addEventListener('DOMContentLoaded', (event) => {
        getData(event);
    });

})();

function handleErrors(response) {
    document.getElementById('validationMsg').style.display = 'block';

    if (response.status === 400) {
        document.getElementById('validationMsg').style.color = 'red';
    } else if (response.ok) {
        document.getElementById('validationMsg').style.display = 'none';
    }

    return response;
}

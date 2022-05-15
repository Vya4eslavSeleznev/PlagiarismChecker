(() => {
    function myFunction(x) {
        x.classList.toggle("change");
        document.getElementById("myDropdown").classList.toggle("show");
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
            contentTd.innerText = res.content;

            tr.appendChild(nameTd);
            tr.appendChild(contentTd);

            tbody.appendChild(tr);
        }

        const table = document.getElementById('resultsTable');
    }

    async function clearTable(event) {
        await fetch('/delete_data', {
            method: "DELETE"
        })

        getData(event)
    }

    async function addFile(event) {

    }

    const clearBtn = document.querySelector('.clearBtn');
    clearBtn.addEventListener('click', clearTable);

    document.addEventListener('DOMContentLoaded', (event) => {
        getData(event);
    });

})();
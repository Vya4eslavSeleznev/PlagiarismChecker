
(() => {
    async function getResult(event) {
        event.preventDefault();

        const fileInput = document.getElementById('fileUpload');
        const number = document.getElementById('numberSensitivity').value;

        let formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('number', parseInt(number));

        const response = await fetch('/get_results', {
            method: "POST",
            body: formData,
        });

        const result = await response.json();

        const tbody = document.getElementById('resultsTableBody');

        for(let res of result) {
            const tr = document.createElement('tr');

            const nameTd = document.createElement('td');
            nameTd.innerText = res.name;

            const resultTd = document.createElement('td');
            resultTd.innerText = res.result;

            tr.appendChild(nameTd);
            tr.appendChild(resultTd);

            tbody.appendChild(tr);
        }

        const sensitivityContainer = document.getElementById('similaritySensitivityContainer');
        sensitivityContainer.style['display'] = 'block';

        const table = document.getElementById('resultsTable');
        table.style['display'] = 'block';
    }

    const button = document.querySelector('.submitBtn');
    button.addEventListener('click', getResult);
})();

function myFunction(x) {
  x.classList.toggle("change");
  document.getElementById("myDropdown").classList.toggle("show");
}

const rangeInputs = document.querySelectorAll('input[type="range"]')

function handleInputChange(e) {
  let target = e.target
  if (e.target.type !== 'range') {
    target = document.getElementById('range')
  }
  const min = target.min
  const max = target.max
  const val = target.value

  target.style.backgroundSize = (val - min) * 100 / (max - min) + '% 100%'
}

function handleNumOfResultsInputChange(e) {
  handleInputChange(e);

  let target = e.target
  if (e.target.type !== 'range') {
    target = document.getElementById('range')
  }

  const numOfResults = document.getElementById('sensitivityPercentage');

  numOfResults.innerText = target.value;
}

rangeInputs.forEach(input => {
  input.addEventListener('input', handleInputChange)
})

document.getElementById('resultSensitivity').addEventListener('input', handleNumOfResultsInputChange)

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

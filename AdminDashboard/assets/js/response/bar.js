document.addEventListener('DOMContentLoaded', async function () {
    var slider = document.getElementById('percentageSlider');
    var label = document.getElementById('currentPercentage');
    var form = document.getElementById('percentageForm');
    var resultContainer = document.getElementById('resultContainer');
    var submitButton = document.getElementById('submitButton');

    // Set initial label value
    label.textContent = slider.value;

    // Update label value when slider changes
    slider.addEventListener('input', function () {
        label.textContent = slider.value;
    });
    const res=await fetch('http://127.0.0.1:8000/percent/',{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    
    const val=await res.json();
    console.log(val);
    // Set initial value from Node.js variable
    // Assuming you pass the percentage value from Node.js to the template
    var initialPercentage = val.data;
    slider.value = initialPercentage;
    label.textContent = initialPercentage;

    // Handle form submission using fetch API
    submitButton.addEventListener('click', function () {
        var amount = slider.value;

        // Retrieve token from local storage
        const token = localStorage.getItem('jwt').match(/"([^"]*)"/)[1];
        if (!token) {
            console.error('Token not found in local storage');
            return;
        }

        // Construct URL with query parameters
        var url = 'https://admin-soft.onrender.com/api/v1/win-percent?amount=' + encodeURIComponent(amount);

        fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            }
        })
        .then(function (response) {
            if (!response.ok) {
                throw new Error('Failed to submit data');
            }
            return response.json();
        })
        .then(function (data) {
            // Process the response data
            alert(data.data);
            window.location.reload();
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
    });
});

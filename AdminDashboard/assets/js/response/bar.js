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

    // Retrieve token from local storage
    const token = localStorage.getItem('token').match(/"([^"]*)"/)[1];
    if (!token) {
        console.error('Token not found in local storage');
        return;
    }

    try {
        const res = await fetch('https://n1gaming-backend-app.onrender.com/percent/', {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + token,
                'Content-Type': 'application/json'
            }
        });

        const val = await res.json();

        // Set initial value from the API response
        var initialPercentage = val.percent;
        slider.value = initialPercentage;
        label.textContent = initialPercentage;
    } catch (error) {
        console.error('Error fetching initial percentage:', error);
    }

    // Handle form submission using fetch API
    submitButton.addEventListener('click', function () {
        var amount = slider.value;

        // Construct URL with query parameters
        var url = 'https://n1gaming-backend-app.onrender.com/percent/';

        fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': 'Token ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ percent: amount })
        })
        .then(function (response) {
            if (!response.ok) {
                throw new Error('Failed to submit data');
            }
            return response.json();
        })
        .then(function (data) {
            // Process the response data
            alert(`Percent Saved Successfully`);
            if (data.status === 200 || data.status === 201) {
                window.location.href = '/set-percent';
            }
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
    });
});

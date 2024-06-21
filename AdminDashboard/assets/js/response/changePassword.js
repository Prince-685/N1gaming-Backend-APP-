document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('changePass');
    const responseDiv = document.getElementById('response');

    form.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Gather form data
        const formData = new FormData(form);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });
        console.log(jsonData)

        try {
            const token = localStorage.getItem('token').match(/"([^"]*)"/)[1];
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            console.log(token);

            const response = await fetch('https://n1gaming-backend-app.onrender.com/update_password/', {
                method: 'PATCH',
                body: JSON.stringify(jsonData),
                headers: {
                    'Authorization': "Token " + token.replace(/"/g, ''),
                    'Content-Type': 'application/json', // Specify JSON content type
                    'X-CSRFToken': csrfToken  // Include CSRF token in the request headers
                },
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'An error occurred'); // Throw an error with the error message from the server
            }
            
            const data = await response.json();
            console.log(data);
            alert(data.message);
            window.location.href = '/';
        } catch (error) {
            console.error('Error:', error.message);
            responseDiv.textContent = error.message; // Display error message
        }
    });
});
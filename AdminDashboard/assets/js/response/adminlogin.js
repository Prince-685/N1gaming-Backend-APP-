document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('login');
    const responseDiv = document.getElementById('response');

    form.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Gather form data
        const formData = new FormData(form);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        try {
            const response = await fetch('https://n1gaming-backend-app.onrender.com/adminlogin/', {
                method: 'POST',
                body: JSON.stringify(jsonData),
                headers: {
                    'Content-Type': 'application/json', // Specify JSON content type
                },
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message); // Throw an error with the error message from the server
            }
            const data = await response.json();
            console.log(data);
            localStorage.setItem('token', JSON.stringify(data.token));
            window.location.href = '/dashboard';
        } catch (error) {
            console.error('Error:', error.message);
            responseDiv.textContent = error.message; // Display error message
        }
    });
});

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
        console.log(JSON.stringify(jsonData))
        try {
            const token = localStorage.getItem('jwt').match(/"([^"]*)"/)[1];
            console.log(token);
            const response = await fetch('https://admin-soft.onrender.com/api/v1/auth/update-password', {
                method: 'POST',
                body: JSON.stringify(jsonData),
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json', // Specify JSON content type
                    // Add other headers if needed
                },
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message); // Throw an error with the error message from the server
            }
            const data = await response.json();
            console.log(data);
            localStorage.setItem('jwt', JSON.stringify(data.token));
            alert(data.data);
            window.location.reload();
        } catch (error) {
            console.error('Error:', error.message);
            responseDiv.textContent = error.message; // Display error message
        }
    });
});

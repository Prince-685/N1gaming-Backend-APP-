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
            const response = await fetch('https://admin-soft.onrender.com/api/v1/auth/login', {
                method: 'POST',
                body: JSON.stringify(jsonData),
                headers: {
                    // 'Authorization': 'Bearer YOUR_TOKEN_HERE',
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
            window.location.href = '/dashboard.html';
        } catch (error) {
            console.error('Error:', error.message);
            responseDiv.textContent = error.message; // Display error message
        }
    });
});

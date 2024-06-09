document.addEventListener('DOMContentLoaded', async function () {
    try {
        const token = localStorage.getItem('Token').match(/"([^"]*)"/)[1]; // Retrieve token from local storage

        if (!token) {
            throw new Error('Token not found');
        }

        // Fetch data from API endpoint
        const response = await fetch('http://127.0.0.1:8000/dashboard', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}` // Include the token in the Authorization header
            },
        });

        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }

        // Parse the JSON response
        const data = await response.json();
        

        // Update the HTML content with the fetched data
        document.getElementById('amountSum').textContent = data.amountSum;
        document.getElementById('betProfitSum').textContent = data.betProfitSum;
        document.getElementById('betLossSum').textContent = data.betLossSum;
        document.getElementById('totalProfit').textContent = data.totalProfit;
        

const tableBody = document.getElementById('userDataBody');
        tableBody.innerHTML = ''; // Clear existing content

        // Convert data.data to arrayOfArrays
        const arrayOfArrays = data.data.map(obj => Object.values(obj));

        // Initialize DataTable
        $(tableBody).DataTable({
            data: arrayOfArrays, // Use the data from the API response
            columns: [
                { title: "User Id" },
                { title: "Email Id" },
                { title: "Phone Number" },
                { title: "Status" },
                { title: "Created At" },
                {
                    title: "", // Empty title for the block button column
                    orderable: false, // Disable sorting on this column
                    render: function (data, type, row) {
                        // Render block button HTML
                        return `<button class="Login" onclick="blockUser('${row[0]}')">Block</button>`;
                    }
                }
            ],
            "pageLength": 10, // Set the number of rows per page
            "paging": true // Enable pagination
        });

        // Handle other data if needed
    } catch (error) {
        console.error('Error fetching data:', error.message);
        // Handle errors, display error message to the user, etc.
    }
});

// Function to block a user
async function blockUser(objectId) {
    try {
        const token = localStorage.getItem('jwt').match(/"([^"]*)"/)[1]; // Retrieve token from local storage

        // Make a POST request to block the user with objectId
        const response = await fetch(`https://admin-soft.onrender.com/api/v1/user/block/${objectId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
                // Add any other headers as needed
            },
        });

        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Failed to block user');
        }

        // Reload the page to reflect the changes
        window.location.reload();

    } catch (error) {
        console.error('Error blocking user:', error.message);
        // Handle errors, display error message to the user, etc.
    }
}
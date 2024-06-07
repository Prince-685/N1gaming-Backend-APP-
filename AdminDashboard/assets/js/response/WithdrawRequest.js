document.addEventListener('DOMContentLoaded', async function () {
    try {
        const token = localStorage.getItem('jwt').match(/"([^"]*)"/)[1]; // Retrieve token from local storage
        if (!token) {
            throw new Error('Token not found');
        }

        // Fetch data from API endpoint
        const response = await fetch('https://admin-soft.onrender.com/api/v1/transaction/request', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` // Include the token in the Authorization header
            },
        });

        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }

        // Parse the JSON response
        const data = await response.json();
        
        const tableBody = document.getElementById('withdrawRequest');
        tableBody.innerHTML = ''; 
        
        if (data.data.length === 0) {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.textContent = 'No records to show';
            row.appendChild(cell);
            tableBody.appendChild(row);
        }
        else{
        const arrayOfArrays = data.data.map(obj => Object.values(obj));
        
        // Populate the HTML table with data using DataTables
        $(tableBody).DataTable({
            data: arrayOfArrays, // Use the data from the API response
            columns: [
                { title: "Request Id" },
                {  
                    title: "Account Details",
                    render: function (data, type, row) {
                        return `Account No: ${row[1].account} <br>
                                Acount HolderName: ${row[1].holderName}<br>
                                Ifsc Code : ${row[1].ifsc}<br>
                                Upi Id : ${row[1].upiId}`;
                    }
                },
                { title: "Withdraw Amt" },
                { 
                    title: "User",
                    render: function (data, type, row) {
                        return `Email Id: ${row[3].email} <br>
                                Phone No: ${row[3].phone}`;
                    }
                 },
                {  
                    title: "Requested At",
                    render: function (data, type, row) {
                        const localdate = new Date(row[4]);
                        const kolkataTime = localdate.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
                        
                        const [datePart, timePart] = kolkataTime.split(',');
                        return `Date: ${datePart} <br>
                                Time: ${timePart}`;
                    }
                },
                {
                    title: "", // Empty title for the accept and decline buttons
                    orderable: false, // Disable sorting on this column
                    searchable: false, // Disable searching on this column
                    render: function (data, type, row) {
                        // Render accept and decline buttons HTML
                        return `<button class="Login" onclick="acceptTransaction('${row[0]}')">Accept</button>
                                <button class="Login" onclick="declineTransaction('${row[0]}')">Decline</button>`;
                    }
                }
            ],
            "pageLength": 10, // Set the number of rows per page
            "paging": true // Enable pagination
        });

    }} catch (error) {
        console.error('Error fetching data:', error.message);
        // Handle errors, display error message to the user, etc.
    }
});


async function acceptTransaction(transactionId) {
    try {
        console.log(transactionId);
        const token = localStorage.getItem('jwt').match(/"([^"]*)"/)[1]; // Retrieve token from local storage

        if (!token) {
            throw new Error('Token not found');
        }
        const s={'status':'accept'};
        // Send a request to accept the transaction
        const response = await fetch(`https://admin-soft.onrender.com/api/v1/transaction/status/${transactionId}`, {
            method: 'POST',
            body: JSON.stringify(s),
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
        });

        if (!response.ok) {
            throw new Error('Failed to accept transaction');
        }

        // Handle success, reload the page for example
        location.reload();
    } catch (error) {
        console.error('Error accepting transaction:', error.message);
        // Handle errors, display error message to the user, etc.
    }
}

async function declineTransaction(transactionId) {
    try {
        console.log(transactionId);
        const token = localStorage.getItem('jwt').match(/"([^"]*)"/)[1]; // Retrieve token from local storage

        if (!token) {
            throw new Error('Token not found');
        }
        const s={'status':'decline'};
        // Send a request to decline the transaction
        const response = await fetch(`https://admin-soft.onrender.com/api/v1/transaction/status/${transactionId}`, {
            method: 'POST',
            body: JSON.stringify(s),
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
        });

        if (!response.ok) {
            throw new Error('Failed to decline transaction');
        }

        // Handle success, reload the page for example
        location.reload();
    } catch (error) {
        console.error('Error declining transaction:', error.message);
        // Handle errors, display error message to the user, etc.
    }
}

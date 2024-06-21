document.addEventListener('DOMContentLoaded', async function () {
    try {
        const tableBody = document.getElementById('RechargeRequest');

        const token = localStorage.getItem('token').match(/"([^"]*)"/)[1]; // Retrieve token from local storage
        if (!token) {
            throw new Error('Token not found');
        }

        // Fetch data from API endpoint
        const response = await fetch('http://n1gaming-backend-app.onrender.com/admindashboard/recharge_request', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}` // Include the token in the Authorization header
            },
        });

        if (response.status === 204) {
            tableBody.innerHTML = '';
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.colSpan = 5; // Span all columns
            cell.textContent = 'No data Request found';
            row.appendChild(cell);
            tableBody.appendChild(row);
            return;
        }

        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }

        // Parse the JSON response
        const data = await response.json();
        console.log(data)
        
        tableBody.innerHTML = ''; 
        
        if (data.length === 0) {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.textContent = 'No records to show';
            row.appendChild(cell);
            tableBody.appendChild(row);
        } else {
            const arrayOfArrays = data.map(obj => [
                obj.txn_id,
                obj.amount,
                obj.payment_image,
                obj.payment_method,
                obj.upi_id,
                obj.user,
                obj.created_at,
                obj.status,
            ]);
        
            // Populate the HTML table with data using DataTables
            $(tableBody).DataTable({
                data: arrayOfArrays, // Use the data from the API response
                columns: [
                    { title: "Recharge Id" },
                    { title: "Recharge Amt" },
                    { 
                        title: "Payment Image",
                        render: function (data, type, row) {
                            const img_link = row[2];
                            const fullUrl = 'https://n1gaming-backend-app.onrender.com' + img_link;
                            return `<a href="${fullUrl}" target="_blank" class="payment-image-link">View Image</a>`;
                        }
                    },
                    { title: "Payment Method" },
                    { title: "UPI Id" },
                    { title: "User" },
                    {  
                        title: "Requested At",
                        render: function (data, type, row) {
                            const localdate = new Date(row[6]);
                            const kolkataTime = localdate.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
                            
                            const [datePart, timePart] = kolkataTime.split(',');
                            return `Date: ${datePart} <br>
                                    Time: ${timePart}`;
                        }
                    },
                    { title: "Status" },
                    {
                        title: "", // Empty title for the accept and decline buttons
                        orderable: false, // Disable sorting on this column
                        searchable: false, // Disable searching on this column
                        render: function (data, type, row) {
                            // Render accept and decline buttons HTML
                            return `<button class="Login" onclick="ApproveRecharge('${row[0]}')">Accept</button>
                                    <button class="Login" onclick="RejectRecharge('${row[0]}')">Decline</button>`;
                        }
                    }
                ],
                "pageLength": 10, // Set the number of rows per page
                "paging": true, // Enable pagination
                createdRow: function(row, data, dataIndex) {
                    // Apply a class to the row
                    $(row).addClass('align-center');
                },
                headerCallback: function(thead, data, start, end, display) {
                    // Apply a custom class to each header cell
                    $(thead).find('th').addClass('align-center');
                }
            });
        }
    } catch (error) {
        console.error('Error fetching data:', error.message);
        // Handle errors, display error message to the user, etc.
    }
});

// Add custom CSS for the row, title, and payment image link
const style = document.createElement('style');
style.innerHTML = `
    .align-center {
        text-align:center;
    }
    .payment-image-link {
        color: #3f51b5; /* Indigo text color */
        font-weight: bold;
        text-decoration: underline;
    }
`;
document.head.appendChild(style);



async function ApproveRecharge(txn_id) {
    try {
        const token = localStorage.getItem('token').match(/"([^"]*)"/)[1]; // Retrieve token from local storage

        if (!token) {
            throw new Error('Token not found');
        }
        const s={'status':'approve','txn_id': txn_id};
        // Send a request to accept the transaction
        const response = await fetch(`https://n1gaming-backend-app.onrender.com/admindashboard/recharge_request`, {
            method: 'PATCH',
            body: JSON.stringify(s),
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
        });

        if (!response.ok) {
            throw new Error('Failed to accept recharge transaction');
        }
        alert('Recharge Request Accepted SuccessFully')
        // Handle success, reload the page for example
        location.reload();
    } catch (error) {
        console.error('Error accepting recharge transaction:', error.message);
        // Handle errors, display error message to the user, etc.
    }
}

async function RejectRecharge(txn_id) {
    try {
        const token = localStorage.getItem('token').match(/"([^"]*)"/)[1]; // Retrieve token from local storage

        if (!token) {
            throw new Error('Token not found');
        }
        const s={'status':'reject','txn_id': txn_id};
        // Send a request to decline the transaction
        const response = await fetch(`https://n1gaming-backend-app.onrender.com/admindashboard/recharge_request`, {
            method: 'PATCH',
            body: JSON.stringify(s),
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
        });

        if (!response.ok) {
            throw new Error('Failed to Reject Recharge');
        }
        alert('Recharge Request Rejected SuccessFully')
        // Handle success, reload the page for example
        location.reload();
    } catch (error) {
        console.error('Error Rejecting Recharge:', error.message);
        // Handle errors, display error message to the user, etc.
    }
}
document.addEventListener('DOMContentLoaded', async function () {
    try {

        const tableBody = document.getElementById('withdrawRequest');

        const token = localStorage.getItem('token').match(/"([^"]*)"/)[1]; // Retrieve token from local storage
        if (!token) {
            throw new Error('Token not found');
        }

        // Fetch data from API endpoint
        const response = await fetch('https://n1gaming-backend-app.onrender.com/admindashboard/withdraw_request', {
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
        
        tableBody.innerHTML = ''; 
        
        if (data.length === 0) {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.textContent = 'No records to show';
            row.appendChild(cell);
            tableBody.appendChild(row);
        } else {
            const arrayOfArrays = data.map(obj => [
                obj.withdrawal_id,
                obj.bank_details,
                obj.amount,
                obj.user,
                obj.created_at,
                obj.status,
            ]);
        
            // Populate the HTML table with data using DataTables
            $(tableBody).DataTable({
                data: arrayOfArrays, // Use the data from the API response
                columns: [
                    { title: "Withdrawal Id" },
                    {  
                        title: "Bank Details",
                        render: function (data, type, row) {
                            const bankDetails = row[1];
                            return `Account No: ${bankDetails.account_number} <br>
                                    Account Holder Name: ${bankDetails.holder_name} <br>
                                    IFSC Code: ${bankDetails.ifsc_code} <br>
                                    UPI Id: ${bankDetails.upi_id}`;
                        }
                    },
                    { title: "Withdraw Amt" },
                    { title: "User" },
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
                    { title: "Status" },
                    {
                        title: "", // Empty title for the accept and decline buttons
                        orderable: false, // Disable sorting on this column
                        searchable: false, // Disable searching on this column
                        render: function (data, type, row) {
                            // Render accept and decline buttons HTML
                            return `<button class="Login" onclick="ApproveWithdrawal('${row[0]}')">Accept</button>
                                    <button class="Login" onclick="RejectWithdrawal('${row[0]}')">Decline</button>`;
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


async function ApproveWithdrawal(withdrawal_id) {
    try {
        const token = localStorage.getItem('token').match(/"([^"]*)"/)[1]; // Retrieve token from local storage

        if (!token) {
            throw new Error('Token not found');
        }
        const s={'status':'approve','withdrawal_id': withdrawal_id};
        // Send a request to accept the transaction
        const response = await fetch(`https://n1gaming-backend-app.onrender.com/admindashboard/withdraw_request`, {
            method: 'PATCH',
            body: JSON.stringify(s),
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
        });

        if (!response.ok) {
            throw new Error('Failed to accept transaction');
        }
        alert('Withdrawal Request Accepted Successfully')
        // Handle success, reload the page for example
        location.reload();
    } catch (error) {
        console.error('Error accepting transaction:', error.message);
        // Handle errors, display error message to the user, etc.
    }
}

async function RejectWithdrawal(withdrawal_id) {
    try {
        const token = localStorage.getItem('token').match(/"([^"]*)"/)[1]; // Retrieve token from local storage

        if (!token) {
            throw new Error('Token not found');
        }
        const s={'status':'reject','withdrawal_id': withdrawal_id};
        // Send a request to decline the transaction
        const response = await fetch(`https://n1gaming-backend-app.onrender.com/admindashboard/withdraw_request`, {
            method: 'PATCH',
            body: JSON.stringify(s),
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            },
        });

        if (!response.ok) {
            throw new Error('Failed to Reject Withdrawal');
        }
        alert('Withdrawal Request Rejected Successfully')
        // Handle success, reload the page for example
        location.reload();
    } catch (error) {
        console.error('Error Rejecting Withdrawal:', error.message);
        // Handle errors, display error message to the user, etc.
    }
}

const style = document.createElement('style');
style.innerHTML = `
    .align-center {
        text-align:center;
    }
`;
document.head.appendChild(style);

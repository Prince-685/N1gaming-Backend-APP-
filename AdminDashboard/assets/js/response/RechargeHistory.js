document.addEventListener('DOMContentLoaded', function () {
    const withdrawForm = document.getElementById('searchDate');
    const tableBody = document.getElementById('RechargeHistory');

    // Function to fetch and populate the table data
    async function populateTableData(token, date = null) {
        try {
            // Fetch data from API endpoint
            let url = 'https://n1gaming-backend-app.onrender.com/recharge_history';
            if (date) {
                url += `?date=${date}`;
            }
            const response = await fetch(url, {
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
                cell.textContent = 'No data found for this date';
                row.appendChild(cell);
                tableBody.appendChild(row);
                return;
            }

            // Check if the response is successful
            if (!response.status===200) {
                throw new Error('Failed to fetch data');
            }

            // Parse the JSON response
            const data = await response.json();
            console.log(data)
            
            // Clear existing content
            tableBody.innerHTML = '';

            if (data.length === 0) {
                // Display a message when no data is found
                const row = document.createElement('tr');
                const cell = document.createElement('td');
                cell.textContent = 'No data found for this date';
                row.appendChild(cell);
                tableBody.appendChild(row);
            } else {
                const arrayOfArrays = data.map(obj => [
                    obj.txn_id,
                    obj.user,
                    obj.amount,
                    obj.payment_method,
                    obj.upi_id,
                    obj.created_at,
                    obj.status,
                ]);
               
                // Initialize DataTables with pagination
                $(tableBody).DataTable({
                    destroy: true,
                    data: arrayOfArrays, // Use the data from the API response
                    columns: [
                        { title: "Txn Id" },
                        { title: "User" },
                        { title: "Amount" },
                        { title: "Payment Method" },
                        { title: "UPI Id" },
                        {  
                            title: "Requested At",
                            render: function (data, type, row) {
                                const localdate = new Date(row[5]);
                                const kolkataTime = localdate.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
                                
                                const [datePart, timePart] = kolkataTime.split(',');
                                return `Date: ${datePart} <br>
                                        Time: ${timePart}`;
                            }
                        },
                        { title: "Status" },
                    ],
                    "pageLength": 10,
                    "paging": true,
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

            // Handle other data if needed
        } catch (error) {
            console.error('Error fetching data:', error.message);
            // Handle errors, display error message to the user, etc.
        }
    }

    // Call the function to initially populate the table data
    const token = localStorage.getItem('token').match(/"([^"]*)"/)[1];
    populateTableData(token);

    // Add event listener to the form for form submission
    withdrawForm.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent the default form submission behavior

        try {
            const formData = new FormData(withdrawForm);
            const date = formData.get('date');
            // Refresh the table data after successful form submission
            populateTableData(token, date);
        } catch (error) {
            console.error('Error:', error.message);
            // Handle errors, display error message to the user, etc.
        }
    });
});

const style = document.createElement('style');
style.innerHTML = `
    .align-center {
        text-align:center;
    }
`;
document.head.appendChild(style);

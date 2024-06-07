// document.addEventListener('DOMContentLoaded', function () {
//     const withdrawForm = document.getElementById('searchDate');
//     const tableBody = document.getElementById('withdrawHistory');

//     // Function to fetch and populate the table data
//     async function populateTableData(token, date = null) {
//         try {
//             // Fetch data from API endpoint
//             let url = 'https://admin-soft.onrender.com/api/v1/transaction/admin-withdraw';
//             if (date) {
//                 url += `?date=${date}`;
//             }
//             const response = await fetch(url, {
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'Authorization': `Bearer ${token}` // Include the token in the Authorization header
//                 },
//             });

//             // Check if the response is successful
//             if (!response.ok) {
//                 throw new Error('Failed to fetch data');
//             }

//             // Parse the JSON response
//             const data = await response.json();
//             console.log(data);
//             // Clear existing content
//             tableBody.innerHTML = '';

//             if (data.data.length === 0) {
//                 // Display a message when no data is found
//                 const row = document.createElement('tr');
//                 const cell = document.createElement('td');
//                 cell.textContent = 'No data found for this date';
//                 cell.colSpan = 4; // Span across all columns
//                 row.appendChild(cell);
//                 tableBody.appendChild(row);
//             } else {
//                 // Populate the HTML table with data
//                 data.data.forEach(transaction => {
//                     const row = document.createElement('tr');

//                     const userIdCell = document.createElement('td');
//                     userIdCell.textContent = transaction._id;
//                     row.appendChild(userIdCell);

//                     const emailCell = document.createElement('td');
//                     emailCell.textContent = transaction.user.email;
//                     row.appendChild(emailCell);

//                     const phoneCell = document.createElement('td');
//                     phoneCell.textContent = transaction.user.phone;
//                     row.appendChild(phoneCell);

//                     const amountCell = document.createElement('td');
//                     amountCell.textContent = transaction.amount;
//                     row.appendChild(amountCell);

//                     tableBody.appendChild(row);
//                 });
//             }

//             // Handle other data if needed
//         } catch (error) {
//             console.error('Error fetching data:', error.message);
//             // Handle errors, display error message to the user, etc.
//         }
//     }

//     // Call the function to initially populate the table data
//     const token = localStorage.getItem('jwt').match(/"([^"]*)"/)[1];
//     populateTableData(token);

//     // Add event listener to the form for form submission
//     withdrawForm.addEventListener('submit', async function (event) {
//         event.preventDefault(); // Prevent the default form submission behavior

//         try {
//             const formData = new FormData(withdrawForm);
//             const date = formData.get('date');

//             // Refresh the table data after successful form submission
//             populateTableData(token, date);
//         } catch (error) {
//             console.error('Error:', error.message);
//             // Handle errors, display error message to the user, etc.
//         }
//     });
// });

document.addEventListener('DOMContentLoaded', function () {
    const withdrawForm = document.getElementById('searchDate');
    const tableBody = document.getElementById('withdrawHistory');

    // Function to fetch and populate the table data
    async function populateTableData(token, date = null) {
        try {
            // Fetch data from API endpoint
            let url = 'https://admin-soft.onrender.com/api/v1/transaction/admin-withdraw';
            if (date) {
                url += `?date=${date}`;
            }
            const response = await fetch(url, {
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
            // Clear existing content
            tableBody.innerHTML = '';

            if (data.data.length === 0) {
                // Display a message when no data is found
                const row = document.createElement('tr');
                const cell = document.createElement('td');
                cell.textContent = 'No data found for this date';
                cell.colSpan = 4; // Span across all columns
                row.appendChild(cell);
                tableBody.appendChild(row);
            } else {
                const arrayOfArrays = data.data.map(obj => Object.values(obj));
                // Populate the HTML table with data
                // data.data.forEach(transaction => {
                //     const row = document.createElement('tr');

                //     const userIdCell = document.createElement('td');
                //     userIdCell.textContent = transaction._id;
                //     row.appendChild(userIdCell);

                //     const emailCell = document.createElement('td');
                //     emailCell.textContent = transaction.user.email;
                //     row.appendChild(emailCell);

                //     const phoneCell = document.createElement('td');
                //     phoneCell.textContent = transaction.user.phone;
                //     row.appendChild(phoneCell);

                //     const amountCell = document.createElement('td');
                //     amountCell.textContent = transaction.amount;
                //     row.appendChild(amountCell);

                //     tableBody.appendChild(row);
                // });

                // Initialize DataTables with pagination
                $(tableBody).DataTable({
                    data: arrayOfArrays, // Use the data from the API response
                    columns: [
                        { 
                            title: "WithDraw Id",
                            render: function (data, type, row) {
                                return ` ${row[0]}`; 
                            }
                        },
                        { 
                            title: "Email-Id",
                            render: function (data, type, row) {
                                return ` ${row[2].email}`; 
                            }
                        },
                        { 
                            title: "Phone No.",
                            render: function (data, type, row) {
                                return ` ${row[2].phone}`; 
                            }
                        },
                        { 
                            title: "Amount" ,
                            render: function (data, type, row) {
                                return ` ${row[1]}`; 
                            }
                        },
                    ],
                    "pageLength": 10,
                    "paging": true
                    
                });
            }

            // Handle other data if needed
        } catch (error) {
            console.error('Error fetching data:', error.message);
            // Handle errors, display error message to the user, etc.
        }
    }

    // Call the function to initially populate the table data
    const token = localStorage.getItem('jwt').match(/"([^"]*)"/)[1];
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

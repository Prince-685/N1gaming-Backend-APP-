
document.addEventListener('DOMContentLoaded', async function () {
    const token = localStorage.getItem('token')?.match(/"([^"]*)"/)?.[1];
    if (!token) {
        console.error('Token not found');
        return;
    }

    const fetchData = async (url) => {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                }
            });
            if (!response.ok) throw new Error('Failed to fetch data');
            return await response.json();
        } catch (error) {
            console.error('Error fetching data:', error.message);
            throw error;
        }
    };

    try {
        const userList = await fetchData('https://n1gaming-backend-app.onrender.com/userlist');
        const tableBody = $('#userlist').DataTable({
            
            data: userList.map(Object.values),
            columns: [
                { title: "User" },
                { title: "Today's Bet" },
                { title: "Today's Winning" },
                { title: "Overall Bet" },
                { title: "Overall Winning" },
                {
                    title: "Joined At",
                    render: (data, type, row) => {
                        const kolkataTime = new Date(row[5]).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
                        const [datePart, timePart] = kolkataTime.split(',');
                        return `Date: ${datePart} <br> Time: ${timePart}`;
                    }
                }
            ],
            pageLength: 10,
            paging: true,
            createdRow: function(row, data, dataIndex) {
                // Example: Apply a class to the row based on a condition
                // Assuming data[4] is "Overall Winning"
                $(row).addClass('align-center'); // Add a custom class
                
            },

            headerCallback: function(thead, data, start, end, display) {
                // Apply a custom class to each header cell
                $(thead).find('th').addClass('align-center');
            }
        });
    } catch (error) {}

    try {
        const dashboardData = await fetchData('https://n1gaming-backend-app.onrender.com/admindashboard_data');
        document.getElementById('today_bets').textContent = dashboardData['today_bets'];
        document.getElementById('today_bets_won').textContent = dashboardData['today_bets_won'];
        document.getElementById('today_bet_loss').textContent = dashboardData['today_bet_loss'];
        document.getElementById('today_profit').textContent = dashboardData['today_profit'];
        document.getElementById('overall_bets').textContent = dashboardData['overall_bets'];
        document.getElementById('overall_bets_won').textContent = dashboardData['overall_bets_won'];
        document.getElementById('overall_bet_loss').textContent = dashboardData['overall_bet_loss'];
        document.getElementById('overall_profit').textContent = dashboardData['overall_profit'];
    } catch (error) {}
});


const style = document.createElement('style');
style.innerHTML = `
    .align-center {
        text-align:center;
    }
`;
document.head.appendChild(style);
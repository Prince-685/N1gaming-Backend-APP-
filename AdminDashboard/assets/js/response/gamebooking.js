document.addEventListener('DOMContentLoaded', async function () {
    const gameBookingSwitch = document.getElementById('gameBookingSwitch');
    const token = localStorage.getItem('jwt').match(/"([^"]*)"/)[1];

    // Function to call API to enable or disable game booking
    async function updateGameBookingStatus(isEnabled) {
        try {
            // Perform API call to update game booking status
            const response = await fetch('https://admin-soft.onrender.com/api/v1/game/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ game: isEnabled })
            });

            if (!response.ok) {
                throw new Error('Failed to update game booking status');
            }

        } catch (error) {
            console.error('Error updating game booking status:', error);
        }
    }

    // Function to fetch and set the initial game booking status
    async function fetchAndSetGameBookingStatus() {
        try {
            // Perform API call to fetch game booking status
            const response = await fetch('https://admin-soft.onrender.com/api/v1/game/get', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch game booking status');
            }

            const data = await response.json();
            const isEnabled = data.game;
            // Set the switch value based on the fetched status
            gameBookingSwitch.checked = isEnabled;
        } catch (error) {
            console.error('Error fetching game booking status:', error);
        }
    }

    // Call the function to fetch and set the initial game booking status
    fetchAndSetGameBookingStatus();

    // Add event listener to handle switch toggle
    gameBookingSwitch.addEventListener('change', function () {
        const isChecked = gameBookingSwitch.checked;
        updateGameBookingStatus(isChecked);
    });
});

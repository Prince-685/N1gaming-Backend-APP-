
        function previewImage(event) {
            const reader = new FileReader();
            reader.onload = function() {
                const output = document.getElementById('imagePreview');
                output.src = reader.result;
                output.style.display = 'block';
            };
            reader.readAsDataURL(event.target.files[0]);
        }

        document.getElementById('uploadForm').addEventListener('submit', function(event) {
            event.preventDefault();

            const fileInput = document.getElementById('imageUpload');
            const upiId = document.getElementById('upiId').value;
            const token = localStorage.getItem('token');

            if (fileInput.files.length === 0) {
                alert('Please select an image to upload.');
                return;
            }

            const formData = new FormData();
            formData.append('image', fileInput.files[0]);
            formData.append('upi_id', upiId);

            fetch('https://n1gaming-backend-app.onrender.com/upload_payment_qr/', {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                alert('Image submitted successfully!');
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('There was an error submitting the image.');
            });
        });






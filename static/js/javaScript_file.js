document.getElementById('SignUpForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent form submission from refreshing the page

    const username = document.getElementById('username').value;
    const passwordfirstName = document.getElementById('passwordfirstName').value;
    const lastName = document.getElementById('lastName').value;
    const motherName = document.getElementById('motherName').value;
    const phoneNumber = document.getElementById('phoneNumber').value;
    const email = document.getElementById('email').value;
    const nationalId = document.getElementById('nationalId').value;
    const familyName = document.getElementById('familyName').value;
    const password = document.getElementById('password').value;
    const re_password = document.getElementById('re_password').value;
    try {
        const response = await fetch('/endpoint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, passwordfirstName, lastName, motherName, phoneNumber, email, nationalId, familyName, password, re_password  }),
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('responseMessage').textContent = 'Sign up successful!';
            console.log('Token:', data.token); // Handle token or user data
        } else {
            const error = await response.json();
            document.getElementById('responseMessage').textContent = `Error: ${error.message}`;
        }
    } catch (err) {
        console.error('Fetch error:', err);
        document.getElementById('responseMessage').textContent = 'Network error occurred.';
    }
});

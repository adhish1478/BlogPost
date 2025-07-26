document.getElementById('form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/api/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username,
            password,
        })
    });

    const data = await response.json();

    if (response.ok) {
        // save token here if returned
        localStorage.setItem('access', data.access);
        localStorage.setItem('refresh', data.refresh);

        // Redirect to home
        //alert('Login successful! Redirecting to home...');
        window.location.href = '/';
    } else {
        alert(data.detail || 'Login failed');
    }
});
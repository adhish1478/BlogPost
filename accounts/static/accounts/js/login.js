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

        // Fetch and store user info
        await fetchUserInfo();

        // Redirect to home
        //alert('Login successful! Redirecting to home...');
        window.location.href = '/';
    } else {
        alert(data.detail || 'Login failed');
    }
});

async function fetchUserInfo() {
    const host = "http://localhost:8000/api";
    const res= await fetch(`${host}/me`, {
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("access")}`
        }
    });
    if (res.ok) {
        const user = await res.json();
        localStorage.setItem("user_id", user.id);
        localStorage.setItem("username", user.username);
    } else {
        alert("Failed to fetch user data.");
    }
};
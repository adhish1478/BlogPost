// Profile Dropdown functionality
document.addEventListener("DOMContentLoaded", () => {
    updateAccountSection();
});

function updateAccountSection() {
    const accountArea = document.getElementById("accountArea");
    const username = localStorage.getItem("username");

    if (username) {
        accountArea.innerHTML = `
            <div class="dropdown">
                <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                    Hi, ${username}
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="#" id="logoutBtn">Logout</a></li>
                </ul>
            </div>
        `;

        document.getElementById("logoutBtn").addEventListener("click", logoutUser);
    } else {
        accountArea.innerHTML = `
            <a href="/login/" class="btn btn-outline-secondary">👤 Login</a>
        `;
    }
}

// Logout functionality
async function logoutUser() {
    const refresh = localStorage.getItem("refresh");

    try {
        await fetch("/api/token/logout/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ refresh })
        });
    } catch (error) {
        console.error("Failed to blacklist refresh token", error);
    }

    // Clear everything
    localStorage.clear();
    window.location.href = "/";
}
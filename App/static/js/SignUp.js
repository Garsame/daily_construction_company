const form = document.getElementById('registrationForm');
const errorDiv = document.getElementById('error');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const role = document.getElementById('role').value;

    if (!["admin", "site_engineer"].includes(role)) {
        errorDiv.textContent = "Invalid role selected.";
        return;
    }

    errorDiv.textContent = ""; // Clear previous error message

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password, role }),
        });

        const data = await response.json();

        if (data.success) {
            alert(data.message);
            form.reset();
        } else {
            errorDiv.textContent = data.message || "Registration failed.";
        }
    } catch (error) {
        errorDiv.textContent = "An error occurred. Please try again.";
    }
});

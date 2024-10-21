// API endpoints
const API_URL = 'http://127.0.0.1:8080';  // Change this if necessary

// Logout function using FastAPI backend
async function logout() {
    const token = localStorage.getItem('access_token');

    try {
        const response = await fetch(`${API_URL}/logout`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            window.location.href = 'index.html';  // Redirect to login page after logout
        } else {
            alert('Error logging out');
        }
    } catch (error) {
        console.error('Logout error:', error);
        alert('An error occurred during logout');
    }
}

async function getUser() {
    const token = localStorage.getItem('access_token');

    try {
        const response = await fetch(`${API_URL}/getuser`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const user_name = document.getElementById('user_name');
            const user_email = document.getElementById('user_email');
            let userData = await response.json();
            user_name.innerHTML = "username: " + userData.username;
            user_email.innerHTML = "email: " + userData.email;
            console.log(userData);
        } else {
            window.location.href = 'index.html';  // Redirect to login page after logout
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during getting users');
    }

}
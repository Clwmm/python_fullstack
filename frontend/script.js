// API endpoints
const API_URL = 'http://127.0.0.1:8080';  // Change this if necessary

// Toggle between login and register forms
function toggleForms() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm.style.display === 'none') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    }
}

// Login function using FastAPI backend
async function login() {
    const email = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);  // Save the token
            alert('Login successful!');
            window.location.href = 'home.html';  // Redirect to the home page after login
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during login');
    }
}

async function users() {
    const token = localStorage.getItem('access_token');

    try {
        const response = await fetch(`${API_URL}/getusers`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            response = response.json()
            console.log(response)
        } else {
            console.log("Error: getUsers")
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during getting users');
    }

}

// Register function using FastAPI backend
async function register() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            alert('Registration successful! You can now log in.');
            toggleForms();  // Switch to login form
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('An error occurred during registration');
    }
}

// Check if user is logged in (used on the home page)
async function checkSession() {
    try {
        const response = await fetch(`${API_URL}/session`, {
            method: 'GET',
            credentials: 'include'  // Send the session cookie with request
        });

        if (!response.ok) {
            window.location.href = 'index.html';  // If not logged in, redirect to login
        }
    } catch (error) {
        console.error('Session check error:', error);
        window.location.href = 'index.html';  // If error occurs, redirect to login
    }
}

// Logout function using FastAPI backend
async function logout() {
    try {
        const response = await fetch(`${API_URL}/logout`, {
            method: 'POST',
            credentials: 'include'  // Send the session cookie with request
        });

        if (response.ok) {
            alert('Logged out successfully');
            window.location.href = 'index.html';  // Redirect to login page after logout
        } else {
            alert('Error logging out');
        }
    } catch (error) {
        console.error('Logout error:', error);
        alert('An error occurred during logout');
    }
}

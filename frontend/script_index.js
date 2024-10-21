// API endpoints
const API_URL = 'http://127.0.0.1:8080';  // Change this if necessary

// Toggle between login and register forms
function toggleForms() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm.style.display === 'none') {
        loginForm.style.display = '';
        registerForm.style.display = 'none';
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = '';
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

// Register function using FastAPI backend
async function register() {
    const email = document.getElementById('register-email').value;
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, username, password })
        });

        if (response.ok) {
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
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch(`${API_URL}/session`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            window.location.href = 'home.html';  // If not logged in, redirect to login
        }
    } catch (error) {
        console.error('Session check error:', error);
        window.location.href = 'index.html';  // If error occurs, redirect to login
    }
}

// Handle Login Form
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Create FormData for OAuth2
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Save token to localStorage
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('username', username);
                
                // Redirect to notes page
                window.location.href = '/';
            } else {
                alert(data.detail || 'Login failed! Please check your credentials.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Login failed! Please try again.');
        }
    });
}

// Handle Register Form
if (document.getElementById('registerForm')) {
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        // Validate passwords match
        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }
        
        // Validate password length
        if (password.length < 6) {
            alert('Password must be at least 6 characters long!');
            return;
        }
        
        const userData = {
            username: username,
            email: email,
            password: password
        };
        
        try {
            const response = await fetch('/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });
            
            if (response.ok) {
                const data = await response.json();
                alert('Registration successful! Please login.');
                window.location.href = '/login';
            } else {
                const error = await response.json();
                alert(error.detail || 'Registration failed! Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Registration failed! Server error. Please try again.');
        }
    });
}
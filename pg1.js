// ==== SIGN IN, SIGN OUT, RESET ====

function toggleSignInForm() {
    const modal = document.getElementById('sign-in-modal');
    modal.style.display = (modal.style.display === 'block') ? 'none' : 'block';
}

function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password-input');
    const toggleIcon = document.getElementById('toggle-password');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

function signIn() {
    const email = document.getElementById('email-input').value;
    const password = document.getElementById('password-input').value;
    if (!email || !password) {
        alert('Please enter both email and password.');
        return;
    }
    const storedPassword = localStorage.getItem(email);
    if (storedPassword) {
        if (storedPassword === password) {
            alert('Sign In Successful!');
            localStorage.setItem('userEmail', email);
            window.location.href = 'page2.html';
        } else {
            alert('Incorrect Password!');
        }
    } else {
        localStorage.setItem(email, password);
        localStorage.setItem('userEmail', email);
        alert('Account Created and Signed In!');
        window.location.href = 'page2.html';
    }
}

function resetPassword() {
    const email = document.getElementById('email-input').value;
    if (!email) {
        alert('Please enter your email to reset the password.');
        return;
    }
    if (localStorage.getItem(email)) {
        localStorage.removeItem(email);
        alert('Password reset. Please create a new password upon signing in.');
    } else {
        alert('Email not found!');
    }
}

function logout() {
    localStorage.removeItem('userEmail');
    alert('Logged Out');
    window.location.reload();
}

window.onload = function () {
    const email = localStorage.getItem('userEmail');
    if (email) {
        document.getElementById('sign-in-text').textContent = email;
        document.getElementById('logout-btn').style.display = 'block';
    }
};

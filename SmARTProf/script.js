function login() {
    // validation of login
    // if successful go to select-language page
    window.location.href = "select-language.html";
}

function goToRegister() {
    window.location.href = "register.html";
}

function register() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // registration logic here
    window.location.href = "select-language.html";
}

function selectLanguage(language) {
    alert(`You selected ${language}!`);
    // Add logic to proceed with the selected language
}
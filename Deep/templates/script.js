const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
const signUpForm = document.querySelector('.sign-up form');
const signInForm = document.querySelector('.sign-in form');
const signUpEmailInput = document.querySelector('.sign-up input[type="email"]');
const signUpPasswordInput = document.querySelector('.sign-up input[type="password"]');
const signInEmailInput = document.querySelector('.sign-in input[type="email"]');
const signInPasswordInput = document.querySelector('.sign-in input[type="password"]');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

signUpForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const signUpEmail = signUpEmailInput.value.trim();
    const signUpPassword = signUpPasswordInput.value.trim();

    // Check if email and password match certain criteria (e.g., not empty)
    if (signUpEmail === "" || signUpPassword === "") {
        alert("Please enter both email and password.");
        return;
    }

    // Here you can add your logic to store the sign-up data or perform further validation

    // Clear the input fields after successful registration
    signUpEmailInput.value = "";
    signUpPasswordInput.value = "";

    // Optionally, you can show a success message
    alert("Registration successful!");
});

signInForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const signInEmail = signInEmailInput.value.trim();
    const signInPassword = signInPasswordInput.value.trim();

    // Here you can add your logic to check the email and password against your database or any other source

    // For demonstration, let's assume a hardcoded email and password
    const validEmail = "example@gmail.com";
    const validPassword = "password";

    // Check if the entered email and password match the hardcoded values
    if (signInEmail !== validEmail || signInPassword !== validPassword) {
        alert("Invalid email or password.");
        return;
    }

    // Clear the input fields after successful sign-in
    signInEmailInput.value = "";
    signInPasswordInput.value = "";
    
    window.location.href = "http://127.0.0.1:3000";

});
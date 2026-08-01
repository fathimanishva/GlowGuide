function setupPasswordToggle(inputId, toggleId) {
    const password = document.getElementById(inputId);
    const toggle = document.getElementById(toggleId);

    if (password && toggle) {
        toggle.addEventListener("click", function () {

            if (password.type === "password") {
                password.type = "text";
                this.innerHTML = '<i class="bi bi-eye-slash"></i>';
            } else {
                password.type = "password";
                this.innerHTML = '<i class="bi bi-eye"></i>';
            }

        });
    }
}

setupPasswordToggle("password", "togglePassword");
setupPasswordToggle("confirmPassword", "toggleConfirmPassword");
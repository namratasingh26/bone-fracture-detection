document.addEventListener('DOMContentLoaded', () => {

    // SIGNUP
    const signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const username = document.getElementById("new-username").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("new-password").value;
            const confirmPassword = document.getElementById("confirm-password").value;
            const message = document.getElementById("signup-message");

            if (password !== confirmPassword) {
                message.innerText = " Passwords do not match!";
                return;
            }

            try {
                message.innerText = "Creating account...";
                const response = await fetch("http://127.0.0.1:5001/signup", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, email, password })
                });

                const data = await response.json();
                message.innerText = data.message || data.error;

                if (response.ok) {
                    setTimeout(() => {
                        window.location.href = "login.html";
                    }, 2000);
                }
            } catch (error) {
                message.innerText = "Signup failed!";
            }
        });
    }

    // LOGIN
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            const message = document.getElementById("login-message");

            try {
                message.innerText = "Logging in...";
                const response = await fetch("http://127.0.0.1:5001/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();
                message.innerText = data.message || data.error;

                if (response.ok) {
                    setTimeout(() => {
                        window.location.href = "detect.html";
                    }, 2000);
                }
            } catch (error) {
                message.innerText = "Login failed!";
            }
        });
    }
});

// PREDICTION FUNCTION (global)
// Predict
async function detectFracture() {
    const fileInput = document.getElementById("fileInput");
    const resultText = document.getElementById("result");
    const previewImage = document.getElementById("preview");

    if (!fileInput.files.length) {
        resultText.innerText = "Please upload an image!";
        return;
    }

    const file = fileInput.files[0];

    // Show uploaded image preview
    const reader = new FileReader();
    reader.onload = function (e) {
        previewImage.src = e.target.result;
        previewImage.style.display = 'block';
    };
    reader.readAsDataURL(file);

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://127.0.0.1:5001/predict", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        if (response.ok) {
            resultText.innerText = ` Result: ${data.prediction}\n Recommendation: ${data.recommendation}`;
        } else {
            resultText.innerText = ` Error: ${data.error}`;
        }
    } catch (error) {
        resultText.innerText = " Prediction failed!";
    }
}

const API_URL = "http://127.0.0.1:8000";


// -----------------------------
// Register Function
// -----------------------------

async function register() {

    const username =
        document.getElementById("username").value;

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    if (
        username === "" ||
        email === "" ||
        password === ""
    ) {

        alert("All fields are required");
        return;
    }

    const response = await fetch(
        `${API_URL}/register`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username,
                email,
                password
            })
        }
    );

    const data = await response.json();

    alert(data.message);

    if (
        data.message ===
        "Registration Successful"
    ) {

        window.location.href =
            "/login-page";
    }
}


// -----------------------------
// Login Function
// -----------------------------

async function login() {

    const email =
        document.getElementById("loginEmail").value;

    const password =
        document.getElementById("loginPassword").value;

    if (
        email === "" ||
        password === ""
    ) {

        alert("All fields required");
        return;
    }

    const response = await fetch(
        `${API_URL}/login`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email,
                password
            })
        }
    );

    const data = await response.json();

    if (
        data.message ===
        "Login Successful"
    ) {

        alert("Login Successful");

        window.location.href =
            "/skills-page";
    }

    else {

        alert(
            "Invalid Email or Password"
        );
    }
}


// -----------------------------
// Skill Analysis Function
// -----------------------------

async function analyzeSkills() {

    const skills =
        document.getElementById("skills").value;

    const role =
        document.getElementById("role").value;

    const response = await fetch(
        `${API_URL}/analyze`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                skills,
                role
            })
        }
    );

    const data = await response.json();

    let output = `
        <b>Status:</b> ${data.status}
        <br><br>

        <b>Message:</b>
        ${data.message}
        <br><br>
    `;

    if (
        data.missing_skills &&
        data.missing_skills.length > 0
    ) {

        output += `
            <b>Missing Skills:</b>
            ${data.missing_skills.join(", ")}
        `;
    }

    document.getElementById("result")
        .innerHTML = output;
}

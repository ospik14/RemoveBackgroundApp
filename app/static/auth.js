const authForm = document.getElementById("authForm");

authForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const email = document.getElementById("emailInput").value;
  const username = document.getElementById("usernameInput").value;
  const password = document.getElementById("passwordInput").value;

  const data = {
    email: email,
    username: username,
    password: password,
    role: "user",
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      document.getElementById("errorMsg").innerText = errorData.detail;
      if (response.status === 409) {
        alert("Такий користувач вже існує");
      }
      return;
    }

    const result = await response.json();
    localStorage.setItem("accessToken", result.access_token);
    window.location.href = "/static/menu.html";
  } catch (error) {
    console.error("Помилка мережі: ", error);
  }
});

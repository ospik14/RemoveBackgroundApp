const loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const email = document.getElementById("emailInput").value;
  const password = document.getElementById("passwordInput").value;

  const formData = new FormData();

  formData.append("username", email);
  formData.append("password", password);

  try {
    const response = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }

    const result = await response.json();

    localStorage.setItem("accessToken", result.access_token);
    window.location.href = "/static/menu.html";
  } catch (error) {
    document.getElementById("errorMsg").innerText = error.message;
    document.getElementById("errorMsg").style.display = "block";
  }
});

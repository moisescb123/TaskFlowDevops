/**
 * Post-login redirects by role (US01 / task 3.3):
 * - admin -> /admin/users
 * - developer | viewer -> /board
 */
(function () {
  const ROLE_LANDING = {
    admin: "/admin/users",
    developer: "/board",
    viewer: "/board",
  };

  const form = document.getElementById("login-form");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const emailError = document.getElementById("email-error");
  const passwordError = document.getElementById("password-error");
  const formError = document.getElementById("form-error");

  function clearErrors() {
    emailError.hidden = true;
    passwordError.hidden = true;
    formError.hidden = true;
    emailError.textContent = "";
    passwordError.textContent = "";
    formError.textContent = "";
  }

  function showFieldErrors(fields) {
    if (fields.email) {
      emailError.hidden = false;
      emailError.textContent = fields.email;
    }
    if (fields.password) {
      passwordError.hidden = false;
      passwordError.textContent = fields.password;
    }
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearErrors();

    const payload = {
      email: emailInput.value,
      password: passwordInput.value,
    };

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify(payload),
      });
      const data = await response.json().catch(() => ({}));

      if (response.status === 400) {
        showFieldErrors(data.fields || {});
        if (!data.fields || Object.keys(data.fields).length === 0) {
          formError.hidden = false;
          formError.textContent = data.message || "Validation failed";
        }
        return;
      }

      if (response.status === 401) {
        formError.hidden = false;
        formError.textContent = data.message || "Invalid email or password";
        return;
      }

      if (!response.ok) {
        formError.hidden = false;
        formError.textContent = data.message || "Unable to sign in";
        return;
      }

      const landing = ROLE_LANDING[data.role] || "/board";
      window.location.assign(landing);
    } catch (error) {
      formError.hidden = false;
      formError.textContent = "Network error. Please try again.";
    }
  });
})();

/**
 * Admin user registration and list (US03).
 */
(function () {
  const form = document.getElementById("register-form");
  const tbody = document.getElementById("users-tbody");
  const formError = document.getElementById("form-error");
  const formSuccess = document.getElementById("form-success");

  const fieldIds = ["email", "password", "full_name", "role"];

  function clearFeedback() {
    formError.hidden = true;
    formSuccess.hidden = true;
    formError.textContent = "";
    formSuccess.textContent = "";
    fieldIds.forEach((id) => {
      const el = document.getElementById(`${id}-error`);
      if (el) {
        el.hidden = true;
        el.textContent = "";
      }
    });
  }

  function showFieldErrors(fields) {
    Object.keys(fields || {}).forEach((key) => {
      const el = document.getElementById(`${key}-error`);
      if (el) {
        el.hidden = false;
        el.textContent = fields[key];
      }
    });
  }

  async function loadUsers() {
    tbody.innerHTML = '<tr><td colspan="4" class="muted">Loading…</td></tr>';
    try {
      const response = await fetch("/api/users", {
        credentials: "same-origin",
      });
      if (response.status === 401) {
        window.location.assign("/login");
        return;
      }
      if (response.status === 403) {
        window.location.assign("/board");
        return;
      }
      if (!response.ok) {
        tbody.innerHTML =
          '<tr><td colspan="4" class="form-error">Unable to load users.</td></tr>';
        return;
      }
      const users = await response.json();
      if (!Array.isArray(users) || users.length === 0) {
        tbody.innerHTML =
          '<tr><td colspan="4" class="muted">No users yet.</td></tr>';
        return;
      }
      tbody.innerHTML = users
        .map(
          (user) =>
            `<tr>
              <td>${user.id}</td>
              <td>${escapeHtml(user.email)}</td>
              <td>${escapeHtml(user.full_name)}</td>
              <td>${escapeHtml(user.role)}</td>
            </tr>`
        )
        .join("");
    } catch (error) {
      tbody.innerHTML =
        '<tr><td colspan="4" class="form-error">Network error loading users.</td></tr>';
    }
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearFeedback();

    const payload = {
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
      full_name: document.getElementById("full_name").value,
      role: document.getElementById("role").value,
    };

    try {
      const response = await fetch("/api/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify(payload),
      });
      const data = await response.json().catch(() => ({}));

      if (response.status === 401) {
        window.location.assign("/login");
        return;
      }
      if (response.status === 403) {
        window.location.assign("/board");
        return;
      }
      if (response.status === 400) {
        showFieldErrors(data.fields || {});
        if (!data.fields || Object.keys(data.fields).length === 0) {
          formError.hidden = false;
          formError.textContent = data.message || "Validation failed";
        }
        return;
      }
      if (!response.ok) {
        formError.hidden = false;
        formError.textContent = data.message || "Unable to create user";
        return;
      }

      form.reset();
      document.getElementById("role").value = "developer";
      formSuccess.hidden = false;
      formSuccess.textContent = `Created ${data.full_name} (${data.role}).`;
      await loadUsers();
    } catch (error) {
      formError.hidden = false;
      formError.textContent = "Network error. Please try again.";
    }
  });

  loadUsers();
})();

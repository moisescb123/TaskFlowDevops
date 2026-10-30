/**
 * Shared logout control (US02): POST /api/auth/logout then redirect to /login.
 */
(function () {
  const button = document.getElementById("logout-button");
  if (!button) {
    return;
  }

  button.addEventListener("click", async () => {
    button.disabled = true;
    try {
      const response = await fetch("/api/auth/logout", {
        method: "POST",
        credentials: "same-origin",
      });
      if (response.status === 204 || response.status === 401) {
        window.location.assign("/login");
        return;
      }
      button.disabled = false;
      window.alert("Unable to log out. Please try again.");
    } catch (error) {
      button.disabled = false;
      window.alert("Network error while logging out. Please try again.");
    }
  });
})();

/**
 * Kanban board view (US04): load tasks and group by status.
 * Viewer: mutate controls stay hidden/disabled (data-can-mutate=false).
 */
(function () {
  const root = document.getElementById("board-root");
  if (!root) {
    return;
  }

  const canMutate = root.dataset.canMutate === "true";
  const emptyEl = document.getElementById("board-empty");
  const errorEl = document.getElementById("board-error");
  const createBtn = document.getElementById("create-task-button");

  const STATUS_ORDER = ["todo", "in_progress", "done"];

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function priorityClass(priority) {
    return `priority-${escapeHtml(priority || "medium")}`;
  }

  function renderCard(task) {
    const assignee =
      task.assignee_name ||
      (task.assignee_id != null ? `User #${task.assignee_id}` : "Unassigned");
    const mutateBlock = canMutate
      ? `<div class="card-actions muted">Edit / move (coming soon)</div>`
      : "";
    return `<article class="task-card" data-task-id="${task.id}">
      <h3 class="task-title">${escapeHtml(task.title)}</h3>
      <p class="task-meta"><span class="${priorityClass(task.priority)}">${escapeHtml(
        task.priority
      )}</span></p>
      <p class="task-meta">Due ${escapeHtml(task.due_date)}</p>
      <p class="task-meta">${escapeHtml(assignee)}</p>
      ${mutateBlock}
    </article>`;
  }

  function clearColumns() {
    STATUS_ORDER.forEach((status) => {
      const column = root.querySelector(`.board-column[data-status="${status}"]`);
      if (!column) {
        return;
      }
      column.querySelector("[data-cards]").innerHTML = "";
      column.querySelector("[data-count]").textContent = "0";
    });
  }

  function renderTasks(tasks) {
    clearColumns();
    const grouped = groupTasksByStatus(tasks);

    let total = 0;
    STATUS_ORDER.forEach((status) => {
      const column = root.querySelector(`.board-column[data-status="${status}"]`);
      const cards = grouped[status] || [];
      total += cards.length;
      column.querySelector("[data-count]").textContent = String(cards.length);
      column.querySelector("[data-cards]").innerHTML = cards.map(renderCard).join("");
    });

    emptyEl.hidden = total > 0;
  }

  async function loadBoard() {
    errorEl.hidden = true;
    errorEl.textContent = "";
    try {
      const response = await fetch("/api/tasks", { credentials: "same-origin" });
      if (response.status === 401) {
        window.location.assign("/login");
        return;
      }
      if (!response.ok) {
        errorEl.hidden = false;
        errorEl.textContent = "Unable to load tasks.";
        return;
      }
      const tasks = await response.json();
      renderTasks(Array.isArray(tasks) ? tasks : []);
    } catch (error) {
      errorEl.hidden = false;
      errorEl.textContent = "Network error loading the board.";
    }
  }

  if (createBtn && !canMutate) {
    createBtn.hidden = true;
  }

  loadBoard();
})();

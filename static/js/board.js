/**
 * Kanban board view (US04/US05): load tasks, group by status, create tasks.
 * Viewer: mutate controls stay hidden/disabled (data-can-mutate=false).
 */
(function () {
  const root = document.getElementById("board-root");
  if (!root) {
    return;
  }

  const canMutate = root.dataset.canMutate === "true";
  const canCreate = root.dataset.canCreate === "true";
  const emptyEl = document.getElementById("board-empty");
  const errorEl = document.getElementById("board-error");
  const createBtn = document.getElementById("create-task-button");
  const dialog = document.getElementById("create-task-dialog");
  const form = document.getElementById("create-task-form");
  const cancelBtn = document.getElementById("create-task-cancel");
  const formError = document.getElementById("create-task-form-error");
  const submitBtn = document.getElementById("create-task-submit");

  const STATUS_ORDER = ["todo", "in_progress", "done"];
  const FIELD_IDS = ["title", "priority", "due_date", "assignee_id"];
  let createInFlight = false;

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

  function clearFieldErrors() {
    FIELD_IDS.forEach((name) => {
      const el = document.getElementById(`task-${name.replace("_", "-")}-error`);
      if (el) {
        el.hidden = true;
        el.textContent = "";
      }
    });
    if (formError) {
      formError.hidden = true;
      formError.textContent = "";
    }
  }

  function showFieldErrors(fields) {
    Object.entries(fields || {}).forEach(([name, message]) => {
      const el = document.getElementById(`task-${name.replace("_", "-")}-error`);
      if (el) {
        el.hidden = false;
        el.textContent = message;
      }
    });
  }

  function openCreateDialog() {
    if (!dialog || !form) {
      return;
    }
    clearFieldErrors();
    form.reset();
    dialog.showModal();
  }

  function closeCreateDialog() {
    if (dialog) {
      dialog.close();
    }
  }

  async function submitCreate(event) {
    event.preventDefault();
    if (!form || createInFlight) {
      return;
    }
    clearFieldErrors();
    const title = form.title.value.trim();
    const priority = form.priority.value;
    const dueDate = form.due_date.value;
    const assigneeRaw = form.assignee_id.value.trim();
    const body = { title, priority, due_date: dueDate };
    if (assigneeRaw) {
      body.assignee_id = Number(assigneeRaw);
    }

    createInFlight = true;
    if (submitBtn) {
      submitBtn.disabled = true;
    }
    try {
      const response = await fetch("/api/tasks", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (response.status === 401) {
        window.location.assign("/login");
        return;
      }
      const payload = await response.json().catch(() => ({}));
      if (response.status === 400) {
        showFieldErrors(payload.fields || {});
        if (formError) {
          formError.hidden = false;
          formError.textContent = payload.message || "Validation failed";
        }
        return;
      }
      if (!response.ok) {
        if (formError) {
          formError.hidden = false;
          formError.textContent = payload.message || "Unable to create task.";
        }
        return;
      }
      closeCreateDialog();
      await loadBoard();
    } catch (error) {
      if (formError) {
        formError.hidden = false;
        formError.textContent = "Network error creating the task.";
      }
    } finally {
      createInFlight = false;
      if (submitBtn) {
        submitBtn.disabled = false;
      }
    }
  }

  if (createBtn && !canCreate) {
    createBtn.hidden = true;
  }
  if (canCreate && createBtn && dialog && form) {
    createBtn.addEventListener("click", openCreateDialog);
    if (cancelBtn) {
      cancelBtn.addEventListener("click", closeCreateDialog);
    }
    form.addEventListener("submit", submitCreate);
  }

  loadBoard();
})();

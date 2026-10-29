/**
 * Kanban board (US04–US06): list/group tasks, create and edit (Developer).
 */
(function () {
  const root = document.getElementById("board-root");
  if (!root) {
    return;
  }

  const canCreate = root.dataset.canCreate === "true";
  const emptyEl = document.getElementById("board-empty");
  const errorEl = document.getElementById("board-error");
  const createBtn = document.getElementById("create-task-button");
  const dialog = document.getElementById("create-task-dialog");
  const form = document.getElementById("create-task-form");
  const cancelBtn = document.getElementById("create-task-cancel");
  const formError = document.getElementById("create-task-form-error");
  const submitBtn = document.getElementById("create-task-submit");

  const editDialog = document.getElementById("edit-task-dialog");
  const editForm = document.getElementById("edit-task-form");
  const editCancelBtn = document.getElementById("edit-task-cancel");
  const editFormError = document.getElementById("edit-task-form-error");
  const editSubmitBtn = document.getElementById("edit-task-submit");
  const editTaskIdInput = document.getElementById("edit-task-id");

  const STATUS_ORDER = ["todo", "in_progress", "done"];
  const FIELD_IDS = ["title", "priority", "due_date", "assignee_id"];
  let createInFlight = false;
  let editInFlight = false;
  let tasksById = {};

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
    const mutateBlock = canCreate
      ? `<div class="card-actions"><button type="button" class="edit-task-button" data-edit-id="${task.id}">Edit</button></div>`
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
    tasksById = {};
    (tasks || []).forEach((task) => {
      tasksById[task.id] = task;
    });
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

  function clearCreateErrors() {
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

  function showCreateErrors(fields) {
    Object.entries(fields || {}).forEach(([name, message]) => {
      const el = document.getElementById(`task-${name.replace("_", "-")}-error`);
      if (el) {
        el.hidden = false;
        el.textContent = message;
      }
    });
  }

  function clearEditErrors() {
    FIELD_IDS.forEach((name) => {
      const el = document.getElementById(`edit-task-${name.replace("_", "-")}-error`);
      if (el) {
        el.hidden = true;
        el.textContent = "";
      }
    });
    if (editFormError) {
      editFormError.hidden = true;
      editFormError.textContent = "";
    }
  }

  function showEditErrors(fields) {
    Object.entries(fields || {}).forEach(([name, message]) => {
      const el = document.getElementById(`edit-task-${name.replace("_", "-")}-error`);
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
    clearCreateErrors();
    form.reset();
    dialog.showModal();
  }

  function closeCreateDialog() {
    if (dialog) {
      dialog.close();
    }
  }

  function openEditDialog(taskId) {
    if (!editDialog || !editForm) {
      return;
    }
    const task = tasksById[taskId];
    if (!task) {
      return;
    }
    clearEditErrors();
    editTaskIdInput.value = String(task.id);
    editForm.title.value = task.title || "";
    editForm.priority.value = task.priority || "medium";
    editForm.due_date.value = task.due_date || "";
    editForm.assignee_id.value =
      task.assignee_id != null ? String(task.assignee_id) : "";
    editDialog.showModal();
  }

  function closeEditDialog() {
    if (editDialog) {
      editDialog.close();
    }
  }

  async function submitCreate(event) {
    event.preventDefault();
    if (!form || createInFlight) {
      return;
    }
    clearCreateErrors();
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
        showCreateErrors(payload.fields || {});
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

  async function submitEdit(event) {
    event.preventDefault();
    if (!editForm || editInFlight) {
      return;
    }
    clearEditErrors();
    const taskId = editTaskIdInput.value;
    const title = editForm.title.value.trim();
    const priority = editForm.priority.value;
    const dueDate = editForm.due_date.value;
    const assigneeRaw = editForm.assignee_id.value.trim();
    const body = {
      title,
      priority,
      due_date: dueDate,
      assignee_id: assigneeRaw ? Number(assigneeRaw) : null,
    };

    editInFlight = true;
    if (editSubmitBtn) {
      editSubmitBtn.disabled = true;
    }
    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: "PUT",
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
        showEditErrors(payload.fields || {});
        if (editFormError) {
          editFormError.hidden = false;
          editFormError.textContent = payload.message || "Validation failed";
        }
        return;
      }
      if (!response.ok) {
        if (editFormError) {
          editFormError.hidden = false;
          editFormError.textContent = payload.message || "Unable to update task.";
        }
        return;
      }
      closeEditDialog();
      await loadBoard();
    } catch (error) {
      if (editFormError) {
        editFormError.hidden = false;
        editFormError.textContent = "Network error updating the task.";
      }
    } finally {
      editInFlight = false;
      if (editSubmitBtn) {
        editSubmitBtn.disabled = false;
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
  if (canCreate && editDialog && editForm) {
    root.addEventListener("click", (event) => {
      const button = event.target.closest("[data-edit-id]");
      if (!button) {
        return;
      }
      openEditDialog(button.getAttribute("data-edit-id"));
    });
    if (editCancelBtn) {
      editCancelBtn.addEventListener("click", closeEditDialog);
    }
    editForm.addEventListener("submit", submitEdit);
  }

  loadBoard();
})();

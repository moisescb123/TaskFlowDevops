/**
 * Kanban board (US04–US11): CRUD, assignee, status, priority badge, due date.
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

  const deleteDialog = document.getElementById("delete-task-dialog");
  const deleteForm = document.getElementById("delete-task-form");
  const deleteCancelBtn = document.getElementById("delete-task-cancel");
  const deleteFormError = document.getElementById("delete-task-form-error");
  const deleteConfirmBtn = document.getElementById("delete-task-confirm");
  const deleteTaskIdInput = document.getElementById("delete-task-id");
  const deleteMessage = document.getElementById("delete-task-message");

  const STATUS_ORDER = ["todo", "in_progress", "done"];
  const FIELD_IDS = ["title", "priority", "due_date", "assignee_id"];
  let createInFlight = false;
  let editInFlight = false;
  let deleteInFlight = false;
  let statusInFlight = false;
  let tasksById = {};
  let assigneeOptionsLoaded = false;

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

  function priorityLabel(priority) {
    const value = priority || "medium";
    return value.charAt(0).toUpperCase() + value.slice(1);
  }

  function statusMoveButtons(task) {
    if (!canCreate) {
      return "";
    }
    const moves = [];
    if (task.status === "todo") {
      moves.push(
        `<button type="button" class="status-task-button" data-status-id="${task.id}" data-status-to="in_progress">Start</button>`
      );
    } else if (task.status === "in_progress") {
      moves.push(
        `<button type="button" class="status-task-button" data-status-id="${task.id}" data-status-to="todo">Back to To Do</button>`
      );
      moves.push(
        `<button type="button" class="status-task-button" data-status-id="${task.id}" data-status-to="done">Complete</button>`
      );
    } else if (task.status === "done") {
      moves.push(
        `<button type="button" class="status-task-button" data-status-id="${task.id}" data-status-to="in_progress">Reopen</button>`
      );
    }
    return moves.join("");
  }

  function renderCard(task) {
    const assignee =
      task.assignee_name ||
      (task.assignee_id != null ? `User #${task.assignee_id}` : "Unassigned");
    const priority = task.priority || "medium";
    const mutateBlock = canCreate
      ? `<div class="card-actions">
          ${statusMoveButtons(task)}
          <button type="button" class="edit-task-button" data-edit-id="${task.id}">Edit</button>
          <button type="button" class="delete-task-button" data-delete-id="${task.id}">Delete</button>
        </div>`
      : "";
    return `<article class="task-card" data-task-id="${task.id}">
      <h3 class="task-title">${escapeHtml(task.title)}</h3>
      <p class="task-meta">
        <span
          class="priority-badge ${priorityClass(priority)}"
          data-priority="${escapeHtml(priority)}"
          aria-label="Priority: ${escapeHtml(priorityLabel(priority))}"
        >${escapeHtml(priorityLabel(priority))}</span>
      </p>
      <p class="task-meta task-due-date" data-due-date="${escapeHtml(task.due_date || "")}">
        Due ${escapeHtml(task.due_date)}
      </p>
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

  function fillAssigneeSelect(selectEl, users) {
    if (!selectEl) {
      return;
    }
    const previous = selectEl.value;
    selectEl.innerHTML = "";
    const blank = document.createElement("option");
    blank.value = "";
    blank.textContent = "Unassigned";
    selectEl.appendChild(blank);
    (users || []).forEach((user) => {
      const option = document.createElement("option");
      option.value = String(user.id);
      option.textContent = `${user.full_name} (${user.email})`;
      selectEl.appendChild(option);
    });
    if (previous) {
      selectEl.value = previous;
    }
  }

  async function loadAssigneeOptions() {
    if (!canCreate || assigneeOptionsLoaded) {
      return;
    }
    try {
      const response = await fetch("/api/users", { credentials: "same-origin" });
      if (response.status === 401) {
        window.location.assign("/login");
        return;
      }
      if (!response.ok) {
        return;
      }
      const users = await response.json();
      const list = Array.isArray(users) ? users : [];
      fillAssigneeSelect(document.getElementById("task-assignee-id"), list);
      fillAssigneeSelect(document.getElementById("edit-task-assignee-id"), list);
      assigneeOptionsLoaded = true;
    } catch (error) {
      // Leave Unassigned-only selects; create/edit still work without assignee.
    }
  }

  function openCreateDialog() {
    if (!dialog || !form) {
      return;
    }
    clearCreateErrors();
    form.reset();
    void loadAssigneeOptions();
    dialog.showModal();
  }

  function closeCreateDialog() {
    if (dialog) {
      dialog.close();
    }
  }

  async function openEditDialog(taskId) {
    if (!editDialog || !editForm) {
      return;
    }
    const task = tasksById[taskId];
    if (!task) {
      return;
    }
    clearEditErrors();
    await loadAssigneeOptions();
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

  function openDeleteDialog(taskId) {
    if (!deleteDialog || !deleteTaskIdInput) {
      return;
    }
    const task = tasksById[taskId];
    if (!task) {
      return;
    }
    if (deleteFormError) {
      deleteFormError.hidden = true;
      deleteFormError.textContent = "";
    }
    deleteTaskIdInput.value = String(task.id);
    if (deleteMessage) {
      deleteMessage.textContent = `Delete "${task.title}"? This cannot be undone.`;
    }
    deleteDialog.showModal();
  }

  function closeDeleteDialog() {
    if (deleteDialog) {
      deleteDialog.close();
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

  async function submitDelete(event) {
    event.preventDefault();
    if (!deleteForm || deleteInFlight) {
      return;
    }
    const taskId = deleteTaskIdInput.value;
    if (deleteFormError) {
      deleteFormError.hidden = true;
      deleteFormError.textContent = "";
    }

    deleteInFlight = true;
    if (deleteConfirmBtn) {
      deleteConfirmBtn.disabled = true;
    }
    try {
      const response = await fetch(`/api/tasks/${taskId}`, {
        method: "DELETE",
        credentials: "same-origin",
      });
      if (response.status === 401) {
        window.location.assign("/login");
        return;
      }
      if (response.status === 204) {
        closeDeleteDialog();
        const card = root.querySelector(`.task-card[data-task-id="${taskId}"]`);
        if (card) {
          card.remove();
        }
        delete tasksById[taskId];
        await loadBoard();
        return;
      }
      const payload = await response.json().catch(() => ({}));
      if (deleteFormError) {
        deleteFormError.hidden = false;
        deleteFormError.textContent = payload.message || "Unable to delete task.";
      }
    } catch (error) {
      if (deleteFormError) {
        deleteFormError.hidden = false;
        deleteFormError.textContent = "Network error deleting the task.";
      }
    } finally {
      deleteInFlight = false;
      if (deleteConfirmBtn) {
        deleteConfirmBtn.disabled = false;
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
  async function moveTaskStatus(taskId, nextStatus) {
    if (statusInFlight || !taskId || !nextStatus) {
      return;
    }
    statusInFlight = true;
    errorEl.hidden = true;
    errorEl.textContent = "";
    try {
      const response = await fetch(`/api/tasks/${taskId}/status`, {
        method: "PATCH",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: nextStatus }),
      });
      if (response.status === 401) {
        window.location.assign("/login");
        return;
      }
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        const fieldMsg =
          payload.fields && payload.fields.status
            ? payload.fields.status
            : payload.message || "Unable to change status.";
        errorEl.hidden = false;
        errorEl.textContent = fieldMsg;
        return;
      }
      await loadBoard();
    } catch (error) {
      errorEl.hidden = false;
      errorEl.textContent = "Network error changing status.";
    } finally {
      statusInFlight = false;
    }
  }

  if (canCreate && editDialog && editForm) {
    root.addEventListener("click", (event) => {
      const statusButton = event.target.closest("[data-status-id]");
      if (statusButton) {
        void moveTaskStatus(
          statusButton.getAttribute("data-status-id"),
          statusButton.getAttribute("data-status-to")
        );
        return;
      }
      const editButton = event.target.closest("[data-edit-id]");
      if (editButton) {
        openEditDialog(editButton.getAttribute("data-edit-id"));
        return;
      }
      const deleteButton = event.target.closest("[data-delete-id]");
      if (deleteButton) {
        openDeleteDialog(deleteButton.getAttribute("data-delete-id"));
      }
    });
    if (editCancelBtn) {
      editCancelBtn.addEventListener("click", closeEditDialog);
    }
    editForm.addEventListener("submit", submitEdit);
  }
  if (canCreate && deleteDialog && deleteForm) {
    if (deleteCancelBtn) {
      deleteCancelBtn.addEventListener("click", closeDeleteDialog);
    }
    deleteForm.addEventListener("submit", submitDelete);
  }

  if (canCreate) {
    void loadAssigneeOptions();
  }
  loadBoard();
})();

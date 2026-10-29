/**
 * Pure status→column grouping for the Kanban board (US04).
 * Usable in the browser (global) and from Node (module.exports) for Pytest.
 * @param {Array<{status?: string}>|null|undefined} tasks
 * @returns {{todo: object[], in_progress: object[], done: object[]}}
 */
function groupTasksByStatus(tasks) {
  const grouped = { todo: [], in_progress: [], done: [] };
  (tasks || []).forEach((task) => {
    if (Object.prototype.hasOwnProperty.call(grouped, task.status)) {
      grouped[task.status].push(task);
    }
  });
  return grouped;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { groupTasksByStatus };
}

async function api(path, opts = {}) {
  const config = {
    headers: { 'Content-Type': 'application/json' },
    method: 'GET',
    ...opts,
  };
  if (config.body && typeof config.body !== 'string') {
    config.body = JSON.stringify(config.body);
  }
  const res = await fetch(path, config);
  let body = null;
  try {
    body = await res.json();
  } catch (_) {
    body = null;
  }
  if (!res.ok) {
    const message = (body && (body.error || body.message)) || `HTTP ${res.status}`;
    const error = new Error(message);
    error.status = res.status;
    error.body = body;
    throw error;
  }
  return body;
}

function showMessage(message, type = 'info') {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.remove('success', 'error', 'info', 'show');
  if (type) {
    toast.classList.add(type);
  }
  window.clearTimeout(toast._hideTimeout);
  requestAnimationFrame(() => {
    toast.classList.add('show');
  });
  toast._hideTimeout = window.setTimeout(() => {
    toast.classList.remove('show');
  }, 2500);
}

function errorMessageFrom(err) {
  const code = err?.body?.error || String(err?.message || '');
  if (code.includes('email_already_exists')) return 'Ese correo ya está registrado';
  if (code.includes('validation_error')) return 'Datos inválidos';
  if (code.includes('not_found')) return 'No encontrado';
  return 'Error interno';
}

async function loadUsers() {
  const tbody = document.querySelector('#users-tbody');
  if (!tbody) return;
  try {
    const rows = await api('/api/users');
    tbody.innerHTML = rows
      .map(
        (u) => `
        <tr>
          <td>${u.id}</td>
          <td>${u.name}</td>
          <td>${u.email}</td>
          <td>
            <button class="btn btn-ghost" data-action="delete" data-id="${u.id}">Eliminar</button>
          </td>
        </tr>`
      )
      .join('');
  } catch (err) {
    showMessage(errorMessageFrom(err), 'error');
  }
}

function setupUsersTable() {
  const tbody = document.querySelector('#users-tbody');
  if (!tbody) return;
  tbody.addEventListener('click', async (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) return;
    if (target.dataset.action !== 'delete') return;
    const uid = target.dataset.id;
    if (!uid) return;
    if (!confirm(`¿Eliminar usuario ${uid}?`)) return;
    try {
      await api(`/api/users/${uid}`, { method: 'DELETE' });
      showMessage('Usuario eliminado', 'success');
      await loadUsers();
    } catch (err) {
      showMessage(errorMessageFrom(err), 'error');
    }
  });
}

function setupRegisterForm() {
  const form = document.querySelector('#register-form');
  if (!form) return;
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    try {
      await api('/api/users', { method: 'POST', body: data });
      showMessage('Usuario creado', 'success');
      form.reset();
      if (location.pathname === '/users') {
        await loadUsers();
      }
    } catch (err) {
      showMessage(errorMessageFrom(err), 'error');
    }
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    setupRegisterForm();
    setupUsersTable();
    if (location.pathname === '/users') loadUsers();
  });
} else {
  setupRegisterForm();
  setupUsersTable();
  if (location.pathname === '/users') loadUsers();
}

window.api = api;
window.errorMessageFrom = errorMessageFrom;
window.showMessage = showMessage;
window.loadUsers = loadUsers;

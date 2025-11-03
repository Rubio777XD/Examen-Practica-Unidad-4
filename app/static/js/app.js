async function api(path, opts = {}) {
  const config = {
    method: 'GET',
    ...opts,
  };
  config.headers = {
    'Content-Type': 'application/json',
    ...(opts.headers || {}),
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
  if (code.includes('invalid_credentials')) return 'Credenciales inválidas';
  if (code.includes('invalid_content')) return 'El mensaje no puede estar vacío ni exceder 500 caracteres';
  if (code.includes('not_found')) return 'No encontrado';
  return 'Error interno';
}

function escapeHtml(value) {
  return String(value || '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function getAuthUser() {
  const raw = localStorage.getItem('auth_user');
  if (!raw) return null;
  try {
    const user = JSON.parse(raw);
    if (user && typeof user === 'object') {
      return user;
    }
  } catch (_) {
    // ignore parse errors and clean storage
  }
  localStorage.removeItem('auth_user');
  return null;
}

function dispatchAuthChanged() {
  const event = new CustomEvent('auth-changed', { detail: { user: getAuthUser() } });
  window.dispatchEvent(event);
}

function updateAuthAwareUI() {
  updateAuthLink();
  updateWallIdentity();
}

function setAuthUser(user) {
  localStorage.setItem('auth_user', JSON.stringify(user));
  updateAuthAwareUI();
  dispatchAuthChanged();
}

function clearAuthUser() {
  localStorage.removeItem('auth_user');
  updateAuthAwareUI();
  dispatchAuthChanged();
}

function updateAuthLink() {
  const link = document.getElementById('auth-link');
  if (!link) return;
  const user = getAuthUser();
  if (user) {
    link.textContent = 'Cerrar sesión';
    link.href = '#';
    link.dataset.action = 'logout';
  } else {
    link.textContent = 'Iniciar sesión';
    link.href = '/login';
    link.dataset.action = 'login';
  }
}

function setupAuthLink() {
  const link = document.getElementById('auth-link');
  if (!link) return;
  updateAuthLink();
  link.addEventListener('click', (event) => {
    if (link.dataset.action !== 'logout') return;
    event.preventDefault();
    clearAuthUser();
    showMessage('Sesión cerrada', 'info');
    window.location.replace('/');
  });
  window.addEventListener('storage', (ev) => {
    if (ev.key === 'auth_user') {
      updateAuthAwareUI();
    }
  });
  window.addEventListener('auth-changed', updateAuthAwareUI);
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

function updateWallIdentity() {
  const identity = document.getElementById('wall-identity');
  if (!identity) return;
  const user = getAuthUser();
  const name = user?.name || 'Anónimo';
  identity.innerHTML = `Publicarás como <strong>${escapeHtml(name)}</strong>`;
}

async function loadWallPosts() {
  const container = document.getElementById('wall-posts');
  if (!container) return;
  try {
    const posts = await api('/api/wall/posts');
    if (!Array.isArray(posts) || posts.length === 0) {
      container.innerHTML = '<p class="wall-empty">Aún no hay comentarios. ¡Sé el primero en escribir uno!</p>';
      return;
    }
    container.innerHTML = posts
      .map((post) => {
        const timestamp = new Date(post.created_at || Date.now());
        const formatted = `${timestamp.toLocaleString('es-ES', { timeZone: 'UTC' })} UTC`;
        return `
        <article class="wall-post">
          <header>
            <strong>${escapeHtml(post.author)}</strong>
            <time datetime="${escapeHtml(post.created_at)}">${escapeHtml(formatted)}</time>
          </header>
          <p>${escapeHtml(post.content)}</p>
        </article>`;
      })
      .join('');
  } catch (err) {
    container.innerHTML = '<p class="wall-empty error">No se pudieron cargar los comentarios.</p>';
    showMessage(errorMessageFrom(err), 'error');
  }
}

function setupWallForm() {
  const form = document.getElementById('wall-form');
  if (!form) return;
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    const content = (data.content || '').trim();
    if (!content) {
      showMessage('Escribe un mensaje antes de publicar', 'error');
      return;
    }
    const user = getAuthUser();
    const headers = {};
    if (user?.name) {
      headers['X-Author'] = user.name;
    }
    try {
      await api('/api/wall/posts', { method: 'POST', headers, body: { content } });
      form.reset();
      updateWallIdentity();
      await loadWallPosts();
      showMessage('Comentario publicado', 'success');
    } catch (err) {
      showMessage(errorMessageFrom(err), 'error');
    }
  });
}

function setupWallPage() {
  setupWallForm();
  updateWallIdentity();
  loadWallPosts();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    setupAuthLink();
    setupRegisterForm();
    setupUsersTable();
    if (location.pathname === '/users') loadUsers();
    if (location.pathname === '/muro') setupWallPage();
  });
} else {
  setupAuthLink();
  setupRegisterForm();
  setupUsersTable();
  if (location.pathname === '/users') loadUsers();
  if (location.pathname === '/muro') setupWallPage();
}

window.api = api;
window.errorMessageFrom = errorMessageFrom;
window.showMessage = showMessage;
window.loadUsers = loadUsers;
window.getAuthUser = getAuthUser;
window.setAuthUser = setAuthUser;
window.clearAuthUser = clearAuthUser;
window.setupWallPage = setupWallPage;
window.loadWallPosts = loadWallPosts;

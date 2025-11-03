async function api(method, url, body) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body !== undefined) {
    options.body = JSON.stringify(body);
  }
  const response = await fetch(url, options);
  let data = null;
  try {
    data = await response.json();
  } catch (error) {
    data = null;
  }
  if (!response.ok) {
    return { ok: false, status: response.status, ...(data || {}) };
  }
  return { ok: true, status: response.status, ...(data || {}) };
}

const apiGet = (url) => api('GET', url);
const apiPost = (url, body) => api('POST', url, body);
const apiPut = (url, body) => api('PUT', url, body);
const apiDelete = (url) => api('DELETE', url);

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

function getDemoUser() {
  const raw = localStorage.getItem('demo_user');
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch (error) {
    return null;
  }
}

function setDemoUser(user) {
  localStorage.setItem('demo_user', JSON.stringify(user));
}

function clearDemoUser() {
  localStorage.removeItem('demo_user');
}

window.apiGet = apiGet;
window.apiPost = apiPost;
window.apiPut = apiPut;
window.apiDelete = apiDelete;
window.showMessage = showMessage;
window.getDemoUser = getDemoUser;
window.setDemoUser = setDemoUser;
window.clearDemoUser = clearDemoUser;

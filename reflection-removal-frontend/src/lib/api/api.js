const RAW_API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const API_BASE = RAW_API_BASE.replace(/\/$/, '');

export function getStoredToken() {
  if (typeof window === "undefined") return null;

  const keys = ["token", "authToken", "access_token", "refresh_token"];
  for (const storage of [window.localStorage, window.sessionStorage]) {
    for (const key of keys) {
      const value = storage.getItem(key);
      if (value && value !== "undefined" && value !== "null") {
        return value;
      }
    }
  }

  return null;
}

export function hasStoredToken() {
  return Boolean(getStoredToken());
}

export async function apiFetch(path, options = {}) {
  const token = getStoredToken();

  let body = options.body;
  const headers = { ...(options.headers || {}) };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Automatically handle JSON for objects that aren't FormData
  if (body && typeof body === 'object' && !(body instanceof FormData)) {
    body = JSON.stringify(body);
    if (!headers["Content-Type"]) {
      headers["Content-Type"] = "application/json";
    }
  }

  // Ensure JSON header if body is a pre-stringified string
  if (typeof body === 'string' && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  return fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    body
  });
}

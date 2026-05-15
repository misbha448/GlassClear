import { apiFetch } from './api.js';

async function readResponse(response) {
  let payload = null;

  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const error = new Error(payload?.detail || payload?.message || 'Request failed');
    error.status = response.status;
    error.payload = payload;
    throw error;
  }

  return payload;
}

function withQuery(params = {}) {
  const query = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      query.set(key, String(value));
    }
  });

  const queryString = query.toString();
  return queryString ? `?${queryString}` : '';
}

export async function getAdminOverview() {
  return readResponse(await apiFetch('/api/admin/overview'));
}

export async function getAdminAnalytics() {
  return readResponse(await apiFetch('/api/admin/analytics'));
}

export async function getAdminUsers(params = {}) {
  return readResponse(await apiFetch(`/api/admin/users${withQuery(params)}`));
}

export async function getAdminUser(userId) {
  return readResponse(await apiFetch(`/api/admin/users/${userId}`));
}

export async function updateUserStatus(userId, status) {
  return readResponse(
    await apiFetch(`/api/admin/users/${userId}/status`, {
      method: 'PATCH',
      body: { status }
    })
  );
}

export async function deleteUser(userId) {
  return readResponse(await apiFetch(`/api/admin/users/${userId}`, { method: 'DELETE' }));
}

export async function getAdminJobs(params = {}) {
  return readResponse(await apiFetch(`/api/admin/jobs${withQuery(params)}`));
}

export async function deleteJob(jobId) {
  return readResponse(await apiFetch(`/api/admin/jobs/${jobId}`, { method: 'DELETE' }));
}

export async function reprocessJob(jobId) {
  return readResponse(await apiFetch(`/api/admin/jobs/${jobId}/reprocess`, { method: 'POST' }));
}

export async function getAdminShares(params = {}) {
  return readResponse(await apiFetch(`/api/admin/shares${withQuery(params)}`));
}

export async function disableShare(shareId) {
  return readResponse(await apiFetch(`/api/admin/shares/${shareId}/disable`, { method: 'PATCH' }));
}

export async function deleteShare(shareId) {
  return readResponse(await apiFetch(`/api/admin/shares/${shareId}`, { method: 'DELETE' }));
}

export async function getSystemHealth() {
  return readResponse(await apiFetch('/api/admin/system-health'));
}

export async function clearFailedJobs() {
  return readResponse(await apiFetch('/api/admin/maintenance/clear-failed-jobs', { method: 'POST' }));
}

export async function cleanupExpiredShares() {
  return readResponse(await apiFetch('/api/admin/maintenance/cleanup-expired-shares', { method: 'POST' }));
}

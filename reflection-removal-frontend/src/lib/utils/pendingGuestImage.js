const STORAGE_KEY = 'glassclear_pending_guest_result';

export function savePendingGuestImage(payload) {
  if (typeof localStorage === 'undefined') return;
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      ...payload,
      saved_at: new Date().toISOString()
    })
  );
}

export function loadPendingGuestImage() {
  if (typeof localStorage === 'undefined') return null;
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw);
    if (parsed && parsed.guest_token && !parsed.guest_image_token) {
      parsed.guest_image_token = parsed.guest_token;
    }
    return parsed;
  } catch {
    localStorage.removeItem(STORAGE_KEY);
    return null;
  }
}

export function clearPendingGuestImage() {
  if (typeof localStorage === 'undefined') return;
  localStorage.removeItem(STORAGE_KEY);
}

export function hasPendingGuestImage() {
  return Boolean(loadPendingGuestImage());
}

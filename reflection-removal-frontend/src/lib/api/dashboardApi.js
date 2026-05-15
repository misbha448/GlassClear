import { API_BASE, apiFetch } from './api.js';

export const DASHBOARD_ENDPOINTS = {
  workspace: '/api/dashboard/workspace',
  workspaceImage: '/api/dashboard/workspace/images',
  history: '/api/dashboard/history',
  smartAlbums: '/api/dashboard/smart-albums',
  albums: '/api/dashboard/albums',
  claimGuestImage: '/api/dashboard/claim-guest-image',
  upload: '/api/editor/upload',
  applyReflection: '/api/editor/apply-reflection',
  versions: '/api/editor/images',
  export: '/api/editor/export',
  projects: '/api/projects',
  share: '/api/share-links',
  publicShare: '/api/share-links/public',
  shareComparison: '/api/share/comparison',
  activateVersion: '/api/editor/versions',
  batchUpload: '/api/batch/upload',
  exportDownload: '/api/export',
  collections: '/api/collections',
  deliveryPacks: '/api/delivery-packs',
  me: '/api/v1/users/me'
};

export function withBase(url) {
  if (!url) return null;
  return url.startsWith('http') ? url : `${API_BASE}${url}`;
}

export function resolveAssetUrl(path) {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  if (path.startsWith('/uploads')) return `${API_BASE}${path}`;
  return path;
}

async function readJson(response) {
  let payload = null;

  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const message =
      payload?.detail ||
      payload?.message ||
      (response.status === 401 ? 'Your session expired. Please log in again.' : 'Request failed.');
    const error = new Error(message);
    error.status = response.status;
    error.payload = payload;
    throw error;
  }

  return payload;
}

async function request(path, options = {}) {
  const response = await apiFetch(path, options);
  return readJson(response);
}

async function requestPublic(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);
  return readJson(response);
}

async function downloadResponseFile(response, fallbackFilename = 'glassclear-download') {
  if (!response.ok) {
    await readJson(response);
  }

  const blob = await response.blob();
  const objectUrl = URL.createObjectURL(blob);
  const disposition = response.headers.get('content-disposition') || '';
  const match = disposition.match(/filename="?([^"]+)"?/i);
  const filename = match?.[1] || fallbackFilename;
  const anchor = document.createElement('a');
  anchor.href = objectUrl;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(objectUrl);
}

export function getGoogleLoginUrl() {
  return `${API_BASE}/api/auth/google/login`;
}

export async function getWorkspace() {
  return request(DASHBOARD_ENDPOINTS.workspace);
}

export async function getWorkspaceImage(imageId) {
  return request(`${DASHBOARD_ENDPOINTS.workspaceImage}/${imageId}`);
}

export async function getCurrentUser() {
  return request(DASHBOARD_ENDPOINTS.me);
}

export async function getHistory(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') query.set(key, String(value));
  });
  const suffix = query.toString() ? `?${query.toString()}` : '';
  return request(`${DASHBOARD_ENDPOINTS.history}${suffix}`);
}

export async function getSmartAlbums() {
  return request(DASHBOARD_ENDPOINTS.smartAlbums);
}

export async function getAlbums() {
  return request(DASHBOARD_ENDPOINTS.albums);
}

export async function getAlbum(albumSlug) {
  return request(`${DASHBOARD_ENDPOINTS.albums}/${encodeURIComponent(String(albumSlug || '').trim())}`);
}

export async function getCollections() {
  return request(DASHBOARD_ENDPOINTS.collections);
}

export async function createCollection(name) {
  return request(DASHBOARD_ENDPOINTS.collections, {
    method: 'POST',
    body: { name }
  });
}

export async function getCollection(collectionId) {
  return request(`${DASHBOARD_ENDPOINTS.collections}/${collectionId}`);
}

export async function addCollectionItem(collectionId, predictionId) {
  return request(`${DASHBOARD_ENDPOINTS.collections}/${collectionId}/items`, {
    method: 'POST',
    body: { prediction_id: predictionId }
  });
}

export async function removeCollectionItem(collectionId, predictionId) {
  return request(`${DASHBOARD_ENDPOINTS.collections}/${collectionId}/items/${predictionId}`, {
    method: 'DELETE'
  });
}

export async function createDeliveryPack(predictionId) {
  return request(DASHBOARD_ENDPOINTS.deliveryPacks, {
    method: 'POST',
    body: { prediction_id: predictionId }
  });
}

export async function downloadDeliveryPack(packId) {
  const response = await apiFetch(`${DASHBOARD_ENDPOINTS.deliveryPacks}/${packId}/download`);
  await downloadResponseFile(response, `glassclear-delivery-pack-${packId}.zip`);
}

export async function uploadBatch(files = []) {
  const body = new FormData();
  files.forEach((file) => body.append('files', file));
  return request(DASHBOARD_ENDPOINTS.batchUpload, { method: 'POST', body });
}

export async function startBatch(batchId) {
  return request(`/api/batch/${batchId}/start`, { method: 'POST' });
}

export async function getBatchStatus(batchId) {
  return request(`/api/batch/${batchId}`);
}

export async function downloadBatchZip(batchId) {
  return apiFetch(`/api/batch/${batchId}/download-zip`);
}

export async function createShareLink(imageId, title = 'GlassClear Result') {
  console.info('[share] selected prediction id', imageId);
  const response = await request(DASHBOARD_ENDPOINTS.share, {
    method: 'POST',
    body: {
      prediction_id: imageId,
      title,
      allow_download: true,
      expires_in_days: null
    }
  });
  console.info('[share] POST response', response);
  return response;
}

export async function deleteHistoryItem(imageId) {
  return request(`/api/dashboard/history/${imageId}`, { method: 'DELETE' });
}

export async function uploadDashboardImage(file, projectId) {
  const body = new FormData();
  body.append('file', file);
  if (projectId) body.append('project_id', projectId);
  return request(DASHBOARD_ENDPOINTS.upload, { method: 'POST', body });
}

export async function uploadImage(file, projectId) {
  return uploadDashboardImage(file, projectId);
}

export async function applyReflection(imageId, settings = {}) {
  return request(DASHBOARD_ENDPOINTS.applyReflection, {
    method: 'POST',
    body: { image_id: imageId, settings }
  });
}

export async function getVersions(imageId) {
  return request(`${DASHBOARD_ENDPOINTS.versions}/${imageId}/versions`);
}

export async function activateVersion(versionId) {
  return request(`${DASHBOARD_ENDPOINTS.activateVersion}/${versionId}/activate`, { method: 'PUT' });
}

export async function getProjects() {
  return request(DASHBOARD_ENDPOINTS.projects);
}

export async function createProject(data) {
  return request(DASHBOARD_ENDPOINTS.projects, { method: 'POST', body: data });
}

export async function addImageToProject(projectId, imageId) {
  return request(`${DASHBOARD_ENDPOINTS.projects}/${projectId}/add-image`, {
    method: 'POST',
    body: { image_id: imageId }
  });
}

export async function attachImageToProject(projectId, imageId) {
  return addImageToProject(projectId, imageId);
}

export async function getPublicShare(token) {
  console.info('[share] route token', token);
  const response = await fetch(`${API_BASE}${DASHBOARD_ENDPOINTS.publicShare}/${token}`);
  let body = null;

  try {
    body = await response.json();
  } catch {
    body = null;
  }

  console.info('[share] public API response', { status: response.status, body });

  if (!response.ok) {
    const message =
      body?.detail ||
      body?.message ||
      (response.status === 401 ? 'Your session expired. Please log in again.' : 'Request failed.');
    const error = new Error(message);
    error.status = response.status;
    error.payload = body;
    throw error;
  }

  return body;
}

export async function downloadBatchZipFile(batchId) {
  const response = await downloadBatchZip(batchId);
  await downloadResponseFile(response, `glassclear-batch-${batchId}.zip`);
}

export async function downloadFile(url, filename = 'glassclear-result.png') {
  if (!url) {
    const error = new Error('No processed image available.');
    error.status = 400;
    throw error;
  }

  const absoluteUrl = resolveAssetUrl(url);

  try {
    const response = await fetch(absoluteUrl);
    if (!response.ok) throw new Error('download-failed');
    const blob = await response.blob();
    const objectUrl = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = objectUrl;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(objectUrl);
    return true;
  } catch {
    window.open(absoluteUrl, '_blank', 'noopener');
    return false;
  }
}

export async function downloadImage(url, filename = 'glassclear-result.png') {
  return downloadFile(url, filename);
}

export async function downloadComparisonImage(originalUrl, processedUrl, filename = 'GlassClear_Comparison.png') {
  if (!originalUrl || !processedUrl) {
    const error = new Error('No processed image available.');
    error.status = 400;
    throw error;
  }

  const loadImage = (src) =>
    new Promise((resolve, reject) => {
      const image = new Image();
      image.crossOrigin = 'anonymous';
      image.onload = () => resolve(image);
      image.onerror = () => reject(new Error('image-load-failed'));
      image.src = resolveAssetUrl(src);
    });

  const [beforeImage, afterImage] = await Promise.all([loadImage(originalUrl), loadImage(processedUrl)]);
  const canvas = document.createElement('canvas');
  canvas.width = 1600;
  canvas.height = 900;
  const context = canvas.getContext('2d');
  if (!context) throw new Error('canvas-unavailable');

  context.fillStyle = '#ffffff';
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.fillStyle = '#172033';
  context.font = '700 34px Arial';
  context.fillText('GlassClear Comparison', 60, 56);
  context.fillStyle = '#6b7280';
  context.font = '600 18px Arial';
  context.fillText('Automated Glare & Reflection Elimination', 60, 860);

  const drawContained = (image, x, y, width, height) => {
    const ratio = Math.min(width / image.width, height / image.height);
    const drawWidth = image.width * ratio;
    const drawHeight = image.height * ratio;
    const offsetX = x + (width - drawWidth) / 2;
    const offsetY = y + (height - drawHeight) / 2;
    context.fillStyle = '#f3f4f6';
    context.fillRect(x, y, width, height);
    context.drawImage(image, offsetX, offsetY, drawWidth, drawHeight);
  };

  drawContained(beforeImage, 60, 110, 700, 680);
  drawContained(afterImage, 840, 110, 700, 680);
  context.fillStyle = '#172033';
  context.font = '600 20px Arial';
  context.fillText('Original', 60, 95);
  context.fillText('GlassClear Output', 840, 95);

  try {
    const objectUrl = canvas.toDataURL('image/png');
    const anchor = document.createElement('a');
    anchor.href = objectUrl;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    return true;
  } catch {
    const error = new Error('Could not generate comparison image due to image access settings.');
    error.status = 500;
    throw error;
  }
}

export async function exportImage(imageId) {
  return request(DASHBOARD_ENDPOINTS.export, {
    method: 'POST',
    body: { image_id: imageId, type: 'processed' }
  });
}

export async function downloadShareComparison(imageId) {
  const response = await apiFetch(`${DASHBOARD_ENDPOINTS.shareComparison}/${imageId}`);
  await downloadResponseFile(response, `glassclear-comparison-${imageId}.jpg`);
}

export async function downloadExportVariant(imageId, format) {
  const response = await apiFetch(`${DASHBOARD_ENDPOINTS.exportDownload}/${imageId}?format=${encodeURIComponent(format)}`);
  await downloadResponseFile(response, `glassclear-export-${imageId}`);
}

export async function exportProcessedImage(imageId) {
  return exportImage(imageId);
}

export async function claimGuestImage(token) {
  return request(DASHBOARD_ENDPOINTS.claimGuestImage, {
    method: 'POST',
    body: { guest_image_token: token }
  });
}

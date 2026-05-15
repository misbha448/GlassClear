export function getDisplayName(item = null) {
  if (item?.title) return item.title;
  if (item?.display_name) return item.display_name;

  const rawName = item?.filename || item?.original_filename || 'GlassClear Result';
  if (/^[a-f0-9]{20,}\.(jpg|jpeg|png|webp)$/i.test(rawName)) {
    return 'GlassClear Restoration';
  }

  return rawName.replace(/\.[^/.]+$/, '').replace(/[-_]+/g, ' ').trim() || 'GlassClear Result';
}

export function getDownloadName(item = null, suffix = 'Output') {
  const base = getDisplayName(item)
    .replace(/[^a-z0-9]+/gi, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '') || 'GlassClear_Output';
  const stamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  return `${base}_${suffix}_${stamp}.png`;
}

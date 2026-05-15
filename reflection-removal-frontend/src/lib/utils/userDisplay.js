export function getDisplayName(user = null) {
  const rawName = user?.name || user?.username || '';
  if (rawName && rawName.trim()) return rawName.trim();

  const email = user?.email || '';
  if (email.includes('@')) {
    const prefix = email.split('@')[0]?.trim();
    if (prefix) return prefix;
  }

  return 'User';
}

export function getUserInitial(user = null) {
  const source = getDisplayName(user) || user?.email || 'User';
  return source.trim().charAt(0).toUpperCase() || 'U';
}

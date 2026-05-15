const NAME_PATTERN = /^[A-Za-z ]+$/;
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function normalizeName(value = '') {
  return value.trim().replace(/\s+/g, ' ');
}

export function normalizeEmail(value = '') {
  return value.trim().toLowerCase();
}

export function validateName(value = '') {
  const normalized = normalizeName(value);
  if (!normalized) return 'Name is required.';
  if (normalized.length < 3) return 'Name must be at least 3 characters.';
  if (normalized.length > 50) return 'Name must be at most 50 characters.';
  if (!NAME_PATTERN.test(normalized)) return 'Name must contain only alphabets and spaces.';
  return '';
}

export function validateEmail(value = '') {
  const normalized = normalizeEmail(value);
  if (!normalized || !EMAIL_PATTERN.test(normalized)) {
    return 'Enter a valid email address.';
  }
  return '';
}

export function getPasswordChecks(password = '') {
  return {
    minLength: password.length >= 8,
    maxLength: password.length <= 64,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /\d/.test(password),
    special: /[^A-Za-z0-9]/.test(password)
  };
}

export function validatePassword(value = '') {
  if (!value) return 'Password must be at least 8 characters.';

  const checks = getPasswordChecks(value);
  if (!checks.minLength) return 'Password must be at least 8 characters.';
  if (!checks.maxLength) return 'Password must be at most 64 characters.';
  if (!(checks.uppercase && checks.lowercase && checks.number && checks.special)) {
    return 'Password must include uppercase, lowercase, number, and special character.';
  }
  return '';
}

export function validateLoginPassword(value = '') {
  return value ? '' : 'Password is required.';
}

export function validateConfirmPassword(password = '', confirmPassword = '') {
  if (!confirmPassword) return 'Please confirm your password.';
  return password === confirmPassword ? '' : 'Passwords do not match.';
}

export function mapAuthServerError(message = '') {
  switch (message) {
    case 'Name is required.':
    case 'Name must be at least 3 characters.':
    case 'Name must be at most 50 characters.':
    case 'Name must contain only alphabets and spaces.':
      return { field: 'name', message };
    case 'Enter a valid email address.':
    case 'Email already registered':
    case 'Email already registered.':
      return { field: 'email', message: message.endsWith('.') ? message : `${message}.` };
    case 'Password must be at least 8 characters.':
    case 'Password must be at most 64 characters.':
    case 'Password must include uppercase, lowercase, number, and special character.':
    case 'Password is required.':
      return { field: 'password', message };
    default:
      return { field: null, message };
  }
}

import { browser } from '$app/environment';
import { get, writable } from 'svelte/store';
import { SUPPORTED_LOCALES, translations } from '$lib/i18n/index.js';

const STORAGE_KEY = 'glassclear_language';

export const LANGUAGE_OPTIONS = [
  { code: 'en', label: 'English' },
  { code: 'hi', label: 'हिन्दी' },
  { code: 'kn', label: 'ಕನ್ನಡ' }
];

const LEGACY_KEY_MAP = {
  upload_title: 'upload.title',
  upload_subtitle: 'upload.subtitle',
  process_button: 'upload.processButton',
  preview_title: 'upload.previewTitle',
  nav_dashboard: 'common.dashboard',
  nav_logout: 'common.logout',
  login_title: 'auth.loginTitle',
  login_email: 'auth.emailPlaceholder',
  login_pass: 'auth.passwordPlaceholder',
  login_btn: 'auth.loginButton',
  login_error_msg: 'auth.loginError',
  signup_title: 'auth.signupTitle',
  signup_name: 'auth.fullNamePlaceholder',
  signup_email: 'auth.emailPlaceholder',
  signup_pass: 'auth.passwordPlaceholder',
  signup_btn: 'auth.signupButton',
  signup_error_msg: 'auth.signupError',
  signup_success: 'auth.signupSuccess',
  res_new: 'result.newResult',
  exp_free: 'result.downloadFree',
  res_original: 'result.originalTitle',
  res_removed: 'result.removedTitle',
  btn_reprocess: 'result.processAnother',
  upload_error_download: 'common.somethingWentWrong',
  upload_error_engine: 'common.somethingWentWrong'
};

function getInitialLanguage() {
  if (!browser) return 'en';
  const saved = localStorage.getItem(STORAGE_KEY);
  return saved && translations[saved] ? saved : 'en';
}

function syncDocumentLanguage(languageCode) {
  if (!browser) return;
  document.documentElement.lang = languageCode;
}

function resolvePath(source, path) {
  return path.split('.').reduce((value, key) => value?.[key], source);
}

function formatString(value, vars) {
  if (typeof value !== 'string') return value;
  return value.replace(/\{(\w+)\}/g, (_, key) => String(vars?.[key] ?? ''));
}

function normalizeTranslationValue(value) {
  return typeof value === 'string' ? value : null;
}

function normalizeKey(key) {
  return key.includes('.') ? key : LEGACY_KEY_MAP[key] || key;
}

export const language = writable(getInitialLanguage());
export const currentLanguage = language;

export function setLanguage(languageCode) {
  if (!SUPPORTED_LOCALES.includes(languageCode) || !translations[languageCode]) return;
  language.set(languageCode);
  if (browser) {
    localStorage.setItem(STORAGE_KEY, languageCode);
  }
  syncDocumentLanguage(languageCode);
}

export function initializeLanguage() {
  const initialLanguage = getInitialLanguage();
  syncDocumentLanguage(initialLanguage);
  return initialLanguage;
}

export function translateKey(key, languageCode = 'en', fallback = key, vars = {}) {
  const path = normalizeKey(key);
  const currentValue = normalizeTranslationValue(resolvePath(translations[languageCode], path));
  const fallbackValue = normalizeTranslationValue(resolvePath(translations.en, path));
  return formatString(currentValue ?? fallbackValue ?? fallback, vars);
}

export function t(key, fallbackOrVars = key, maybeVars = {}) {
  const fallback = typeof fallbackOrVars === 'string' ? fallbackOrVars : key;
  const vars = typeof fallbackOrVars === 'object' && fallbackOrVars !== null ? fallbackOrVars : maybeVars;
  return translateKey(key, get(language), fallback, vars);
}

if (browser) {
  initializeLanguage();
}

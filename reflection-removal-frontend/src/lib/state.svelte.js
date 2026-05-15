import { currentLanguage, LANGUAGE_OPTIONS, setLanguage as setStoreLanguage, translateKey } from '$lib/stores/language.js';

const LANGUAGE_NAME_MAP = {
  en: 'English',
  hi: 'हिन्दी',
  kn: 'ಕನ್ನಡ'
};

const LANGUAGE_CODE_MAP = {
  English: 'en',
  हिन्दी: 'hi',
  ಕನ್ನಡ: 'kn',
  Hindi: 'hi',
  Kannada: 'kn',
  en: 'en',
  hi: 'hi',
  kn: 'kn'
};

export const appState = $state({
  language: 'English',
  languageCode: 'en'
});

currentLanguage.subscribe((code) => {
  appState.languageCode = code;
  appState.language = LANGUAGE_NAME_MAP[code] || 'English';
});

export function setLanguage(language) {
  const code = LANGUAGE_CODE_MAP[language] || language;
  if (!code) return;
  setStoreLanguage(code);
}

export function getSupportedLanguages() {
  return LANGUAGE_OPTIONS.map((option) => LANGUAGE_NAME_MAP[option.code] || option.label);
}

export function t(key, vars = {}) {
  return translateKey(key, appState.languageCode, key, vars);
}

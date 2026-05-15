<script>
  import { clickOutside } from '$lib/actions/clickOutside';
  import { appState, getSupportedLanguages, setLanguage, t } from '$lib/state.svelte.js';

  const labels = {
    English: 'English',
    हिन्दी: 'हिन्दी',
    ಕನ್ನಡ: 'ಕನ್ನಡ'
  };

  const languages = getSupportedLanguages();
  let isOpen = $state(false);
</script>

<div class="dropdown language-shell" use:clickOutside={() => (isOpen = false)}>
  <button
    class="btn dropdown-toggle lang-trigger"
    type="button"
    onclick={() => (isOpen = !isOpen)}
    aria-expanded={isOpen}
    aria-label={t('common.language')}
  >
    <span class="lang-icon-wrap"><i class="bi bi-translate"></i></span>
    <span class="lang-copy">
      <small>{t('common.language')}</small>
      <strong>{labels[appState.language] || appState.language}</strong>
    </span>
    <i class="bi bi-chevron-down lang-caret {isOpen ? 'open' : ''}"></i>
  </button>

  <ul class="dropdown-menu dropdown-menu-end shadow-premium border-0 p-2 lang-menu {isOpen ? 'show' : ''}">
    {#each languages as lang}
      <li>
        <button
          class="dropdown-item lang-item rounded-3 {appState.language === lang ? 'active' : ''}"
          onclick={() => {
            setLanguage(lang);
            isOpen = false;
          }}
        >
          <span>{labels[lang] || lang}</span>
          {#if appState.language === lang}
            <i class="bi bi-check2"></i>
          {/if}
        </button>
      </li>
    {/each}
  </ul>
</div>

<style>
  .language-shell { position: relative; }
  .lang-trigger {
    display: inline-flex;
    align-items: center;
    gap: 0.7rem;
    min-width: 176px;
    padding: 0.45rem 0.75rem;
    border-radius: 14px;
    border: 1px solid rgba(15, 23, 42, 0.08);
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(244, 246, 252, 0.94));
    color: #0f172a;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
  }
  .lang-trigger:hover {
    border-color: rgba(99, 102, 241, 0.28);
    background: linear-gradient(180deg, rgba(255, 255, 255, 1), rgba(238, 242, 255, 0.95));
    color: #0f172a;
  }
  .lang-icon-wrap {
    width: 34px;
    height: 34px;
    border-radius: 11px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.16), rgba(56, 189, 248, 0.12));
    color: #4f46e5;
    flex-shrink: 0;
  }
  .lang-copy {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    line-height: 1.05;
    flex: 1;
  }
  .lang-copy small {
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(15, 23, 42, 0.45);
  }
  .lang-copy strong {
    font-size: 0.85rem;
    font-weight: 700;
    color: #0f172a;
  }
  .lang-caret {
    font-size: 0.72rem;
    color: rgba(15, 23, 42, 0.45);
    transition: transform 0.2s ease, color 0.2s ease;
  }
  .lang-caret.open {
    transform: rotate(180deg);
    color: #4f46e5;
  }
  .lang-menu {
    min-width: 100%;
    margin-top: 0.65rem;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(24px);
    border: 1px solid rgba(15, 23, 42, 0.08);
    box-shadow: 0 18px 42px rgba(15, 23, 42, 0.12);
  }
  .lang-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.7rem 0.8rem;
    color: #334155;
    font-size: 0.84rem;
    font-weight: 600;
    background: transparent;
  }
  .lang-item:hover {
    background: rgba(99, 102, 241, 0.08);
    color: #0f172a;
  }
  .lang-item.active {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.16), rgba(56, 189, 248, 0.1));
    color: #0f172a;
  }
  .lang-item i {
    color: #4f46e5;
    font-size: 0.9rem;
  }
</style>

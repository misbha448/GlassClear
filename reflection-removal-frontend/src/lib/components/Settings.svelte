<script>
  import { fade, fly } from 'svelte/transition';
  import { onMount } from 'svelte';
  import { apiFetch } from '$lib/api/api.js';
  import { appState, t } from '$lib/state.svelte.js';

  let user = $state({ name: "Loading...", email: "..." });

  let settings = $state({
    theme: 'Dark',
    defaultMode: 'Quality',
    defaultFormat: 'JPG',
    enableAnimations: true,
    enableSuggestions: true
  });

  const languages = [
    'English',
    'Español',
    'Français',
    'Deutsch',
    'हिंदी',
    'ಕನ್ನಡ',
    'Nederlands',
    'العربية',
    '中文',
    '日本語',
    'Русский'
  ];

  onMount(async () => {
    // Fetch user data
    const response = await apiFetch("/api/v1/users/me");
    if (response.ok) {
      const data = await response.json();
      user = data;
    }

    // Sync toggle with current document theme
    const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'dark';
    settings.theme = currentTheme.charAt(0).toUpperCase() + currentTheme.slice(1);
  });

  // Apply theme change to the whole document
  $effect(() => {
    const themeValue = settings.theme.toLowerCase();
    document.documentElement.setAttribute('data-bs-theme', themeValue);
    
    // Optional: Update body class for custom CSS targeting
    if (themeValue === 'light') {
      document.body.classList.add('light-mode');
    } else {
      document.body.classList.remove('light-mode');
    }
  });

  function handleReset() {
    appState.language = 'English';
    settings.theme = 'Dark';
    settings.defaultMode = 'Quality';
    settings.defaultFormat = 'JPG';
    settings.enableAnimations = true;
    settings.enableSuggestions = true;
  }

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("token_type");
    window.location.href = "/login";
  }
</script>

<div class="settings-container" in:fade>
  <div class="d-flex justify-content-between align-items-end mb-5">
    <div>
      <h2 class="text-white fw-bold mb-1">{t('settings_title')}</h2>
      <p class="text-secondary mb-0">{t('settings_subtitle')}</p>
    </div>
    <button class="btn btn-outline-secondary btn-sm rounded-pill px-3" onclick={handleReset}>
      <i class="bi bi-arrow-counterclockwise me-1"></i> {t('settings_reset')}
    </button>
  </div>

  <div class="row g-4">
    <!-- GENERAL SETTINGS -->
    <div class="col-md-6" in:fly={{ y: 20, delay: 100 }}>
      <div class="glass-card p-4 h-100">
        <h5 class="text-white mb-4"><i class="bi bi-gear-wide-connected me-2 text-primary"></i> {t('settings_general')}</h5>
        
        <div class="settings-group mb-4">
          <label for="lang" class="form-label text-secondary small">{t('settings_lang_label')}</label>
          <select id="lang" bind:value={appState.language} class="form-select glass-input">
            {#each languages as lang}
              <option value={lang}>{lang}</option>
            {/each}
          </select>
        </div>

        <div class="d-flex justify-content-between align-items-center">
          <div>
            <span class="text-white d-block">{t('settings_theme_label')}</span>
            <span class="text-secondary small">{t('settings_theme_sub')}</span>
          </div>
          <div class="form-check form-switch custom-switch">
            <input class="form-check-input" type="checkbox" checked={settings.theme === 'Dark'} 
              onchange={(e) => settings.theme = e.target.checked ? 'Dark' : 'Light'}>
          </div>
        </div>
      </div>
    </div>

    <!-- PROCESSING PREFERENCES -->
    <div class="col-md-6" in:fly={{ y: 20, delay: 200 }}>
      <div class="glass-card p-4 h-100">
        <h5 class="text-white mb-4"><i class="bi bi-cpu me-2 text-info"></i> {t('settings_proc_pref')}</h5>
        
        <div class="row g-3">
          <div class="col-6">
            <label class="form-label text-secondary small">{t('settings_def_mode')}</label>
            <div class="btn-group w-100 p-1 bg-dark rounded-3">
              <button class="btn btn-sm {settings.defaultMode === 'Quality' ? 'btn-primary' : 'text-secondary'}" 
                onclick={() => settings.defaultMode = 'Quality'}>{t('mode_quality')}</button>
              <button class="btn btn-sm {settings.defaultMode === 'Fidelity' ? 'btn-primary' : 'text-secondary'}" 
                onclick={() => settings.defaultMode = 'Fidelity'}>{t('mode_fidelity')}</button>
            </div>
          </div>
          <div class="col-6">
            <label class="form-label text-secondary small">{t('settings_dl_format')}</label>
            <div class="btn-group w-100 p-1 bg-dark rounded-3">
              <button class="btn btn-sm {settings.defaultFormat === 'PNG' ? 'btn-info' : 'text-secondary'}" 
                onclick={() => settings.defaultFormat = 'PNG'}>PNG</button>
              <button class="btn btn-sm {settings.defaultFormat === 'JPG' ? 'btn-info' : 'text-secondary'}" 
                onclick={() => settings.defaultFormat = 'JPG'}>JPG</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- USER EXPERIENCE -->
    <div class="col-md-6" in:fly={{ y: 20, delay: 300 }}>
      <div class="glass-card p-4 h-100">
        <h5 class="text-white mb-4"><i class="bi bi-palette me-2 text-warning"></i> {t('settings_ux')}</h5>
        
        <div class="d-flex justify-content-between align-items-center mb-4">
          <div>
            <span class="text-white d-block">{t('settings_anim')}</span>
            <span class="text-secondary small">{t('settings_anim_sub')}</span>
          </div>
          <div class="form-check form-switch custom-switch">
            <input class="form-check-input" type="checkbox" bind:checked={settings.enableAnimations}>
          </div>
        </div>

        <div class="d-flex justify-content-between align-items-center">
          <div>
            <span class="text-white d-block">{t('settings_sugg')}</span>
            <span class="text-secondary small">{t('settings_sugg_sub')}</span>
          </div>
          <div class="form-check form-switch custom-switch">
            <input class="form-check-input" type="checkbox" bind:checked={settings.enableSuggestions}>
          </div>
        </div>
      </div>
    </div>

    <!-- ACCOUNT SETTINGS -->
    <div class="col-md-6" in:fly={{ y: 20, delay: 400 }}>
      <div class="glass-card p-4 h-100 border-danger border-opacity-10">
        <h5 class="text-white mb-4"><i class="bi bi-person-circle me-2 text-danger"></i> {t('settings_account')}</h5>
        
        <div class="d-flex align-items-center mb-4">
          <div class="avatar-box me-3">
            {user.name ? user.name.charAt(0) : '?'}
          </div>
          <div>
            <h6 class="text-white mb-0">{user.name}</h6>
            <span class="text-secondary small">{user.email}</span>
          </div>
        </div>

        <button class="btn btn-glass-danger w-100 py-2 rounded-3" onclick={handleLogout}>
          <i class="bi bi-box-arrow-right me-2"></i> {t('settings_logout_btn')}
        </button>
      </div>
    </div>
  </div>
</div>

<style>
  .settings-container { max-width: 900px; margin: 0 auto; }

  .glass-input {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    border-radius: 12px;
    padding: 10px 15px;
  }
  .glass-input:focus {
    background: rgba(255, 255, 255, 0.08);
    border-color: #6366f1;
    box-shadow: 0 0 0 0.25rem rgba(99, 102, 241, 0.25);
    color: white;
  }

  /* Custom Switch Styling */
  .custom-switch .form-check-input {
    width: 3rem;
    height: 1.5rem;
    background-color: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    cursor: pointer;
    transition: all 0.3s ease;
  }
  .custom-switch .form-check-input:checked {
    background-color: #6366f1;
    border-color: #6366f1;
  }

  .avatar-box {
    width: 48px; height: 48px;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-weight: bold; font-size: 1.2rem; color: white;
  }

  .btn-glass-danger {
    background: rgba(239, 68, 68, 0.1);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.2);
    transition: all 0.3s ease;
  }
  .btn-glass-danger:hover {
    background: #ef4444;
    color: white;
  }

  /* Select dropdown override */
  select option {
    background: #1a1a1e;
    color: white;
  }
</style>
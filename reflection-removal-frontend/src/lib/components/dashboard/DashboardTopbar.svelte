<svelte:options runes={false} />

<script>
  import LogoutDropdown from '$lib/components/dashboard/LogoutDropdown.svelte';

  export let title = 'Dashboard';
  export let searchValue = '';
  export let searchPlaceholder = '';
  export let uploadLabel = '';
  export let languageLabel = '';
  export let languageOptions = [];
  export let currentLanguage = 'en';
  export let userName = 'User';
  export let userInitial = 'U';
  export let logoutLabel = 'Logout';
  export let onSearch = () => {};
  export let onUpload = () => {};
  export let onLanguageChange = () => {};
  export let onLogout = () => {};
</script>

<header class="gc-topbar">
  <div class="gc-topbar__brand">
    <a href="/" class="gc-topbar__logo" aria-label="GlassClear">
      <span>G</span>
    </a>
    <div>
      <p>GlassClear</p>
      <h1>{title}</h1>
    </div>
  </div>

  <label class="gc-topbar__search">
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" />
      <circle cx="11" cy="11" r="6" stroke="currentColor" stroke-width="1.7" />
    </svg>
    <input
      type="search"
      value={searchValue}
      placeholder={searchPlaceholder}
      oninput={(event) => onSearch(event.currentTarget.value)}
    />
  </label>

  <div class="gc-topbar__actions">
    <button type="button" class="gc-button gc-button--primary" onclick={onUpload}>{uploadLabel}</button>

    <label class="gc-language-switcher">
      <span>{languageLabel}</span>
      <select value={currentLanguage} onchange={(event) => onLanguageChange(event.currentTarget.value)}>
        {#each languageOptions as option}
          <option value={option.code}>{option.label}</option>
        {/each}
      </select>
    </label>

    <LogoutDropdown {userName} {userInitial} {logoutLabel} onLogout={onLogout} />
  </div>
</header>

<svelte:options runes={false} />

<script>
  export let onMenuToggle = () => {};
</script>

<header class="gc-topbar">
  <div class="gc-topbar__left">
    <button class="gc-topbar__menu" type="button" on:click={onMenuToggle} aria-label="Open sidebar">
      <span></span>
      <span></span>
      <span></span>
    </button>

    <label class="gc-search">
      <span class="gc-search__icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="7"></circle>
          <path d="m20 20-3.5-3.5"></path>
        </svg>
      </span>
      <input type="text" placeholder="Search projects, images, exports..." />
    </label>
  </div>

  <div class="gc-topbar__right">
    <div class="gc-status-pill">
      <span class="gc-status-pill__dot"></span>
      AI Engine Online
    </div>

    <div class="gc-user-card gc-glass-card">
      <span class="gc-user-card__name">Misbha</span>
      <span class="gc-user-card__mode">Architect Mode</span>
    </div>
  </div>
</header>

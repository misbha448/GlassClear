<svelte:options runes={false} />

<script>
  export let title = 'Overview';
  export let search = '';
  export let admin = { name: 'Admin', email: '' };
  export let onSearch = () => {};
  export let onRefresh = () => {};
  export let onLogout = () => {};
  export let onOpenMobile = () => {};

  let open = false;

  function handleFocusOut(event) {
    if (!event.currentTarget.contains(event.relatedTarget)) {
      open = false;
    }
  }
</script>

<header class="gc-admin-topbar">
  <div class="gc-admin-topbar__title">
    <button type="button" class="gc-admin-icon-button gc-admin-mobile-trigger" on:click={onOpenMobile} aria-label="Open navigation">=</button>
    <div>
      <span class="gc-admin-eyebrow">Admin</span>
      <h1>{title}</h1>
    </div>
  </div>

  <div class="gc-admin-topbar__actions">
    <label class="gc-admin-search">
      <input type="search" placeholder="Search users or jobs" value={search} on:input={(event) => onSearch(event.currentTarget.value)} />
    </label>
    <button type="button" class="gc-admin-button gc-admin-button--ghost" on:click={onRefresh}>Refresh</button>
    <div class="gc-admin-profile" on:focusout={handleFocusOut}>
      <button type="button" class="gc-admin-profile__trigger" on:click={() => (open = !open)} aria-expanded={open}>
        <span class="gc-admin-profile__avatar">{admin.name?.slice(0, 1) || 'A'}</span>
        <span class="gc-admin-profile__meta">
          <strong>{admin.name}</strong>
          <small>{admin.email}</small>
        </span>
      </button>
      {#if open}
        <div class="gc-admin-profile__menu">
          <button type="button" class="gc-admin-text-button danger" on:click={onLogout}>Logout</button>
        </div>
      {/if}
    </div>
  </div>
</header>

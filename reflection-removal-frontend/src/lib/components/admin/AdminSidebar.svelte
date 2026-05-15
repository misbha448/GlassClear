<svelte:options runes={false} />

<script>
  import { t } from '$lib/state.svelte.js';

  export let items = [];
  export let active = 'overview';
  export let collapsed = false;
  export let mobileOpen = false;
  export let onToggle = () => {};
  export let onSelect = () => {};
  export let onCloseMobile = () => {};
</script>

<aside class={`gc-admin-sidebar ${collapsed ? 'is-collapsed' : ''} ${mobileOpen ? 'is-mobile-open' : ''}`}>
  <div class="gc-admin-sidebar__header">
    <div class="gc-admin-sidebar__brand">
      <span>GC</span>
      {#if !collapsed}
        <div>
          <strong>GlassClear</strong>
          <small>{t('adminUi.dashboard')}</small>
        </div>
      {/if}
    </div>
    <button type="button" class="gc-admin-icon-button gc-admin-sidebar__toggle" on:click={onToggle} aria-label={t('adminUi.toggleSidebar')}>{collapsed ? '>' : '<'}</button>
  </div>

  <nav class="gc-admin-sidebar__nav" aria-label={t('adminUi.sections')}>
    {#each items as item}
      <button
        type="button"
        class={`gc-admin-sidebar__item ${active === item.id ? 'is-active' : ''}`}
        on:click={() => onSelect(item.id)}
        title={item.label}
      >
        <span class="gc-admin-sidebar__item-icon">{item.icon}</span>
        {#if !collapsed}
          <span>{item.label}</span>
        {/if}
      </button>
    {/each}
  </nav>

  <button type="button" class="gc-admin-button gc-admin-button--ghost gc-admin-sidebar__close" on:click={onCloseMobile}>{t('common.close')}</button>
</aside>

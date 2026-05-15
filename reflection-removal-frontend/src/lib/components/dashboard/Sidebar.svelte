<svelte:options runes={false} />

<script>
  import { t } from '$lib/stores/language.js';

  export let items = [];
  export let activeItem = 'command-center';
  export let mobileOpen = false;
  export let onSelect = () => {};
  export let onClose = () => {};

  const iconMap = {
    grid: [
      'M4 4h6v6H4z',
      'M14 4h6v6h-6z',
      'M4 14h6v6H4z',
      'M14 14h6v6h-6z'
    ],
    glass: ['M5 5h14v14H5z', 'M5 12h14', 'M12 5v14'],
    pulse: ['M3 12h4l2-5 4 10 2-5h4'],
    vault: ['M5 8h14v11H5z', 'M8 8V5h8v3', 'M12 12h.01'],
    layers: ['M12 4 20 8 12 12 4 8 12 4', 'M4 12l8 4 8-4', 'M4 16l8 4 8-4'],
    send: ['M4 12 20 4 14 20 11 13 4 12', 'M20 4 11 13'],
    gear: ['M12 8.2a3.8 3.8 0 1 0 0 7.6 3.8 3.8 0 0 0 0-7.6', 'M12 2v3', 'M12 19v3', 'M4.9 4.9l2.1 2.1', 'M17 17l2.1 2.1', 'M2 12h3', 'M19 12h3', 'M4.9 19.1 7 17', 'M17 7l2.1-2.1']
  };
</script>

<aside class:gc-mobile-open={mobileOpen} class="gc-sidebar">
  <div class="gc-sidebar__header">
    <div>
      <div class="gc-sidebar__brand">GlassClear</div>
      <p class="gc-sidebar__tagline">{t('dashboard.aiReflectionStudio')}</p>
    </div>
    <button class="gc-sidebar__close" type="button" on:click={onClose} aria-label={t('common.close')}>
      <span>&times;</span>
    </button>
  </div>

  <nav class="gc-sidebar__nav" aria-label={t('navbar.primaryNavigation')}>
    {#each items as item}
      <button
        type="button"
        class:gc-active={item.id === activeItem}
        class="gc-sidebar__item"
        on:click={() => onSelect(item.id)}
      >
        <span class="gc-sidebar__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            {#each iconMap[item.icon] || [] as segment}
              {#if segment.includes('a')}
                <path d={segment}></path>
              {:else}
                <path d={segment}></path>
              {/if}
            {/each}
          </svg>
        </span>
        <span>{item.label}</span>
      </button>
    {/each}
  </nav>

  <div class="gc-sidebar__footer gc-glass-card">
    <span class="gc-section-kicker">{t('dashboard.systemHealth')}</span>
    <strong>{t('dashboard.online')}</strong>
    <p>{t('dashboard.modelConfidence')}</p>
    <div class="gc-health-bar">
      <span style="width: 96%;"></span>
    </div>
  </div>
</aside>

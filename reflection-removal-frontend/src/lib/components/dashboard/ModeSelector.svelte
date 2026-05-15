<svelte:options runes={false} />

<script>
  export let modes = [];
  export let selectedMode = '';
  export let onSelect = () => {};

  const iconPaths = {
    facade: ['M5 20V8l7-4 7 4v12', 'M9 20v-5h6v5', 'M8 10h.01', 'M12 10h.01', 'M16 10h.01'],
    mirror: ['M7 5h10a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2', 'M9 8h6', 'M9 16h6', 'M8 9v6', 'M16 9v6'],
    interior: ['M4 19h16', 'M6 19V9l6-4 6 4v10', 'M9 19v-5h6v5'],
    building: ['M6 20V4h12v16', 'M9 8h.01', 'M12 8h.01', 'M15 8h.01', 'M9 12h.01', 'M12 12h.01', 'M15 12h.01'],
    window: ['M5 5h14v14H5z', 'M12 5v14', 'M5 12h14'],
    mixed: ['M4 16c3-6 13-6 16 0', 'M6 9h12', 'M8 5h8', 'M12 9v10']
  };
</script>

<section class="gc-panel gc-glass-card">
  <div class="gc-panel__header">
    <div>
      <h3>Recovery Mode Selection</h3>
      <p>Choose the reflection profile that best matches the architectural scene.</p>
    </div>
  </div>

  <div class="gc-mode-grid">
    {#each modes as mode}
      <button
        type="button"
        class:gc-active={selectedMode === mode.id}
        class="gc-mode-card"
        on:click={() => onSelect(mode.id)}
      >
        <span class="gc-mode-card__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            {#each iconPaths[mode.icon] || [] as path}
              <path d={path}></path>
            {/each}
          </svg>
        </span>
        <strong>{mode.title}</strong>
        <p>{mode.description}</p>
      </button>
    {/each}
  </div>
</section>

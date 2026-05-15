<svelte:options runes={false} />

<script>
  export let collapsed = false;
  export let mobileOpen = false;
  export let items = [];
  export let activeItem = 'ai-tools';
  export let onToggleCollapse = () => {};
  export let onSelectItem = () => {};
  export let onCloseMobile = () => {};

  const icons = {
    spark: 'AI',
    slider: 'AD',
    stack: 'BT',
    grid: 'CG',
    clock: 'HS',
    share: 'SH',
    gear: 'ST'
  };
</script>

<aside class:gc-mobile-open={mobileOpen} class:gc-collapsed={collapsed} class="gc-left-rail">
  <div class="gc-left-rail__header">
    <button class="gc-rail-toggle" type="button" aria-label="Collapse sidebar" on:click={onToggleCollapse}>
      {collapsed ? '>' : '<'}
    </button>

    <button class="gc-rail-close" type="button" aria-label="Close tools sidebar" on:click={onCloseMobile}>
      x
    </button>
  </div>

  <nav class="gc-rail-nav" aria-label="Editor sections">
    {#each items as item}
      <button
        type="button"
        class:gc-active={item.id === activeItem}
        class="gc-rail-item"
        title={collapsed ? item.label : ''}
        on:click={() => onSelectItem(item.id)}
      >
        <span class="gc-rail-item__icon">{icons[item.icon]}</span>
        {#if !collapsed}
          <span class="gc-rail-item__label">{item.label}</span>
        {/if}
      </button>
    {/each}
  </nav>
</aside>

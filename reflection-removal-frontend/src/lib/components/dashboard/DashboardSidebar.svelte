<svelte:options runes={false} />

<script>
  export let activeTool = 'remove-reflection';
  export let sidebarCollapsed = false;
  export let onToggleCollapse = () => {};
  export let onSelectTool = () => {};

  const tools = [
    { id: 'remove-reflection', label: 'Remove Reflection', icon: 'AI' },
    { id: 'adjust-image', label: 'Adjust Image', icon: 'FX' },
    { id: 'history', label: 'History', icon: 'HS' },
    { id: 'projects', label: 'Projects', icon: 'PJ' },
    { id: 'share', label: 'Share', icon: 'SH' }
  ];
</script>

<aside class:gc-sidebar--collapsed={sidebarCollapsed} class="gc-sidebar">
  <div class="gc-sidebar__header">
    <div>
      <strong>Tools</strong>
      <p>Editor controls</p>
    </div>
    <button type="button" class="gc-icon-button" onclick={onToggleCollapse}>
      {sidebarCollapsed ? 'Expand' : 'Collapse'}
    </button>
  </div>

  <nav class="gc-sidebar__nav" aria-label="Dashboard tools">
    {#each tools as tool}
      <button
        type="button"
        class:gc-sidebar__item--active={activeTool === tool.id}
        class="gc-sidebar__item"
        onclick={() => onSelectTool(tool.id)}
      >
        <span class="gc-sidebar__icon">{tool.icon}</span>
        <span>{tool.label}</span>
      </button>
    {/each}
  </nav>
</aside>

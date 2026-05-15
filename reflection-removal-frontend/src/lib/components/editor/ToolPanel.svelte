<svelte:options runes={false} />

<script>
  export let collapsed = false;
  export let activeSection = 'ai-tools';
  export let searchQuery = '';
  export let toolGroups = [];
  export let selectedToolId = 'remove-reflection';
  export let panelContent = null;
  export let onSelectTool = () => {};
  export let onRunPanelAction = () => {};

  const icons = {
    spark: 'RF',
    sun: 'GL',
    lens: 'CL',
    shield: 'PD',
    drop: 'CR',
    compare: 'BA',
    grid: 'CM',
    frame: 'CS',
    share: 'SE',
    crop: 'CP',
    expand: 'RS',
    swap: 'FC',
    stamp: 'WM'
  };
</script>

{#if !collapsed}
  <aside class="gc-tool-panel">
    {#if activeSection === 'ai-tools'}
      <div class="gc-tool-panel__header">
        <span>AI Tools</span>
        <strong>{searchQuery ? 'Filtered tools' : 'Editor tools'}</strong>
      </div>

      {#if toolGroups.length}
        {#each toolGroups as group}
          <section class="gc-tool-group">
            <h3>{group.title}</h3>

            <div class="gc-tool-cards">
              {#each group.items as tool}
                <button
                  type="button"
                  class:gc-active={tool.id === selectedToolId}
                  class="gc-tool-card"
                  on:click={() => onSelectTool(tool.id)}
                >
                  <span class="gc-tool-card__icon">{icons[tool.icon]}</span>
                  <div>
                    <strong>{tool.title}</strong>
                    <p>{tool.description}</p>
                  </div>
                </button>
              {/each}
            </div>
          </section>
        {/each}
      {:else}
        <div class="gc-tool-panel__empty">
          <strong>No tools found</strong>
          <p>Try a shorter search term to bring GlassClear tools back into view.</p>
        </div>
      {/if}
    {:else if panelContent}
      <div class="gc-tool-panel__header">
        <span>{panelContent.title}</span>
        <strong>Workspace module</strong>
      </div>

      <div class="gc-tool-panel__summary">
        <p>{panelContent.description}</p>

        <div class="gc-tool-panel__preview">
          {#each panelContent.items as item}
            <span>{item}</span>
          {/each}
        </div>

        <button class="gc-panel-action" type="button" on:click={onRunPanelAction}>
          {panelContent.actionLabel}
        </button>
      </div>
    {/if}
  </aside>
{/if}

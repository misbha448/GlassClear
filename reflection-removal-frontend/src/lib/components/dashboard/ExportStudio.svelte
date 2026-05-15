<svelte:options runes={false} />

<script>
  export let options = [];
  export let selected = [];
  export let onToggle = () => {};
  export let onGenerate = async () => {};
  export let generating = false;
</script>

<section class="gc-panel gc-glass-card">
  <div class="gc-panel__header">
    <div>
      <h3>Client Export Studio</h3>
      <p>Build a premium delivery package for architects and stakeholders.</p>
    </div>
  </div>

  <div class="gc-export-options">
    {#each options as option}
      <button
        type="button"
        class:gc-active={selected.includes(option.id)}
        class="gc-export-option"
        on:click={() => onToggle(option.id)}
      >
        <strong>{option.title}</strong>
        <p>{option.description}</p>
      </button>
    {/each}
  </div>

  <button class="gc-gradient-button" type="button" on:click={onGenerate} disabled={generating}>
    {generating ? 'Generating package...' : 'Generate Delivery Package'}
  </button>
</section>

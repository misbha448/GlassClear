<svelte:options runes={false} />

<script>
  export let items = [];
  export let selectedId = '';
  export let onSelect = () => {};
</script>

<section class="gc-history-strip">
  <div class="gc-history-strip__header">
    <strong>Recent Edits</strong>
    <span>Versions and saved project checkpoints</span>
  </div>

  <div class="gc-history-strip__cards">
    {#each items as item}
      <button
        type="button"
        class:gc-active={item.id === selectedId}
        class="gc-history-card"
        on:click={() => onSelect(item.id)}
      >
        <img src={item.image} alt={item.label} />
        <div>
          <strong>{item.label}</strong>
          <span>{item.time}</span>
        </div>
      </button>
    {/each}
  </div>
</section>

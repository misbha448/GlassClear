<svelte:options runes={false} />

<script>
  export let items = [];
  export let selectedId = '';
  export let onSelect = () => {};
</script>

<section class="gc-history-strip">
  <div class="gc-history-strip__label">
    <strong>History</strong>
    <p>Session versions</p>
  </div>

  <div class="gc-history-strip__items">
    {#each items as item}
      <button
        type="button"
        class:gc-history-strip__item--active={selectedId === item.id}
        class="gc-history-strip__item"
        onclick={() => onSelect(item)}
      >
        <img src={item.thumbnail} alt={item.label} />
        <span>{item.label}</span>
      </button>
    {/each}
  </div>
</section>

<svelte:options runes={false} />

<script>
  export let queue = [];
  export let hover = false;
  export let onHoverChange = () => {};
</script>

<section class:gc-dragging={hover} class="gc-panel gc-glass-card">
  <div class="gc-panel__header">
    <div>
      <h3>Batch Reflection Recovery</h3>
      <p>Process multiple architectural images together.</p>
    </div>
  </div>

  <div
    class="gc-dropzone"
    role="button"
    tabindex="0"
    aria-label="Batch upload dropzone"
    on:dragenter={() => onHoverChange(true)}
    on:dragleave={() => onHoverChange(false)}
    on:dragover|preventDefault={() => onHoverChange(true)}
    on:drop|preventDefault={() => onHoverChange(false)}
  >
    <span class="gc-dropzone__icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 4v12"></path>
        <path d="m7 11 5 5 5-5"></path>
        <path d="M5 20h14"></path>
      </svg>
    </span>
    <strong>Drop project frames here</strong>
    <p>Mock queue ready for future FastAPI batch upload integration.</p>
  </div>

  <div class="gc-batch-list">
    {#each queue as item}
      <div class="gc-batch-row">
        <span>{item.name}</span>
        <em class={`gc-batch-row__status gc-batch-row__status--${item.tone}`}>{item.status}</em>
      </div>
    {/each}
  </div>
</section>

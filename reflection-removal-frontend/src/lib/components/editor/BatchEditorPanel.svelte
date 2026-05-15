<svelte:options runes={false} />

<script>
  export let open = false;
  export let queue = [];
  export let selectedFiles = [];
  export let running = false;
  export let infoMessage = '';
  export let onFilesSelected = () => {};
  export let onStart = () => {};
  export let onClose = () => {};
</script>

<aside class:gc-open={open} class="gc-batch-panel">
  <div class="gc-batch-panel__header">
    <div>
      <span>Batch Editor</span>
      <h2>Queue up to 50 images</h2>
    </div>
    <button type="button" class="gc-modal__close" aria-label="Close batch panel" on:click={onClose}>x</button>
  </div>

  <div class="gc-batch-panel__dropzone">
    <strong>Drop architectural image sets here</strong>
    <p>Files are uploaded to your real batch queue and processed with the current reflection pipeline.</p>
    <input type="file" multiple accept="image/*" on:change={(event) => onFilesSelected(Array.from(event.currentTarget.files || []))} />
  </div>

  {#if selectedFiles.length}
    <div class="gc-batch-panel__selected">
      {#each selectedFiles as file}
        <span title={file}>{file}</span>
      {/each}
    </div>
  {/if}

  {#if infoMessage}
    <p class="gc-batch-panel__message">{infoMessage}</p>
  {/if}

  <button type="button" class="gc-primary-action" on:click={onStart} disabled={running}>
    {running ? 'Processing batch...' : 'Start Batch Processing'}
  </button>

  <div class="gc-batch-panel__list">
    {#each queue as item}
      <div class={`gc-batch-panel__row gc-batch-panel__row--${item.tone}`}>
        <span>{item.name}</span>
        <strong>{item.status}</strong>
      </div>
    {/each}
  </div>
</aside>

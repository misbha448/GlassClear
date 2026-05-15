<svelte:options runes={false} />

<script>
  export let shareLink = '';
  export let shareStatus = '';
  export let hasProcessedImage = false;
  export let onCopyShareLink = () => {};
  export let onDownloadComparison = () => {};
  export let onOpenClientPreview = () => {};
</script>

<div class="gc-panel-stack">
  <div class="gc-setting-card">
    <div class="gc-setting-card__header">
      <div>
        <strong>Share Result</strong>
        <p>{shareStatus}</p>
      </div>
    </div>

    <button type="button" class="gc-button gc-button--primary" onclick={onCopyShareLink}>Copy Share Link</button>
    <button type="button" class="gc-button gc-button--ghost" onclick={onDownloadComparison}>Download Comparison Image</button>
    <button type="button" class="gc-button gc-button--ghost" onclick={onOpenClientPreview}>Client Preview</button>

    {#if shareLink}
      <div class="gc-link-preview">{shareLink}</div>
    {/if}

    {#if !hasProcessedImage}
      <div class="gc-panel-empty">Generate a processed result to unlock sharing actions.</div>
    {/if}
  </div>
</div>

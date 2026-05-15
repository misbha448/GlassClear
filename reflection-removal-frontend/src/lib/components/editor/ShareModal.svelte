<svelte:options runes={false} />

<script>
  export let open = false;
  export let shareLink = '';
  export let shareImagePreview = '';
  export let statusMessage = '';
  export let disabled = false;
  export let onCopyLink = () => {};
  export let onDownloadImage = () => {};
  export let onClientPreview = () => {};
  export let onShareProject = () => {};
  export let onCopyExistingLink = () => {};
  export let onClose = () => {};
</script>

{#if open}
  <div class="gc-modal-backdrop" role="presentation" on:click={onClose}>
    <div
      class="gc-modal gc-modal--share"
      role="dialog"
      aria-modal="true"
      aria-label="Share center"
      tabindex="-1"
      on:click|stopPropagation
      on:keydown|stopPropagation
    >
      <div class="gc-modal__header">
        <div>
          <span>Share Center</span>
          <h2>Share Your GlassClear Result</h2>
          <p>Copy a client link, generate a share image, or move the current result into a project workflow.</p>
        </div>
        <button type="button" class="gc-modal__close" aria-label="Close share center" on:click={onClose}>x</button>
      </div>

      <div class="gc-share-actions">
        <button type="button" class="gc-primary-action" on:click={onCopyLink} disabled={disabled}>
          Copy Share Link
        </button>
        <button type="button" class="gc-secondary-action" on:click={onDownloadImage} disabled={disabled}>
          Download Share Image
        </button>
        <button type="button" class="gc-secondary-action" on:click={onClientPreview} disabled={disabled}>
          Client Preview
        </button>
        <button type="button" class="gc-secondary-action" on:click={onShareProject} disabled={disabled}>
          Share as Project
        </button>
      </div>

      <section class="gc-modal-card">
        <div class="gc-modal-card__head">
          <strong>Share link</strong>
          {#if shareLink}
            <button type="button" class="gc-mini-button" on:click={onCopyExistingLink}>Copy</button>
          {/if}
        </div>

        <div class="gc-share-link-row">
          <input
            class="gc-share-link-input"
            type="text"
            readonly
            value={shareLink || 'Create a share link to enable client preview.'}
          />
        </div>
      </section>

      <section class="gc-modal-card">
        <div class="gc-modal-card__head">
          <strong>Client preview image</strong>
        </div>

        {#if shareImagePreview}
          <div class="gc-modal-preview">
            <img src={shareImagePreview} alt="Share preview poster" />
          </div>
        {:else}
          <div class="gc-modal-placeholder">
            <strong>Share poster preview</strong>
            <p>Download Share Image generates a polished original-vs-output poster locally.</p>
          </div>
        {/if}
      </section>

      {#if statusMessage}
        <p class="gc-modal-note">{statusMessage}</p>
      {/if}
    </div>
  </div>
{/if}

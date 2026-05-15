<svelte:options runes={false} />

<script>
  import { getDisplayName } from '$lib/utils/displayName.js';

  export let open = false;
  export let item = null;
  export let shareLink = '';
  export let busy = false;
  export let labels = {};
  export let onClose = () => {};
  export let onCopyLink = async () => {};
  export let onPreview = async () => {};
  export let onDownloadComparison = async () => {};
  export let onWhatsApp = async () => {};
</script>

{#if open && item}
  <div class="gc-modal-backdrop" role="presentation" onclick={onClose}>
    <div class="gc-modal-card" role="dialog" aria-modal="true" aria-label={labels.title} tabindex="-1" onclick={(event) => event.stopPropagation()} onkeydown={(event) => event.stopPropagation()}>
      <div class="gc-modal-header">
        <div>
          <p class="gc-modal-kicker">{labels.kicker}</p>
          <h2>{labels.title}</h2>
          <p>{getDisplayName(item)}</p>
        </div>
        <button type="button" class="gc-button gc-button--ghost gc-button--small" onclick={onClose}>{labels.close}</button>
      </div>

      {#if shareLink}
        <label class="gc-share-link gc-share-link--modal">
          <span>{labels.linkLabel}</span>
          <input type="text" readonly value={shareLink} />
        </label>
      {/if}

      <div class="gc-action-grid">
        <button type="button" class="gc-action-card" onclick={onCopyLink} disabled={busy}>
          <strong>{labels.copyLink}</strong>
          <p>{labels.copyLinkHelp}</p>
        </button>
        <button type="button" class="gc-action-card" onclick={onPreview} disabled={busy}>
          <strong>{labels.clientPreview}</strong>
          <p>{labels.clientPreviewHelp}</p>
        </button>
        <button type="button" class="gc-action-card" onclick={onDownloadComparison} disabled={busy}>
          <strong>{labels.downloadComparison}</strong>
          <p>{labels.downloadComparisonHelp}</p>
        </button>
        <button type="button" class="gc-action-card" onclick={onWhatsApp} disabled={busy}>
          <strong>{labels.whatsApp}</strong>
          <p>{labels.whatsAppHelp}</p>
        </button>
      </div>
    </div>
  </div>
{/if}

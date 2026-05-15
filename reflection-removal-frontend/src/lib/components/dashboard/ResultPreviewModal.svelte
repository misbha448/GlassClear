<svelte:options runes={false} />

<script>
  import StatusBadge from '$lib/components/dashboard/StatusBadge.svelte';
  import { getDisplayName } from '$lib/utils/displayName.js';

  export let open = false;
  export let item = null;
  export let labels = {};
  export let onClose = () => {};
  export let onExport = () => {};
  export let onShare = () => {};
</script>

{#if open && item}
  <div
    class="gc-preview-backdrop"
    role="presentation"
    onclick={onClose}
    onkeydown={(event) => event.key === 'Escape' && onClose()}
  >
    <div class="gc-preview-modal" role="dialog" aria-modal="true" tabindex="-1" onclick={(event) => event.stopPropagation()} onkeydown={() => {}}>
      <div class="gc-card__header gc-card__header--compact">
        <div>
          <h2>{labels.title || 'Result Preview'}</h2>
          <p>{getDisplayName(item)}</p>
        </div>
        <button type="button" class="gc-button gc-button--ghost" onclick={onClose}>
          {labels.close || 'Close'}
        </button>
      </div>

      <div class="gc-latest-result__meta gc-preview-meta">
        <StatusBadge status={item.status || 'completed'} />
        <span>{item.processedAtLabel}</span>
      </div>

      <div class="gc-share-center__preview">
        <figure>
          <img src={item.originalUrl} alt={labels.original || 'Original'} />
          <figcaption>{labels.original || 'Original'}</figcaption>
        </figure>
        <figure>
          <img src={item.processedUrl} alt={labels.output || 'Output'} />
          <figcaption>{labels.output || 'Output'}</figcaption>
        </figure>
      </div>

      <div class="gc-result-actions gc-preview-actions">
        <button type="button" class="gc-button gc-button--primary" onclick={() => onExport(item)}>
          {labels.export || 'Export'}
        </button>
        <button type="button" class="gc-button gc-button--secondary" onclick={() => onShare(item)}>
          {labels.share || 'Share'}
        </button>
      </div>
    </div>
  </div>
{/if}

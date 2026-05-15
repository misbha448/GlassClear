<svelte:options runes={false} />

<script>
  import EmptyState from '$lib/components/dashboard/EmptyState.svelte';
  import { getDisplayName } from '$lib/utils/displayName.js';

  export let item = null;
  export let shareLink = '';
  export let labels = {};
  export let onOpenShareModal = () => {};
  export let disabled = false;
  export let helperMessage = '';
</script>

<section class="gc-card">
  <div class="gc-card__header">
    <div>
      <h2>{labels.title}</h2>
      <p>{labels.subtitle}</p>
    </div>
  </div>

  {#if item}
    <div class="gc-share-center">
      <div class="gc-share-center__heading">
        <h3>{getDisplayName(item)}</h3>
      </div>
      <div class="gc-share-center__preview">
        <figure>
          <img src={item.originalUrl} alt={labels.original} />
          <figcaption>{labels.original}</figcaption>
        </figure>
        <figure>
          <img src={item.processedUrl} alt={labels.output} />
          <figcaption>{labels.output}</figcaption>
        </figure>
      </div>

      <p class="gc-panel-note">{labels.description}</p>

      <div class="gc-share-center__actions">
        <button type="button" class="gc-button gc-button--primary" onclick={() => onOpenShareModal(item)} disabled={disabled}>
          {labels.openShareModal}
        </button>
      </div>

      {#if helperMessage}
        <p class="gc-inline-message">{helperMessage}</p>
      {/if}

      {#if shareLink}
        <label class="gc-share-link">
          <span>{labels.publicShareUrl || 'Public share URL'}</span>
          <input type="text" readonly value={shareLink} />
        </label>
      {/if}
    </div>
  {:else}
    <EmptyState title={labels.emptyTitle} message={labels.emptyMessage} />
  {/if}
</section>

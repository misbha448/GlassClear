<svelte:options runes={false} />

<script>
  import EmptyState from '$lib/components/dashboard/EmptyState.svelte';
  import { t } from '$lib/state.svelte.js';

  export let latestResult = null;
  export let latestResultLabel = '';
  export let helperMessage = '';
  export let canGenerate = false;
  export let canDownload = false;
  export let generating = false;
  export let downloading = false;
  export let onGenerate = async () => {};
  export let onDownload = async () => {};
</script>

<section class="gc-card gc-delivery-pack">
  <div class="gc-card__header">
    <div>
      <h2>{t('delivery.title')}</h2>
      <p>{t('delivery.subtitle')}</p>
    </div>
  </div>

  {#if latestResult}
    <div class="gc-delivery-pack__body">
      <div class="gc-delivery-pack__summary">
        <span class="gc-delivery-pack__eyebrow">{t('delivery.latestCompleted')}</span>
        <h3>{latestResult.title || latestResult.filename}</h3>
        <p>{latestResultLabel}</p>
        {#if helperMessage}
          <p class="gc-delivery-pack__helper">{helperMessage}</p>
        {/if}
      </div>

      <div class="gc-delivery-pack__actions">
        <button type="button" class="gc-button gc-button--primary" onclick={onGenerate} disabled={!canGenerate || generating}>
          {generating ? t('delivery.generating') : t('delivery.generate')}
        </button>
        <button type="button" class="gc-button gc-button--ghost" onclick={onDownload} disabled={!canDownload || downloading}>
          {downloading ? t('delivery.downloading') : t('delivery.download')}
        </button>
      </div>
    </div>
  {:else}
    <EmptyState title={t('delivery.title')} message={t('delivery.emptyMessage')} />
  {/if}
</section>

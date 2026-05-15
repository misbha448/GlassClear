<svelte:options runes={false} />

<script>
  import EmptyState from '$lib/components/dashboard/EmptyState.svelte';
  import StatusBadge from '$lib/components/dashboard/StatusBadge.svelte';
  import { t } from '$lib/stores/language.js';
  import { getDisplayName } from '$lib/utils/displayName.js';

  export let item = null;
  export let labels = {};
  export let hasImage = false;
  export let onView = () => {};
  export let onExport = () => {};
  export let onUpload = () => {};
  export let helperMessage = '';
  export let disableView = false;
  export let disableExport = false;
</script>

<section class="gc-card gc-latest-result">
  <div class="gc-card__header">
    <div>
      <h2>{labels.title}</h2>
      <p>{labels.subtitle}</p>
    </div>
    {#if item}
      <div class="gc-latest-result__meta">
        <StatusBadge status={item.status || 'ready'} />
        <span>{item.processedAtLabel}</span>
      </div>
    {/if}
  </div>

  {#if hasImage && item}
    <div class="gc-latest-result__body">
      <div class="gc-result-frame">
        <figure>
          <img src={item.originalUrl} alt={`${labels.original} ${item.filename}`} />
          <figcaption>{labels.original}</figcaption>
        </figure>
        {#if item.processedUrl}
          <figure>
            <img src={item.processedUrl} alt={`${labels.output} ${item.filename}`} />
            <figcaption>{labels.output}</figcaption>
          </figure>
        {:else}
          <figure class="gc-result-frame__placeholder">
            <div class="gc-result-frame__status">
              <StatusBadge status={item.status || 'queued'} />
              <strong>{labels.output}</strong>
              <p>{t('dashboard.previewPending')}</p>
            </div>
            <figcaption>{labels.output}</figcaption>
          </figure>
        {/if}
      </div>

      <div class="gc-latest-result__details">
        <div class="gc-result-copy">
          <p>{labels.beforeAfter}</p>
          <h3>{getDisplayName(item)}</h3>
          {#if getDisplayName(item) !== item.filename}
            <p class="gc-helper-message gc-helper-message--filename">{item.filename}</p>
          {/if}
          {#if helperMessage}
            <p class="gc-helper-message">{helperMessage}</p>
          {/if}
          <dl>
            <div>
              <dt>{labels.processedOn}</dt>
              <dd>{item.processedAtLabel}</dd>
            </div>
            <div>
              <dt>{labels.status}</dt>
              <dd><StatusBadge status={item.status || 'ready'} /></dd>
            </div>
          </dl>
        </div>

        <div class="gc-result-actions">
          <button type="button" class="gc-button gc-button--soft" onclick={onView} disabled={disableView}>{labels.viewResult}</button>
          <button type="button" class="gc-button gc-button--primary" onclick={onExport} disabled={disableExport}>{labels.exportResult}</button>
        </div>
      </div>
    </div>
  {:else}
    <EmptyState title={labels.emptyTitle} message={labels.emptyMessage} actionLabel={labels.uploadImage} onAction={onUpload} />
  {/if}
</section>

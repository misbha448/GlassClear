<svelte:options runes={false} />

<script>
  import EmptyState from '$lib/components/dashboard/EmptyState.svelte';
  import StatusBadge from '$lib/components/dashboard/StatusBadge.svelte';

  export let queue = [];
  export let summary = '';
  export let notice = '';
  export let labels = {};
  export let onPickFiles = () => {};
  export let onStart = () => {};
  export let onClear = () => {};
  export let onDownloadZip = () => {};
  export let disablePick = false;
  export let disableStart = false;
  export let disableClear = false;
  export let disableDownload = false;
  export let overallProgress = 0;
</script>

<section class="gc-card">
  <div class="gc-card__header">
    <div>
      <h2>{labels.title}</h2>
      <p>{labels.subtitle}</p>
    </div>
    <span class="gc-panel-caption">{summary}</span>
  </div>

  <div class="gc-batch-actions">
    <button type="button" class="gc-button gc-button--soft" onclick={onPickFiles} disabled={disablePick}>{labels.addImages}</button>
    <button type="button" class="gc-button gc-button--primary" onclick={onStart} disabled={disableStart}>{labels.startBatch}</button>
    <button type="button" class="gc-button gc-button--ghost" onclick={onClear} disabled={disableClear}>{labels.clearQueue}</button>
    <button type="button" class="gc-button gc-button--secondary" onclick={onDownloadZip} disabled={disableDownload}>{labels.downloadZip}</button>
  </div>

  <p class="gc-panel-note">{labels.uploadHint}</p>

  {#if notice}
    <p class="gc-inline-message">{notice}</p>
  {/if}

  {#if queue.length}
    <div class="gc-progress">
      <div class="gc-progress__bar" style={`width:${overallProgress}%`}></div>
    </div>
    <p class="gc-panel-note">{labels.progressLabel}: {overallProgress}%</p>

    <div class="gc-batch-list">
      {#each queue as item}
        <div class="gc-batch-item">
          <div class="gc-batch-item__main">
            <strong>{item.name}</strong>
            <StatusBadge status={item.status} />
          </div>
          <div class="gc-progress">
            <div class="gc-progress__bar" style={`width:${item.progress || 0}%`}></div>
          </div>
          <span>{item.progress || 0}%</span>
          {#if item.error_message}
            <p class="gc-inline-message">{item.error_message}</p>
          {/if}
        </div>
      {/each}
    </div>
  {:else}
    <EmptyState title={labels.emptyTitle} message={labels.emptyMessage} />
  {/if}
</section>

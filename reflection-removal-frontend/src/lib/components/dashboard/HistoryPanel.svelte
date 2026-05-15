<svelte:options runes={false} />

<script>
  import EmptyState from '$lib/components/dashboard/EmptyState.svelte';
  import StatusBadge from '$lib/components/dashboard/StatusBadge.svelte';
  import { getDisplayName } from '$lib/utils/displayName.js';

  export let items = [];
  export let labels = {};
  export let onView = () => {};
  export let onExport = () => {};
  export let onDelete = () => {};
  export let onViewAll = () => {};
  export let showViewAll = false;
  export let variant = 'list';
</script>

<section class="gc-card">
  <div class="gc-card__header">
    <div>
      <h2>{labels.title}</h2>
      <p>{labels.subtitle}</p>
    </div>
    {#if showViewAll}
      <button type="button" class="gc-button gc-button--ghost gc-button--small" onclick={onViewAll}>
        {labels.viewAll}
      </button>
    {/if}
  </div>

  {#if items.length}
    <div class={variant === 'grid' ? 'gc-history-grid' : variant === 'preview' ? 'gc-history-preview-grid' : 'gc-history-list'}>
      {#each items as item}
        <article class={`gc-history-item ${variant === 'grid' ? 'gc-history-item--card' : ''} ${variant === 'preview' ? 'gc-history-item--preview' : ''}`}>
          <img src={item.thumbnail} alt={getDisplayName(item)} class="gc-history-item__thumb" />
          <div class="gc-history-item__copy">
            <h3>{getDisplayName(item)}</h3>
            {#if getDisplayName(item) !== item.filename}
              <p class="gc-history-item__filename">{item.filename}</p>
            {/if}
            <p>{item.processedAtLabel}</p>
            <StatusBadge status={item.status || 'completed'} />
          </div>
          <div class="gc-history-item__actions">
            <button type="button" class="gc-link-button" onclick={() => onView(item)}>{labels.view}</button>
            <button type="button" class="gc-link-button" onclick={() => onExport(item)}>{labels.export}</button>
            <button type="button" class="gc-link-button gc-link-button--danger" onclick={() => onDelete(item)}>{labels.delete}</button>
          </div>
        </article>
      {/each}
    </div>
  {:else}
    <EmptyState title={labels.emptyTitle} message={labels.emptyMessage} />
  {/if}
</section>

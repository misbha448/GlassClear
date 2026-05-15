<svelte:options runes={false} />

<script>
  import EmptyState from '$lib/components/dashboard/EmptyState.svelte';
  import { t } from '$lib/state.svelte.js';

  export let collections = [];
  export let showViewAll = false;
  export let creating = false;
  export let addingLatest = false;
  export let latestResultAvailable = false;
  export let onCreate = async () => {};
  export let onAddLatest = async () => {};
  export let onAddLatestToCollection = async () => {};
  export let onOpenCollection = () => {};
  export let onViewAll = () => {};

  function formatUpdated(value) {
    if (!value) return t('common.updatedRecently');
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return t('common.updatedRecently');
    return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
  }
</script>

<section class="gc-card gc-collections-panel">
  <div class="gc-card__header">
    <div>
      <h2>{t('collections.title')}</h2>
      <p>{t('collections.subtitle')}</p>
    </div>
    <div class="gc-collections-panel__toolbar">
      <button type="button" class="gc-button gc-button--ghost gc-button--small" onclick={onCreate} disabled={creating}>
        {creating ? t('collections.creating') : t('collections.newCollection')}
      </button>
      {#if showViewAll}
        <button type="button" class="gc-button gc-button--ghost gc-button--small" onclick={onViewAll}>
          {t('collections.viewAll')}
        </button>
      {/if}
    </div>
  </div>

  <div class="gc-collections-panel__quick-actions">
    <button type="button" class="gc-button gc-button--soft" onclick={onAddLatest} disabled={!latestResultAvailable || addingLatest}>
      {addingLatest ? t('collections.addingLatest') : t('collections.addLatest')}
    </button>
  </div>
  {#if !latestResultAvailable}
    <p class="gc-helper-message">{t('collections.processBeforeAdd')}</p>
  {/if}

  {#if collections.length}
    <div class="gc-album-grid gc-collections-grid">
      {#each collections as collection}
        <article class="gc-album-card gc-collection-card">
          <div class="gc-album-cover">
            {#if collection.cover_url}
              <img src={collection.cover_url} alt={collection.name} />
            {:else}
              <div class="gc-album-cover__fallback" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3.5 7.5a2 2 0 0 1 2-2h4l1.5 2h7.5a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2z"></path>
                </svg>
              </div>
            {/if}
          </div>

          <div class="gc-album-card__body">
            <div class="gc-album-card__meta">
              <span>{t('common.imagesCount', { count: collection.count })}</span>
              <span>{t('common.updated')}: {formatUpdated(collection.updated_at)}</span>
            </div>
            <h3>{collection.name}</h3>
            <p>{t('collections.cardDescription')}</p>
            <div class="gc-collections-panel__card-actions">
              <button
                type="button"
                class="gc-button gc-button--soft gc-button--small"
                onclick={() => onAddLatestToCollection(collection.id)}
                disabled={!latestResultAvailable || addingLatest}
              >
                {addingLatest ? t('collections.adding') : t('collections.addLatestShort')}
              </button>
              <button type="button" class="gc-button gc-button--primary" onclick={() => onOpenCollection(collection.id)}>
                {t('common.open')}
              </button>
            </div>
          </div>
        </article>
      {/each}
    </div>
  {:else}
    <EmptyState title={t('collections.title')} message={t('collections.emptyMessage')} />
  {/if}
</section>

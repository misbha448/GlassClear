<svelte:options runes={false} />

<script>
  import EmptyState from '$lib/components/dashboard/EmptyState.svelte';

  export let albums = [];
  export let labels = {};
  export let onViewAlbum = () => {};
  export let onViewAll = () => {};
  export let showViewAll = false;

  function formatUpdated(value) {
    if (!value) return labels.justNow;
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return labels.justNow;
    return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
  }
</script>

<section class="gc-card gc-albums-panel">
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

  {#if albums.length}
    <div class="gc-album-grid gc-album-grid--premium">
      {#each albums as album}
        <article class="gc-album-card gc-album-card--premium">
          <div class="gc-album-cover">
            {#if album.cover_url}
              <img src={album.cover_url} alt={album.name} />
            {:else}
              <div class="gc-album-cover__fallback" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3.5" y="5" width="17" height="14" rx="2.5"></rect>
                  <path d="M7.5 14.5l2.5-2.5 2.5 2.5 4-4 2 2"></path>
                  <circle cx="9" cy="9" r="1.25"></circle>
                </svg>
              </div>
            {/if}
          </div>

          <div class="gc-album-card__body">
            <div class="gc-album-card__meta">
              <span>{album.count} {labels.imagesLabel}</span>
              <span>{labels.updatedLabel}: {formatUpdated(album.updated_at)}</span>
            </div>
            <h3>{album.name}</h3>
            <p>{album.description}</p>
            <button type="button" class="gc-button gc-button--primary" onclick={() => onViewAlbum(album.slug)}>
              {labels.viewAlbum}
            </button>
          </div>
        </article>
      {/each}
    </div>
  {:else}
    <EmptyState title={labels.emptyTitle} message={labels.emptyMessage} />
  {/if}
</section>

<svelte:options runes={false} />

<script>
  import '../../../../styles/dashboard.css';

  import { goto } from '$app/navigation';
  import { onDestroy, onMount } from 'svelte';
  import outputAsset from '$lib/assets/output.jpg';
  import DashboardTopbar from '$lib/components/dashboard/DashboardTopbar.svelte';
  import EmptyState from '$lib/components/dashboard/EmptyState.svelte';
  import ExportResultModal from '$lib/components/dashboard/ExportResultModal.svelte';
  import StatusBadge from '$lib/components/dashboard/StatusBadge.svelte';
  import Toast from '$lib/components/dashboard/Toast.svelte';
  import { LANGUAGE_OPTIONS, language, setLanguage, t } from '$lib/stores/language.js';
  import { downloadExportVariant, getAlbum, getCurrentUser, getHistory, withBase } from '$lib/api/dashboardApi.js';
  import { clearPendingGuestImage } from '$lib/utils/pendingGuestImage.js';
  import { getDisplayName as getResultDisplayName } from '$lib/utils/displayName.js';
  import { getDisplayName, getUserInitial } from '$lib/utils/userDisplay.js';
  import { getStoredToken } from '$lib/api/api.js';

  export let data;

  const AUTH_STORAGE_KEYS = ['token', 'token_type', 'role', 'user_name', 'authToken', 'access_token', 'refresh_token'];
  const ALBUM_CACHE_SESSION_KEY = 'glassclear-albums-cache';
  const SELECTED_ALBUM_SESSION_KEY = 'glassclear-selected-album';

  let currentLanguage = 'en';
  let currentUser = null;
  let searchQuery = '';
  let album = null;
  let loaded = false;
  let albumNotFound = false;
  let loadError = '';
  let toast = null;
  let toastTimer;
  let exportModalOpen = false;
  let exportModalItem = null;
  let exportModalBusy = false;
  let labels = {};

  $: activeLanguage = $language;
  $: currentLanguage = activeLanguage;
  $: filteredItems = (album?.items || []).filter((item) => {
    if (!searchQuery) return true;
    const query = searchQuery.toLowerCase();
    return `${item.filename} ${item.title || ''} ${item.status || ''}`.toLowerCase().includes(query);
  });

  $: {
    activeLanguage;
    labels = {
      albumsTitle: t('albums.title'),
      backToAlbums: t('albums.viewAll'),
      language: t('common.language'),
      logout: t('common.logout'),
      searchPlaceholder: t('common.searchFilenameOrStatus'),
      imagesLabel: t('albums.imagesLabel'),
      updatedLabel: t('albums.updatedLabel'),
      emptyTitle: t('albums.emptyAlbumTitle'),
      emptyMessage: t('common.noImagesInAlbumYet'),
      notFoundTitle: t('albums.notFoundTitle'),
      notFoundMessage: t('albums.notFoundMessage'),
      noMatchingImages: t('albums.noMatchingImages'),
      searchHelp: t('albums.searchHelp'),
      smartAlbumLabel: t('albums.smartAlbumLabel'),
      viewResult: t('dashboard.viewResult'),
      export: t('common.export'),
      filename: t('resultDetail.fileName'),
      status: t('common.status'),
      exportModal: {
        kicker: t('exportModal.kicker'),
        title: t('exportModal.title'),
        close: t('common.close'),
        jpg: t('exportModal.jpg'),
        jpgHelp: t('exportModal.jpgHelp'),
        png: t('exportModal.png'),
        pngHelp: t('exportModal.pngHelp'),
        hd: t('exportModal.hd'),
        hdHelp: t('exportModal.hdHelp'),
        comparison: t('exportModal.comparison'),
        comparisonHelp: t('exportModal.comparisonHelp')
      }
    };
  }

  function showToast(type, message) {
    toast = { type, message };
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (toast = null), 3200);
  }

  function normalizeUrl(url) {
    if (!url) return '';
    if (url.startsWith('http')) return url;
    return withBase(url) || url;
  }

  function formatDate(value) {
    if (!value) return t('albums.justNow');
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return t('albums.justNow');
    return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
  }

  function mapItem(source = {}) {
    return {
      id: source.id,
      imageId: source.id,
      filename: source.filename || t('resultDetail.title'),
      title: source.display_name || null,
      thumbnail: normalizeUrl(source.thumbnail_url || source.processed_url || source.original_url),
      originalUrl: normalizeUrl(source.original_url),
      processedUrl: normalizeUrl(source.processed_url),
      date: formatDate(source.updated_at || source.created_at),
      status: (source.status || 'completed').toLowerCase()
    };
  }

  function readAlbumCache() {
    if (typeof sessionStorage === 'undefined') return [];
    try {
      const payload = JSON.parse(sessionStorage.getItem(ALBUM_CACHE_SESSION_KEY) || '[]');
      return Array.isArray(payload) ? payload : [];
    } catch {
      return [];
    }
  }

  function readSelectedAlbum() {
    if (typeof sessionStorage === 'undefined') return null;
    try {
      const payload = JSON.parse(sessionStorage.getItem(SELECTED_ALBUM_SESSION_KEY) || 'null');
      return payload && typeof payload === 'object' ? payload : null;
    } catch {
      return null;
    }
  }

  function normalizeAlbumSlug(value) {
    return String(value || '')
      .trim()
      .toLowerCase()
      .replace(/[_\s]+/g, '-')
      .replace(/[^a-z0-9-]+/g, '')
      .replace(/-{2,}/g, '-')
      .replace(/^-|-$/g, '');
  }

  function resolveHistoryAlbumSlug(source = {}) {
    return normalizeAlbumSlug(
      source.category_slug ||
      source.album_slug ||
      source.category ||
      source.album ||
      source.group
    );
  }

  function buildAlbumFallbackItem(payload = {}) {
    const cachedAlbum = readAlbumCache().find((item) => item?.slug === payload.slug);
    return {
      id: `album-preview-${payload.slug || 'unknown'}`,
      imageId: null,
      filename: payload.name || t('resultDetail.title'),
      title: `${payload.name || 'Album'} Preview`,
      thumbnail: normalizeUrl(cachedAlbum?.cover_url) || outputAsset,
      originalUrl: '',
      processedUrl: normalizeUrl(cachedAlbum?.cover_url) || outputAsset,
      date: formatDate(payload.updated_at),
      status: 'completed',
      isPreview: true
    };
  }

  async function loadAlbum() {
    searchQuery = '';
    const payload = await getAlbum(data.albumSlug);
    const selectedAlbum = readSelectedAlbum();
    const requestedSlug = normalizeAlbumSlug(payload.slug || data.albumSlug);
    const cachedAlbum = readAlbumCache().find((item) => normalizeAlbumSlug(item?.slug) === requestedSlug);
    const fallbackAlbum =
      (normalizeAlbumSlug(selectedAlbum?.slug) === requestedSlug ? selectedAlbum : null) ||
      cachedAlbum;
    let mappedItems = Array.isArray(payload.items) ? payload.items.map(mapItem) : [];
    const resolvedSlug = payload.slug || fallbackAlbum?.slug || data.albumSlug;

    if (!mappedItems.length) {
      try {
        const historyPayload = await getHistory({ limit: 100 });
        const historyItems = Array.isArray(historyPayload?.items) ? historyPayload.items : [];
        mappedItems = historyItems
          .filter((item) => resolveHistoryAlbumSlug(item) === normalizeAlbumSlug(resolvedSlug))
          .map(mapItem);
      } catch {
        mappedItems = [];
      }
    }

    const resolvedName = payload.name || fallbackAlbum?.name || t('albums.title');
    const resolvedDescription = payload.description || fallbackAlbum?.description || '';
    const resolvedCount = Number(payload.count || fallbackAlbum?.count || mappedItems.length || 0);
    const resolvedUpdatedAt = payload.updated_at || fallbackAlbum?.updated_at || mappedItems[0]?.date || null;
    album = {
      slug: resolvedSlug,
      name: resolvedName,
      description: resolvedDescription,
      count: Math.max(resolvedCount, mappedItems.length),
      updatedAt: resolvedUpdatedAt,
      items:
        mappedItems.length || (!resolvedCount && !fallbackAlbum?.cover_url)
          ? mappedItems
          : [buildAlbumFallbackItem({ ...payload, slug: resolvedSlug, name: resolvedName, updated_at: resolvedUpdatedAt })]
    };
    albumNotFound = false;
    loadError = '';
  }

  function openExportModal(item) {
    exportModalItem = item;
    exportModalOpen = true;
  }

  async function handleExportVariant(format, item = exportModalItem) {
    exportModalBusy = true;
    try {
      await downloadExportVariant(item.imageId, format);
      showToast('success', t('dashboard.exportDownloaded'));
    } catch (error) {
      showToast('error', error?.message || t('common.somethingWentWrong'));
    } finally {
      exportModalBusy = false;
    }
  }

  function handleLogout() {
    AUTH_STORAGE_KEYS.forEach((key) => {
      localStorage.removeItem(key);
      sessionStorage.removeItem(key);
    });
    sessionStorage.removeItem(ALBUM_CACHE_SESSION_KEY);
    sessionStorage.removeItem('glassclear-albums-report-demo');
    clearPendingGuestImage();
    goto('/login');
  }

  onMount(async () => {
    if (!getStoredToken()) {
      goto('/login');
      return;
    }

    currentUser = await getCurrentUser().catch(() => ({ name: localStorage.getItem('user_name') || t('common.user'), email: '' }));

    await loadAlbum().catch((error) => {
      album = null;
      albumNotFound = error?.status === 404;
      loadError = error?.message || t('common.somethingWentWrong');
      if (!albumNotFound) {
        showToast('error', loadError);
      }
    });

    loaded = true;
  });

  onDestroy(() => clearTimeout(toastTimer));
</script>

<script context="module">
  export async function load({ params }) {
    return { albumSlug: params.albumSlug };
  }
</script>

<svelte:head>
  <title>{album?.name || labels.albumsTitle} | GlassClear</title>
</svelte:head>

{#if toast}
  <Toast {toast} onDismiss={() => (toast = null)} />
{/if}

<div class="gc-dashboard-page">
  <div class="gc-dashboard-shell">
    <DashboardTopbar
      title={album?.name || labels.albumsTitle}
      searchValue={searchQuery}
      searchPlaceholder={labels.searchPlaceholder}
      uploadLabel={labels.backToAlbums}
      languageLabel={labels.language}
      languageOptions={LANGUAGE_OPTIONS}
      {currentLanguage}
      userName={getDisplayName(currentUser)}
      userInitial={getUserInitial(currentUser)}
      logoutLabel={labels.logout}
      onSearch={(value) => (searchQuery = value)}
      onUpload={() => goto('/dashboard/albums')}
      onLanguageChange={(code) => {
        setLanguage(code);
        showToast('success', t('dashboard.languageChanged'));
      }}
      onLogout={handleLogout}
    />

    {#if loaded && album}
      <section class="gc-card gc-album-hero">
        <div class="gc-album-hero__copy">
          <p class="gc-panel-caption">{album.slug}</p>
          <h2>{album.name}</h2>
          <p>{album.description}</p>
          <p>{album.count} {labels.imagesLabel} | {labels.updatedLabel}: {formatDate(album.updatedAt)}</p>
        </div>
      </section>

      {#if filteredItems.length}
        <section class="gc-card">
          <div class="gc-card__header">
            <div>
              <h2>{album.name}</h2>
              <p>{album.description}</p>
            </div>
          </div>

          <div class="gc-history-grid gc-album-detail-grid">
            {#each filteredItems as item}
              <article class="gc-history-item gc-history-item--card">
                {#if item.thumbnail}
                  <img src={item.thumbnail} alt={getResultDisplayName(item)} class="gc-history-item__thumb" />
                {:else}
                  <div class="gc-history-item__thumb-placeholder" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3.5" y="5" width="17" height="14" rx="2.5"></rect>
                      <path d="M7.5 14.5l2.5-2.5 2.5 2.5 4-4 2 2"></path>
                      <circle cx="9" cy="9" r="1.25"></circle>
                    </svg>
                  </div>
                {/if}

                <div class="gc-history-item__copy">
                  <h3>{getResultDisplayName(item)}</h3>
                  {#if getResultDisplayName(item) !== item.filename}
                    <p class="gc-history-item__filename">{item.filename}</p>
                  {/if}
                  <p class="gc-history-item__date">{item.date}</p>
                  <StatusBadge status={item.status} />
                </div>

                <div class="gc-history-item__actions">
                  <button type="button" class="gc-button gc-button--soft" disabled={item.isPreview} onclick={() => goto(`/dashboard/results/${item.imageId}`)}>
                    {labels.viewResult}
                  </button>
                  <button type="button" class="gc-button gc-button--primary" disabled={item.isPreview} onclick={() => openExportModal(item)}>
                    {labels.export}
                  </button>
                </div>
              </article>
            {/each}
          </div>
        </section>
      {:else}
        <section class="gc-card">
          <EmptyState
            title={album.items.length ? labels.noMatchingImages : labels.emptyTitle}
            message={album.items.length ? labels.searchHelp : labels.emptyMessage}
          />
        </section>
      {/if}
    {:else if loaded && albumNotFound}
      <section class="gc-card gc-album-hero">
        <div class="gc-album-hero__copy">
          <p class="gc-panel-caption">{labels.smartAlbumLabel}</p>
          <h2>{labels.notFoundTitle}</h2>
          <p>{labels.notFoundMessage}</p>
          <button type="button" class="gc-button gc-button--primary" onclick={() => goto('/dashboard/albums')}>
            {labels.backToAlbums}
          </button>
        </div>
      </section>
    {:else if loaded}
      <section class="gc-card gc-album-hero">
        <div class="gc-album-hero__copy">
          <p class="gc-panel-caption">{labels.smartAlbumLabel}</p>
          <h2>{loadError || t('common.somethingWentWrong')}</h2>
          <p>{t('common.somethingWentWrong')}</p>
        </div>
      </section>
    {/if}
  </div>
</div>

<ExportResultModal
  open={exportModalOpen}
  item={exportModalItem}
  busy={exportModalBusy}
  labels={labels.exportModal}
  onClose={() => (exportModalOpen = false)}
  onJpg={() => handleExportVariant('jpg', exportModalItem)}
  onPng={() => handleExportVariant('png', exportModalItem)}
  onHd={() => handleExportVariant('hd', exportModalItem)}
  onComparison={() => handleExportVariant('comparison', exportModalItem)}
/>

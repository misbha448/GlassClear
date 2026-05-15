<svelte:options runes={false} />

<script>
  import '../../../styles/dashboard.css';

  import { goto } from '$app/navigation';
  import { onDestroy, onMount } from 'svelte';
  import inputAsset from '$lib/assets/input.jpg';
  import outputAsset from '$lib/assets/output.jpg';
  import DashboardTopbar from '$lib/components/dashboard/DashboardTopbar.svelte';
  import SmartAlbumsPanel from '$lib/components/dashboard/SmartAlbumsPanel.svelte';
  import Toast from '$lib/components/dashboard/Toast.svelte';
  import { LANGUAGE_OPTIONS, language, setLanguage, t } from '$lib/stores/language.js';
  import { getAlbums, getCurrentUser, withBase } from '$lib/api/dashboardApi.js';
  import { getStoredToken } from '$lib/api/api.js';
  import { clearPendingGuestImage } from '$lib/utils/pendingGuestImage.js';
  import { getDisplayName, getUserInitial } from '$lib/utils/userDisplay.js';

  const AUTH_STORAGE_KEYS = ['token', 'token_type', 'role', 'user_name', 'authToken', 'access_token', 'refresh_token'];
  const ALBUM_DEMO_SESSION_KEY = 'glassclear-albums-report-demo';
  const ALBUM_CACHE_SESSION_KEY = 'glassclear-albums-cache';
  const SELECTED_ALBUM_SESSION_KEY = 'glassclear-selected-album';
  const DEMO_ALBUM_COVERS = {
    'high-reflection': outputAsset,
    'interior-spaces': inputAsset,
    'outdoor-architecture': outputAsset,
    'client-deliveries': inputAsset,
    miscellaneous: outputAsset
  };

  let currentLanguage = 'en';
  let currentUser = null;
  let searchQuery = '';
  let albums = [];
  let toast = null;
  let toastTimer;
  let loaded = false;
  let labels = {};

  $: activeLanguage = $language;
  $: currentLanguage = activeLanguage;
  $: filteredAlbums = albums.filter((album) => {
    if (!searchQuery) return true;
    const query = searchQuery.toLowerCase();
    return `${album.name} ${album.description} ${album.slug}`.toLowerCase().includes(query);
  });

  $: {
    activeLanguage;
    labels = {
      title: t('albums.title'),
      subtitle: t('albums.subtitle'),
      searchPlaceholder: t('common.searchDashboard'),
      backToDashboard: t('common.backToDashboard'),
      language: t('common.language'),
      logout: t('common.logout'),
      viewAlbum: t('albums.viewAlbum'),
      viewAll: t('albums.viewAll'),
      imagesLabel: t('albums.imagesLabel'),
      updatedLabel: t('albums.updatedLabel'),
      justNow: t('albums.justNow'),
      emptyTitle: t('albums.emptyTitle'),
      emptyMessage: t('albums.emptyMessage')
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

  function mapAlbum(source = {}) {
    return {
      slug: source.slug,
      name: source.name || t('albums.fallbackName'),
      description: source.description || '',
      count: Number(source.count ?? 0),
      cover_url: normalizeUrl(source.cover_url),
      updated_at: source.updated_at || null
    };
  }

  function withDemoAlbumPreviews(items = []) {
    if (typeof sessionStorage === 'undefined') return items;
    if (sessionStorage.getItem(ALBUM_DEMO_SESSION_KEY)) return items;

    const enhanced = items.map((album) => {
      if (album.count > 0 || album.cover_url) return album;
      const demoCover = DEMO_ALBUM_COVERS[album.slug];
      if (!demoCover) return album;
      return {
        ...album,
        cover_url: demoCover
      };
    });

    sessionStorage.setItem(ALBUM_DEMO_SESSION_KEY, 'used');
    return enhanced;
  }

  async function loadAlbums() {
    const payload = await getAlbums();
    const mappedAlbums = Array.isArray(payload?.albums) ? payload.albums.map(mapAlbum) : [];
    albums = withDemoAlbumPreviews(mappedAlbums);
    if (typeof sessionStorage !== 'undefined') {
      sessionStorage.setItem(ALBUM_CACHE_SESSION_KEY, JSON.stringify(mappedAlbums));
    }
  }

  function openAlbum(albumSlug) {
    const album = albums.find((item) => item.slug === albumSlug);
    if (typeof sessionStorage !== 'undefined' && album) {
      sessionStorage.setItem(SELECTED_ALBUM_SESSION_KEY, JSON.stringify(album));
    }
    goto(`/dashboard/albums/${albumSlug}`);
  }

  function handleLogout() {
    AUTH_STORAGE_KEYS.forEach((key) => {
      localStorage.removeItem(key);
      sessionStorage.removeItem(key);
    });
    sessionStorage.removeItem(ALBUM_DEMO_SESSION_KEY);
    sessionStorage.removeItem(ALBUM_CACHE_SESSION_KEY);
    sessionStorage.removeItem(SELECTED_ALBUM_SESSION_KEY);
    clearPendingGuestImage();
    goto('/login');
  }

  onMount(async () => {
    if (!getStoredToken()) {
      goto('/login');
      return;
    }

    currentUser = await getCurrentUser().catch(() => ({ name: localStorage.getItem('user_name') || t('common.user'), email: '' }));
    await loadAlbums().catch((error) => {
      showToast('error', error?.message || t('common.somethingWentWrong'));
    });
    loaded = true;
  });

  onDestroy(() => clearTimeout(toastTimer));
</script>

<svelte:head>
  <title>{labels.title} | GlassClear</title>
</svelte:head>

{#if toast}
  <Toast {toast} onDismiss={() => (toast = null)} />
{/if}

<div class="gc-dashboard-page">
  <div class="gc-dashboard-shell">
    <DashboardTopbar
      title={labels.title}
      searchValue={searchQuery}
      searchPlaceholder={labels.searchPlaceholder}
      uploadLabel={labels.backToDashboard}
      languageLabel={labels.language}
      languageOptions={LANGUAGE_OPTIONS}
      {currentLanguage}
      userName={getDisplayName(currentUser)}
      userInitial={getUserInitial(currentUser)}
      logoutLabel={labels.logout}
      onSearch={(value) => (searchQuery = value)}
      onUpload={() => goto('/dashboard')}
      onLanguageChange={(code) => {
        setLanguage(code);
        showToast('success', t('dashboard.languageChanged'));
      }}
      onLogout={handleLogout}
    />

    {#if loaded}
      <SmartAlbumsPanel
        albums={filteredAlbums}
        labels={labels}
        onViewAlbum={openAlbum}
      />
    {/if}
  </div>
</div>

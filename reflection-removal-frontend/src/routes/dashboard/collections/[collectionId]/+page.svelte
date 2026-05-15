<svelte:options runes={false} />

<script>
  import '../../../../styles/dashboard.css';

  import { goto } from '$app/navigation';
  import { onDestroy, onMount } from 'svelte';
  import DashboardTopbar from '$lib/components/dashboard/DashboardTopbar.svelte';
  import HistoryPanel from '$lib/components/dashboard/HistoryPanel.svelte';
  import ExportResultModal from '$lib/components/dashboard/ExportResultModal.svelte';
  import Toast from '$lib/components/dashboard/Toast.svelte';
  import { LANGUAGE_OPTIONS, language, setLanguage, t } from '$lib/stores/language.js';
  import { downloadExportVariant, getCollection, getCurrentUser, removeCollectionItem, withBase } from '$lib/api/dashboardApi.js';
  import { clearPendingGuestImage } from '$lib/utils/pendingGuestImage.js';
  import { getStoredToken } from '$lib/api/api.js';
  import { getDisplayName, getUserInitial } from '$lib/utils/userDisplay.js';

  export let data;

  const AUTH_STORAGE_KEYS = ['token', 'token_type', 'role', 'user_name', 'authToken', 'access_token', 'refresh_token'];

  let currentLanguage = 'en';
  let currentUser = null;
  let searchQuery = '';
  let collection = null;
  let exportModalOpen = false;
  let exportModalItem = null;
  let exportModalBusy = false;
  let loaded = false;
  let toast = null;
  let toastTimer;

  $: activeLanguage = $language;
  $: currentLanguage = activeLanguage;
  $: filteredItems = (collection?.items || []).filter((item) => {
    if (!searchQuery) return true;
    return `${item.filename} ${item.status || ''}`.toLowerCase().includes(searchQuery.toLowerCase());
  });

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
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return t('common.recently');
    return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
  }

  function mapItem(source = {}) {
    return {
      id: source.id,
      imageId: source.id,
      filename: source.filename || t('resultDetail.title'),
      title: source.display_name || null,
      originalUrl: normalizeUrl(source.original_url),
      processedUrl: normalizeUrl(source.processed_url),
      thumbnail: normalizeUrl(source.thumbnail_url || source.processed_url || source.original_url),
      processedAt: source.created_at,
      processedAtLabel: formatDate(source.created_at),
      status: (source.status || 'completed').toLowerCase()
    };
  }

  async function loadCollectionDetail() {
    const payload = await getCollection(data.collectionId);
    collection = {
      id: payload.id,
      name: payload.name || t('collections.fallbackName'),
      count: Number(payload.count ?? 0),
      items: Array.isArray(payload.items) ? payload.items.map(mapItem) : []
    };
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

  async function handleRemove(item) {
    if (!window.confirm(t('collections.removeConfirm', { filename: item.filename }))) return;
    try {
      await removeCollectionItem(collection.id, item.imageId);
      await loadCollectionDetail();
      showToast('success', t('collections.removed'));
    } catch (error) {
      showToast('error', error?.message || t('collections.removeFailed'));
    }
  }

  function handleLogout() {
    AUTH_STORAGE_KEYS.forEach((key) => {
      localStorage.removeItem(key);
      sessionStorage.removeItem(key);
    });
    clearPendingGuestImage();
    goto('/login');
  }

  onMount(async () => {
    if (!getStoredToken()) {
      goto('/login');
      return;
    }

    currentUser = await getCurrentUser().catch(() => ({ name: localStorage.getItem('user_name') || t('common.user'), email: '' }));
    await loadCollectionDetail().catch((error) => {
      showToast('error', error?.message || t('collections.loadFailed'));
      goto('/dashboard/collections');
    });
    loaded = true;
  });

  onDestroy(() => clearTimeout(toastTimer));
</script>

<script context="module">
  export async function load({ params }) {
    return { collectionId: params.collectionId };
  }
</script>

<svelte:head>
  <title>{collection?.name || t('collections.title')} | GlassClear</title>
</svelte:head>

{#if toast}
  <Toast {toast} onDismiss={() => (toast = null)} />
{/if}

<div class="gc-dashboard-page">
  <div class="gc-dashboard-shell">
    <DashboardTopbar
      title={collection?.name || t('collections.title')}
      searchValue={searchQuery}
      searchPlaceholder={t('common.searchFilenameOrStatus')}
      uploadLabel={t('collections.viewAllShort')}
      languageLabel={t('common.language')}
      languageOptions={LANGUAGE_OPTIONS}
      {currentLanguage}
      userName={getDisplayName(currentUser)}
      userInitial={getUserInitial(currentUser)}
      logoutLabel={t('common.logout')}
      onSearch={(value) => (searchQuery = value)}
      onUpload={() => goto('/dashboard/collections')}
      onLanguageChange={(code) => {
        setLanguage(code);
        showToast('success', t('dashboard.languageChanged'));
      }}
      onLogout={handleLogout}
    />

    {#if loaded}
      <HistoryPanel
        items={filteredItems}
        variant="grid"
        labels={{
          title: collection?.name || t('collections.title'),
          subtitle: t('collections.detailSubtitle'),
          view: t('common.view'),
          export: t('common.export'),
          delete: t('common.remove'),
          emptyTitle: t('collections.emptyDetailTitle'),
          emptyMessage: t('collections.emptyDetailMessage')
        }}
        onView={(item) => goto(`/dashboard/results/${item.imageId}`)}
        onExport={openExportModal}
        onDelete={handleRemove}
      />
    {/if}
  </div>
</div>

<ExportResultModal
  open={exportModalOpen}
  item={exportModalItem}
  busy={exportModalBusy}
  labels={{
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
  }}
  onClose={() => (exportModalOpen = false)}
  onJpg={() => handleExportVariant('jpg', exportModalItem)}
  onPng={() => handleExportVariant('png', exportModalItem)}
  onHd={() => handleExportVariant('hd', exportModalItem)}
  onComparison={() => handleExportVariant('comparison', exportModalItem)}
/>

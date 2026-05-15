<svelte:options runes={false} />

<script>
  import '../../../styles/dashboard.css';

  import { goto } from '$app/navigation';
  import { onDestroy, onMount } from 'svelte';
  import DashboardTopbar from '$lib/components/dashboard/DashboardTopbar.svelte';
  import HistoryPanel from '$lib/components/dashboard/HistoryPanel.svelte';
  import ExportResultModal from '$lib/components/dashboard/ExportResultModal.svelte';
  import Toast from '$lib/components/dashboard/Toast.svelte';
  import { LANGUAGE_OPTIONS, language, setLanguage, t } from '$lib/stores/language.js';
  import { deleteHistoryItem, downloadExportVariant, getCurrentUser, getHistory, withBase } from '$lib/api/dashboardApi.js';
  import { clearPendingGuestImage } from '$lib/utils/pendingGuestImage.js';
  import { getDisplayName, getUserInitial } from '$lib/utils/userDisplay.js';
  import { getStoredToken } from '$lib/api/api.js';

  const AUTH_STORAGE_KEYS = ['token', 'token_type', 'role', 'user_name', 'authToken', 'access_token', 'refresh_token'];

  let currentLanguage = 'en';
  let currentUser = null;
  let searchQuery = '';
  let statusFilter = 'all';
  let historyItems = [];
  let exportModalOpen = false;
  let exportModalItem = null;
  let exportModalBusy = false;
  let toast = null;
  let toastTimer;
  let loaded = false;
  let labels = {};

  $: activeLanguage = $language;
  $: currentLanguage = activeLanguage;
  $: filteredItems = historyItems;

  $: {
    activeLanguage;
    labels = {
      topbarTitle: t('history.title'),
      searchPlaceholder: t('common.searchFilenameOrStatus'),
      backToDashboard: t('common.backToDashboard'),
      language: t('common.language'),
      logout: t('common.logout'),
      title: t('history.title'),
      subtitle: t('history.subtitle'),
      status: t('common.status'),
      all: t('history.all'),
      completed: t('batch.completed'),
      failed: t('batch.failed'),
      uploaded: t('history.uploaded'),
      view: t('common.view'),
      export: t('common.export'),
      delete: t('common.delete'),
      emptyTitle: t('history.emptyTitle'),
      emptyMessage: t('history.emptyMessage'),
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

  function formatDate(dateValue) {
    const date = new Date(dateValue);
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

  async function loadHistory() {
    const payload = await getHistory({
      limit: 100,
      status: statusFilter,
      search: searchQuery
    });
    historyItems = Array.isArray(payload?.items) ? payload.items.map(mapItem) : [];
  }

  function openExportModal(item) {
    if (item?.status === 'failed') {
      showToast('info', t('dashboard.exportFailed'));
      return;
    }
    if (!item?.processedUrl) {
      showToast('info', t('dashboard.exportUnavailable'));
      return;
    }
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

  async function handleDelete(item) {
    if (!window.confirm(t('dashboard.deleteConfirm', { filename: item.filename }))) return;
    try {
      await deleteHistoryItem(item.imageId);
      historyItems = historyItems.filter((entry) => entry.imageId !== item.imageId);
      showToast('success', t('history.deleteSuccess'));
    } catch (error) {
      showToast('error', error?.message || t('common.somethingWentWrong'));
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
    await loadHistory().catch((error) => {
      if (error?.status === 401) {
        showToast('error', t('dashboard.relogin'));
        goto('/login');
        return;
      }
      showToast('error', t('common.somethingWentWrong'));
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

<div class="gc-dashboard-page gc-history-page">
  <div class="gc-dashboard-shell">
    <DashboardTopbar
      title={labels.topbarTitle}
      searchValue={searchQuery}
      searchPlaceholder={labels.searchPlaceholder}
      uploadLabel={labels.backToDashboard}
      languageLabel={labels.language}
      languageOptions={LANGUAGE_OPTIONS}
      {currentLanguage}
      userName={getDisplayName(currentUser)}
      userInitial={getUserInitial(currentUser)}
      logoutLabel={labels.logout}
      onSearch={async (value) => {
        searchQuery = value;
        await loadHistory().catch(() => showToast('error', t('common.somethingWentWrong')));
      }}
      onUpload={() => goto('/dashboard')}
      onLanguageChange={(code) => {
        setLanguage(code);
        showToast('success', t('dashboard.languageChanged'));
      }}
      onLogout={handleLogout}
    />

    {#if loaded}
      <section class="gc-card gc-history-toolbar">
        <div>
          <h2>{labels.title}</h2>
          <p>{labels.subtitle}</p>
        </div>

        <label class="gc-filter-select">
          <span>{labels.status}</span>
          <select bind:value={statusFilter} onchange={async () => await loadHistory()}>
            <option value="all">{labels.all}</option>
            <option value="completed">{labels.completed}</option>
            <option value="failed">{labels.failed}</option>
            <option value="uploaded">{labels.uploaded}</option>
          </select>
        </label>
      </section>

      <HistoryPanel
        items={filteredItems}
        variant="grid"
        labels={{
          title: labels.title,
          subtitle: labels.subtitle,
          view: labels.view,
          export: labels.export,
          delete: labels.delete,
          emptyTitle: labels.emptyTitle,
          emptyMessage: labels.emptyMessage
        }}
        onView={(item) => goto(`/dashboard/results/${item.imageId}`)}
        onExport={openExportModal}
        onDelete={handleDelete}
      />
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

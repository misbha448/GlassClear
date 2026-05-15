<svelte:options runes={false} />

<script>
  import '../../../styles/dashboard.css';

  import { goto } from '$app/navigation';
  import { onDestroy, onMount } from 'svelte';
  import DashboardTopbar from '$lib/components/dashboard/DashboardTopbar.svelte';
  import CollectionPickerModal from '$lib/components/dashboard/CollectionPickerModal.svelte';
  import CollectionsPanel from '$lib/components/dashboard/CollectionsPanel.svelte';
  import Toast from '$lib/components/dashboard/Toast.svelte';
  import { LANGUAGE_OPTIONS, language, setLanguage, t } from '$lib/stores/language.js';
  import { createCollection, getCollections, getCurrentUser, withBase } from '$lib/api/dashboardApi.js';
  import { getStoredToken } from '$lib/api/api.js';
  import { clearPendingGuestImage } from '$lib/utils/pendingGuestImage.js';
  import { getDisplayName, getUserInitial } from '$lib/utils/userDisplay.js';

  const AUTH_STORAGE_KEYS = ['token', 'token_type', 'role', 'user_name', 'authToken', 'access_token', 'refresh_token'];

  let currentLanguage = 'en';
  let currentUser = null;
  let searchQuery = '';
  let collections = [];
  let creatingCollection = false;
  let collectionModalOpen = false;
  let newCollectionName = '';
  let loaded = false;
  let toast = null;
  let toastTimer;

  $: activeLanguage = $language;
  $: currentLanguage = activeLanguage;
  $: filteredCollections = collections.filter((collection) => {
    if (!searchQuery) return true;
    return `${collection.name}`.toLowerCase().includes(searchQuery.toLowerCase());
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

  async function loadCollections() {
    const payload = await getCollections();
    collections = Array.isArray(payload?.collections)
      ? payload.collections.map((collection) => ({
          id: collection.id,
          name: collection.name || t('collections.fallbackName'),
          count: Number(collection.count ?? 0),
          cover_url: normalizeUrl(collection.cover_url),
          updated_at: collection.updated_at || null
        }))
      : [];
  }

  function openCreateCollectionModal() {
    collectionModalOpen = true;
    newCollectionName = '';
  }

  function closeCreateCollectionModal() {
    collectionModalOpen = false;
    newCollectionName = '';
  }

  async function handleCreateCollection() {
    if (!newCollectionName.trim()) return;
    creatingCollection = true;
    try {
      await createCollection(newCollectionName.trim());
      await loadCollections();
      closeCreateCollectionModal();
      showToast('success', t('collections.created'));
    } catch (error) {
      showToast('error', error?.message || t('collections.createFailed'));
    } finally {
      creatingCollection = false;
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
    await loadCollections().catch((error) => showToast('error', error?.message || t('common.somethingWentWrong')));
    loaded = true;
  });

  onDestroy(() => clearTimeout(toastTimer));
</script>

<svelte:head>
  <title>{t('collections.title')} | GlassClear</title>
</svelte:head>

{#if toast}
  <Toast {toast} onDismiss={() => (toast = null)} />
{/if}

<div class="gc-dashboard-page">
  <div class="gc-dashboard-shell">
    <DashboardTopbar
      title={t('collections.title')}
      searchValue={searchQuery}
      searchPlaceholder={t('common.searchDashboard')}
      uploadLabel={t('common.backToDashboard')}
      languageLabel={t('common.language')}
      languageOptions={LANGUAGE_OPTIONS}
      {currentLanguage}
      userName={getDisplayName(currentUser)}
      userInitial={getUserInitial(currentUser)}
      logoutLabel={t('common.logout')}
      onSearch={(value) => (searchQuery = value)}
      onUpload={() => goto('/dashboard')}
      onLanguageChange={(code) => {
        setLanguage(code);
        showToast('success', t('dashboard.languageChanged'));
      }}
      onLogout={handleLogout}
    />

    {#if loaded}
      <CollectionsPanel
        collections={filteredCollections}
        showViewAll={false}
        creating={creatingCollection}
        addingLatest={false}
        latestResultAvailable={false}
        onCreate={openCreateCollectionModal}
        onAddLatest={() => {}}
        onAddLatestToCollection={() => {}}
        onOpenCollection={(collectionId) => goto(`/dashboard/collections/${collectionId}`)}
        onViewAll={() => {}}
      />
    {/if}
  </div>
</div>

<CollectionPickerModal
  open={collectionModalOpen}
  collections={[]}
  creating={creatingCollection}
  adding={false}
  latestResultAvailable={false}
  bind:newCollectionName
  selectedCollectionId={null}
  mode="create"
  onClose={closeCreateCollectionModal}
  onChoose={() => {}}
  onAdd={() => {}}
  onCreate={handleCreateCollection}
/>

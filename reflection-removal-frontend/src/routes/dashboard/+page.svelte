<svelte:options runes={false} />

<script>
  import '../../styles/dashboard.css';

  import { goto } from '$app/navigation';
  import { onDestroy, onMount } from 'svelte';
  import inputAsset from '$lib/assets/input.jpg';
  import outputAsset from '$lib/assets/output.jpg';
  import DashboardTopbar from '$lib/components/dashboard/DashboardTopbar.svelte';
  import LatestResultCard from '$lib/components/dashboard/LatestResultCard.svelte';
  import BatchProcessingPanel from '$lib/components/dashboard/BatchProcessingPanel.svelte';
  import SmartAlbumsPanel from '$lib/components/dashboard/SmartAlbumsPanel.svelte';
  import HistoryPanel from '$lib/components/dashboard/HistoryPanel.svelte';
  import DeliveryPackPanel from '$lib/components/dashboard/DeliveryPackPanel.svelte';
  import CollectionsPanel from '$lib/components/dashboard/CollectionsPanel.svelte';
  import CollectionPickerModal from '$lib/components/dashboard/CollectionPickerModal.svelte';
  import ExportResultModal from '$lib/components/dashboard/ExportResultModal.svelte';
  import Toast from '$lib/components/dashboard/Toast.svelte';
  import { LANGUAGE_OPTIONS, language, setLanguage, t } from '$lib/stores/language.js';
  import {
    addCollectionItem,
    claimGuestImage,
    createCollection,
    createDeliveryPack,
    deleteHistoryItem,
    downloadBatchZipFile,
    downloadDeliveryPack,
    downloadExportVariant,
    getBatchStatus,
    getCollections,
    getCurrentUser,
    getWorkspace,
    startBatch,
    uploadBatch,
    withBase
  } from '$lib/api/dashboardApi.js';
  import { getStoredToken } from '$lib/api/api.js';
  import { clearPendingGuestImage, loadPendingGuestImage } from '$lib/utils/pendingGuestImage.js';
  import { getDisplayName, getUserInitial } from '$lib/utils/userDisplay.js';

  const AUTH_STORAGE_KEYS = ['token', 'token_type', 'role', 'user_name', 'authToken', 'access_token', 'refresh_token'];
  const UPLOAD_ROUTE = '/#upload';
  const DEFAULT_FILENAME = 'Sample Architectural Image';
  const MAX_BATCH_FILES = 20;
  const MAX_BATCH_SIZE = 5 * 1024 * 1024;
  const ALLOWED_BATCH_TYPES = new Set(['jpg', 'jpeg', 'png', 'webp']);

  let batchFileInput;
  let toast = null;
  let toastTimer;
  let currentLanguage = 'en';
  let currentUser = null;
  let searchQuery = '';
  let latestResult = null;
  let latestResultHelper = '';
  let historyItems = [];
  let smartAlbums = [];
  let collections = [];
  let workspaceLoaded = false;
  let exportModalOpen = false;
  let exportModalItem = null;
  let exportModalBusy = false;
  let batchQueue = [];
  let batchSummary = '';
  let batchNotice = '';
  let currentBatchId = null;
  let currentBatchStatus = 'idle';
  let batchZipUrl = null;
  let batchPollingTimer = null;
  let creatingCollection = false;
  let addingToCollection = false;
  let generatingDeliveryPack = false;
  let downloadingDeliveryPack = false;
  let latestDeliveryPackId = null;
  let latestDeliveryPackUrl = '';
  let collectionModalOpen = false;
  let collectionModalMode = 'add';
  let selectedCollectionId = null;
  let newCollectionName = '';
  let pageLabels = {};

  $: activeLanguage = $language;
  $: currentLanguage = activeLanguage;

  $: filteredHistory = historyItems.filter((item) => {
    if (!searchQuery) return true;
    const query = searchQuery.toLowerCase();
    return item.filename.toLowerCase().includes(query) || item.status.toLowerCase().includes(query);
  });

  $: filteredAlbums = smartAlbums.filter((album) => {
    if (!searchQuery) return true;
    const target = `${album.name} ${album.description} ${album.slug}`.toLowerCase();
    return target.includes(searchQuery.toLowerCase());
  });
  $: dashboardAlbums = filteredAlbums.slice(0, 3);
  $: latestResultIsSample = latestResult?.status === 'sample';
  $: dashboardCollections = collections.slice(0, 3);
  $: latestCompletedResult = latestResult?.status === 'completed' && latestResult?.imageId ? latestResult : null;
  $: latestCompletedResultLabel = latestCompletedResult ? `${latestCompletedResult.filename} | ${latestCompletedResult.processedAtLabel}` : '';

  $: batchCompletedCount = batchQueue.filter((item) => item.status === 'completed').length;
  $: batchFailedCount = batchQueue.filter((item) => item.status === 'failed').length;
  $: batchOverallProgress = batchQueue.length ? Math.round(((batchCompletedCount + batchFailedCount) / batchQueue.length) * 100) : 0;
  $: batchCanStart = batchQueue.length > 0 && !currentBatchId && currentBatchStatus !== 'processing';
  $: batchCanClear = batchQueue.length > 0 && currentBatchStatus !== 'processing';
  $: batchCanDownload = Boolean(currentBatchId && batchZipUrl && (currentBatchStatus === 'completed' || currentBatchStatus === 'partially_failed'));
  $: updateBatchSummary(currentBatchStatus);

  $: {
    activeLanguage;
    pageLabels = {
      title: t('dashboard.title'),
      searchPlaceholder: t('common.searchDashboard'),
      uploadImage: t('common.uploadImage'),
      language: t('common.language'),
      logout: t('common.logout'),
      latest: {
        title: t('dashboard.latestResult'),
        subtitle: t('dashboard.latestResultSubtitle'),
        beforeAfter: t('dashboard.beforeAfter'),
        processedOn: t('dashboard.processedOn'),
        status: t('common.status'),
        original: t('common.original'),
        output: t('common.output'),
        viewResult: t('dashboard.viewResult'),
        exportResult: t('dashboard.exportResult'),
        emptyTitle: t('dashboard.emptyLatestTitle'),
        emptyMessage: t('dashboard.emptyLatestMessage'),
        uploadImage: t('common.uploadImage')
      },
      batch: {
        title: t('dashboard.batchProcessing'),
        subtitle: t('dashboard.batchSubtitle'),
        addImages: t('batch.addImages'),
        startBatch: t('batch.startBatch'),
        clearQueue: t('batch.clearQueue'),
        downloadZip: t('batch.downloadZip'),
        uploadHint: t('batch.uploadHint'),
        emptyTitle: t('batch.emptyTitle'),
        emptyMessage: t('batch.emptyMessage'),
        progressLabel: t('batch.progressLabel')
      },
      albums: {
        title: t('dashboard.smartAlbums'),
        subtitle: t('albums.subtitle'),
        emptyTitle: t('dashboard.smartAlbums'),
        emptyMessage: t('history.emptyMessage'),
        viewAlbum: t('albums.viewAlbum'),
        viewAll: t('albums.viewAll'),
        imagesLabel: t('albums.imagesLabel'),
        updatedLabel: t('albums.updatedLabel'),
        justNow: t('albums.justNow')
      },
      history: {
        title: t('dashboard.history'),
        subtitle: t('dashboard.historySubtitle'),
        view: t('common.view'),
        export: t('common.export'),
        delete: t('common.delete'),
        viewAll: t('history.viewAll'),
        emptyTitle: t('history.emptyTitle'),
        emptyMessage: t('history.emptyMessage')
      },
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
    toastTimer = setTimeout(() => {
      toast = null;
    }, 3200);
  }

  function normalizeUrl(url) {
    if (!url) return '';
    if (url.startsWith('http') || url.startsWith('blob:') || url.startsWith('data:')) return url;
    if (url.startsWith('/uploads')) return withBase(url) || url;
    return url;
  }

  function formatDate(dateValue) {
    if (!dateValue) return t('common.recently');
    const date = new Date(dateValue);
    if (Number.isNaN(date.getTime())) return t('common.recently');
    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  function buildResultItem(source = {}, fallbackToDefaults = false) {
    const originalUrl = normalizeUrl(source.originalUrl || source.original_url);
    const processedUrl = normalizeUrl(source.processedUrl || source.processed_url);
    const processedAt = source.processedAt || source.processed_at || source.created_at || new Date().toISOString();

    return {
      id: source.id || crypto.randomUUID(),
      imageId: source.imageId || source.image_id || source.id || null,
      title: source.title || source.display_name || null,
      filename: source.filename || DEFAULT_FILENAME,
      originalUrl: originalUrl || (fallbackToDefaults ? inputAsset : ''),
      processedUrl: processedUrl || (fallbackToDefaults ? outputAsset : ''),
      thumbnail:
        normalizeUrl(source.thumbnail || source.thumbnail_url) ||
        processedUrl ||
        originalUrl ||
        (fallbackToDefaults ? outputAsset : inputAsset),
      processedAt,
      processedAtLabel: formatDate(processedAt),
      status: (source.status || (fallbackToDefaults ? 'sample' : 'completed')).toLowerCase(),
      category: source.category || null
    };
  }

  function buildDefaultLatest() {
    return buildResultItem(
      {
        id: 'default-latest',
        filename: DEFAULT_FILENAME,
        original_url: inputAsset,
        processed_url: outputAsset,
        created_at: new Date().toISOString(),
        status: 'sample'
      },
      true
    );
  }

  function loadPendingGuestResult() {
    const pending = loadPendingGuestImage();
    if (!pending) return null;

    return buildResultItem(
      {
        id: pending.guest_image_id || 'pending-guest',
        image_id: pending.guest_image_id || null,
        filename: pending.guest_filename || DEFAULT_FILENAME,
        original_url: pending.guest_original_url || inputAsset,
        processed_url: pending.guest_processed_url || outputAsset,
        created_at: new Date().toISOString(),
        status: pending.guest_processed_url ? 'completed' : 'queued'
      },
      true
    );
  }

  async function claimPendingGuestResult() {
    const pending = loadPendingGuestImage();
    if (!pending?.guest_image_token || !getStoredToken()) return false;

    try {
      await claimGuestImage(pending.guest_image_token);
      clearPendingGuestImage();
      return true;
    } catch {
      return false;
    }
  }

  function mapWorkspacePayload(payload = {}) {
    currentUser = payload.user || currentUser;

    const latest = payload.latest_result ? buildResultItem(payload.latest_result) : null;
    const historySource = Array.isArray(payload.recent_history) ? payload.recent_history : payload.history;
    const albumSource = Array.isArray(payload.albums) ? payload.albums : payload.smart_albums;
    const recentHistory = Array.isArray(historySource) ? historySource.map((item) => buildResultItem(item)).slice(0, 4) : [];
    const albums = Array.isArray(albumSource)
      ? albumSource.map((album) => ({
          slug: album.slug,
          name: album.name || t('albums.fallbackName'),
          description: album.description || '',
          count: Number(album.count ?? 0),
          cover_url: normalizeUrl(album.cover_url),
          updated_at: album.updated_at || null
        }))
      : [];

    return { latest, recentHistory, albums };
  }

  async function loadCollectionsPreview() {
    try {
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
    } catch {
      collections = [];
    }
  }

  async function loadUserFallback() {
    try {
      currentUser = await getCurrentUser();
      if (currentUser?.name) {
        localStorage.setItem('user_name', currentUser.name);
      }
    } catch {
      currentUser = currentUser || { name: localStorage.getItem('user_name') || t('common.user'), email: '' };
    }
  }

  async function bootstrapDashboard() {
    const pendingGuest = loadPendingGuestResult();
    latestResultHelper = '';

    try {
      await claimPendingGuestResult();
      const workspace = await getWorkspace();
      const mapped = mapWorkspacePayload(workspace);
      latestResult = mapped.latest || pendingGuest || buildDefaultLatest();
      historyItems = mapped.recentHistory.length ? mapped.recentHistory : latestResult?.imageId ? [latestResult] : [];
      smartAlbums = mapped.albums;

      if (!mapped.latest) {
        latestResultHelper = t('dashboard.emptyLatestMessage');
      }
    } catch (error) {
      if (error?.status === 401) {
        showToast('error', t('dashboard.relogin'));
        goto('/login');
        return;
      }
      await loadUserFallback();
      latestResult = pendingGuest || buildDefaultLatest();
      latestResultHelper = t('dashboard.emptyLatestMessage');
      historyItems = latestResult?.imageId ? [latestResult] : [];
      smartAlbums = [];
    }

    workspaceLoaded = true;
  }

  function buildBatchQueueItem(item, index = 0) {
    return {
      id: item.id || `local-${index}`,
      name: item.filename || item.name || `Image ${index + 1}`,
      status: item.status || 'queued',
      originalUrl: normalizeUrl(item.original_url || item.originalUrl),
      processedUrl: normalizeUrl(item.processed_url || item.processedUrl),
      error_message: item.error_message || '',
      progress:
        item.progress ??
        (item.status === 'completed' || item.status === 'failed'
          ? 100
          : item.status === 'processing'
            ? 50
            : 0),
      file: item.file || null
    };
  }

  function updateBatchSummary(status = currentBatchStatus) {
    if (!batchQueue.length) {
      batchSummary = t('batch.summaryIdle');
      return;
    }

    if (status === 'completed') {
      batchSummary = t('batch.summaryCompleted', {
        completed: batchCompletedCount,
        total: batchQueue.length
      });
      return;
    }

    if (status === 'failed') {
      batchSummary = t('batch.summaryFailed', {
        failed: batchFailedCount,
        total: batchQueue.length
      });
      return;
    }

    if (status === 'partially_failed') {
      batchSummary = t('batch.summaryPartiallyFailed', {
        completed: batchCompletedCount,
        failed: batchFailedCount
      });
      return;
    }

    batchSummary = t(status === 'processing' ? 'batch.summaryProcessing' : 'batch.summaryQueued', {
      completed: batchCompletedCount,
      total: batchQueue.length
    });
  }

  function resetBatchState(clearQueue = true) {
    stopBatchPolling();
    currentBatchId = null;
    currentBatchStatus = 'idle';
    batchZipUrl = null;
    batchNotice = '';
    batchSummary = t('batch.summaryIdle');
    if (clearQueue) {
      batchQueue = [];
    }
  }

  function stopBatchPolling() {
    if (batchPollingTimer) {
      clearInterval(batchPollingTimer);
      batchPollingTimer = null;
    }
  }

  function validateBatchFiles(fileList, existingCount = 0) {
    const files = Array.from(fileList || []);
    if (!files.length) return [];

    if (existingCount + files.length > MAX_BATCH_FILES) {
      showToast('error', t('batch.selectLimit'));
      return [];
    }

    const validFiles = [];
    for (const file of files) {
      const extension = file.name.split('.').pop()?.toLowerCase() || '';
      if (!ALLOWED_BATCH_TYPES.has(extension)) {
        showToast('error', t('batch.invalidType', { filename: file.name }));
        continue;
      }
      if (file.size > MAX_BATCH_SIZE) {
        showToast('error', t('batch.fileTooLarge', { filename: file.name }));
        continue;
      }
      validFiles.push(file);
    }

    return validFiles;
  }

  function handleBatchPickFiles() {
    batchFileInput?.click();
  }

  function handleBatchFilesSelected(event) {
    const validFiles = validateBatchFiles(event.currentTarget.files, batchQueue.length);
    if (!validFiles.length) {
      event.currentTarget.value = '';
      return;
    }

    batchQueue = [
      ...batchQueue,
      ...validFiles.map((file, index) =>
        buildBatchQueueItem(
          {
            id: `local-${Date.now()}-${index}`,
            filename: file.name,
            status: 'queued',
            progress: 0,
            file
          },
          index
        )
      )
    ];
    batchNotice = '';
    updateBatchSummary('queued');
    event.currentTarget.value = '';
  }

  async function syncBatchStatus(batchId) {
    const payload = await getBatchStatus(batchId);
    currentBatchId = payload.batch_id;
    currentBatchStatus = payload.status;
    batchZipUrl = payload.zip_url || null;
    batchQueue = (payload.items || []).map((item, index) => buildBatchQueueItem(item, index));
    const completedItems = (payload.items || [])
      .filter((item) => item.status === 'completed')
      .map((item) =>
        buildResultItem({
          id: item.image_id || item.id,
          image_id: item.image_id || item.id,
          filename: item.filename,
          original_url: item.original_url,
          processed_url: item.processed_url,
          created_at: item.created_at,
          status: item.status
        })
      );

    if (completedItems.length) {
      const mergedHistory = [...completedItems, ...historyItems].reduce((items, item) => {
        if (!items.some((entry) => entry.imageId === item.imageId)) {
          items.push(item);
        }
        return items;
      }, []);
      historyItems = mergedHistory.slice(0, 4);
      latestResult = completedItems[0] || latestResult;
    }

    updateBatchSummary(payload.status);

    if (!['queued', 'processing'].includes(payload.status)) {
      stopBatchPolling();
    }

    if (payload.status === 'completed') {
      batchNotice = t('batch.downloadReady');
    } else if (payload.status === 'partially_failed') {
      batchNotice = t('batch.summaryPartiallyFailed', {
        completed: payload.completed_count || 0,
        failed: payload.failed_count || 0
      });
    } else if (payload.status === 'failed') {
      batchNotice = t('batch.summaryFailed', {
        failed: payload.failed_count || 0,
        total: payload.total_count || batchQueue.length
      });
    } else {
      batchNotice = '';
    }
  }

  function startBatchPolling(batchId) {
    stopBatchPolling();
    batchPollingTimer = setInterval(async () => {
      try {
        await syncBatchStatus(batchId);
      } catch (error) {
        stopBatchPolling();
        if (error?.status >= 404) {
          showToast('error', error?.message || t('batch.pollStopped'));
        }
      }
    }, 2000);
  }

  async function handleBatchStart() {
    if (!batchQueue.length) {
      showToast('info', t('batch.noItemsReady'));
      return;
    }
    if (currentBatchStatus === 'processing') {
      return;
    }

    try {
      if (!currentBatchId) {
        const files = batchQueue.map((item) => item.file).filter(Boolean);
        if (!files.length) {
          showToast('error', t('batch.uploadFailed'));
          return;
        }

        const uploadResponse = await uploadBatch(files);
        currentBatchId = uploadResponse.batch_id;
        currentBatchStatus = uploadResponse.status;
        batchQueue = (uploadResponse.items || []).map((item, index) => buildBatchQueueItem(item, index));
        updateBatchSummary(uploadResponse.status);
      }

      await startBatch(currentBatchId);
      currentBatchStatus = 'processing';
      batchNotice = '';
      showToast('success', t('batch.started'));
      await syncBatchStatus(currentBatchId);
      startBatchPolling(currentBatchId);
    } catch (error) {
      showToast('error', error?.message || t('batch.startFailed'));
    }
  }

  function handleBatchClear() {
    if (currentBatchStatus === 'processing') return;
    resetBatchState(true);
  }

  async function handleBatchDownload() {
    if (!currentBatchId) {
      showToast('info', t('batch.noBatchReady'));
      return;
    }

    try {
      await downloadBatchZipFile(currentBatchId);
      showToast('success', t('batch.downloadReady'));
    } catch (error) {
      showToast('error', error?.message || t('common.somethingWentWrong'));
    }
  }

  function handleUploadNavigation() {
    goto(UPLOAD_ROUTE);
  }

  function handleViewAllAlbums() {
    goto('/dashboard/albums');
  }

  function openExportModal(item = latestResult) {
    if (item?.status === 'sample') {
      showToast('info', t('dashboard.uploadBeforeShare'));
      return;
    }
    if (!item?.imageId || !item?.processedUrl) {
      showToast('info', t('dashboard.exportUnavailable'));
      return;
    }
    if (item?.status === 'failed') {
      showToast('info', t('dashboard.exportFailed'));
      return;
    }
    exportModalItem = item;
    exportModalOpen = true;
  }

  function handleViewResultRoute(item = latestResult) {
    if (!item?.imageId || item?.status === 'sample') {
      showToast('info', t('dashboard.uploadImageToView'));
      return;
    }
    goto(`/dashboard/results/${item.imageId}`);
  }

  async function handleExportVariant(format, item = exportModalItem || latestResult) {
    if (!item?.imageId) {
      showToast('info', t('dashboard.exportUnavailable'));
      return;
    }

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

  async function handleDeleteHistory(item) {
    if (!item?.imageId) return;
    const confirmed = window.confirm(t('dashboard.deleteConfirm', { filename: item.filename }));
    if (!confirmed) return;

    try {
      await deleteHistoryItem(item.imageId);
      historyItems = historyItems.filter((entry) => entry.imageId !== item.imageId);
      if (latestResult?.imageId === item.imageId) {
        latestResult = historyItems[0] || buildDefaultLatest();
        if (!historyItems.length) {
          latestResultHelper = t('dashboard.emptyLatestMessage');
        }
      }
      showToast('success', t('dashboard.historyDeleted'));
    } catch (error) {
      showToast('error', error?.message || t('common.somethingWentWrong'));
    }
  }

  function handleViewAllHistory() {
    goto('/dashboard/history');
  }

  function handleViewAlbum(albumSlug) {
    if (!albumSlug) {
      showToast('error', t('albums.routeUnavailable'));
      return;
    }
    goto(`/dashboard/albums/${albumSlug}`);
  }

  function handleLanguageChange(languageCode) {
    setLanguage(languageCode);
    showToast('success', t('dashboard.languageChanged'));
  }

  function handleLogout() {
    AUTH_STORAGE_KEYS.forEach((key) => {
      localStorage.removeItem(key);
      sessionStorage.removeItem(key);
    });
    clearPendingGuestImage();
    showToast('success', t('dashboard.logoutSuccessful'));
    setTimeout(() => goto('/login'), 250);
  }

  onMount(async () => {
    if (!getStoredToken()) {
      goto('/login');
      return;
    }

    await loadUserFallback();
    await bootstrapDashboard();
    await loadCollectionsPreview();
    updateBatchSummary();
  });

  onDestroy(() => {
    clearTimeout(toastTimer);
    stopBatchPolling();
  });

  function openCreateCollectionModal() {
    collectionModalMode = 'create';
    collectionModalOpen = true;
    selectedCollectionId = null;
    newCollectionName = '';
  }

  function openAddToCollectionModal() {
    if (!latestCompletedResult?.imageId) {
      showToast('info', t('collections.processBeforeAdd'));
      return;
    }
    collectionModalMode = 'add';
    collectionModalOpen = true;
    selectedCollectionId = collections[0]?.id || null;
    newCollectionName = '';
  }

  function closeCollectionModal() {
    collectionModalOpen = false;
    selectedCollectionId = null;
    newCollectionName = '';
  }

  async function handleCreateCollection() {
    if (!newCollectionName.trim()) return;
    creatingCollection = true;
    try {
      const created = await createCollection(newCollectionName.trim());
      await loadCollectionsPreview();
      selectedCollectionId = created?.id || selectedCollectionId;
      newCollectionName = '';
      showToast('success', t('collections.created'));
    } catch (error) {
      showToast('error', error?.message || t('collections.createFailed'));
    } finally {
      creatingCollection = false;
    }
  }

  async function handleAddLatestToCollection() {
    if (!latestCompletedResult?.imageId) {
      showToast('info', t('collections.processBeforeAdd'));
      return;
    }
    if (!selectedCollectionId) {
      showToast('info', t('collections.selectFirst'));
      return;
    }

    addingToCollection = true;
    try {
      await addCollectionItem(selectedCollectionId, latestCompletedResult.imageId);
      await loadCollectionsPreview();
      showToast('success', t('collections.latestAdded'));
      closeCollectionModal();
    } catch (error) {
      showToast('error', error?.message || t('collections.addFailed'));
    } finally {
      addingToCollection = false;
    }
  }

  async function handleAddLatestToSpecificCollection(collectionId) {
    if (!latestCompletedResult?.imageId) {
      showToast('info', t('collections.processBeforeAdd'));
      return;
    }
    addingToCollection = true;
    try {
      await addCollectionItem(collectionId, latestCompletedResult.imageId);
      await loadCollectionsPreview();
      showToast('success', t('collections.latestAdded'));
    } catch (error) {
      showToast('error', error?.message || t('collections.addFailed'));
    } finally {
      addingToCollection = false;
    }
  }

  async function handleGenerateDeliveryPack() {
    if (!latestCompletedResult?.imageId) {
      showToast('info', t('delivery.emptyMessage'));
      return;
    }

    generatingDeliveryPack = true;
    try {
      const payload = await createDeliveryPack(latestCompletedResult.imageId);
      latestDeliveryPackId = payload?.pack_id || null;
      latestDeliveryPackUrl = payload?.download_url || '';
      showToast('success', t('delivery.ready'));
    } catch (error) {
      showToast('error', error?.message || t('delivery.generateFailed'));
    } finally {
      generatingDeliveryPack = false;
    }
  }

  async function handleDownloadDeliveryPack() {
    if (!latestDeliveryPackId) {
      showToast('info', t('delivery.generateFirst'));
      return;
    }

    downloadingDeliveryPack = true;
    try {
      await downloadDeliveryPack(latestDeliveryPackId);
      showToast('success', t('delivery.downloaded'));
    } catch (error) {
      showToast('error', error?.message || t('delivery.downloadFailed'));
    } finally {
      downloadingDeliveryPack = false;
    }
  }

  function handleViewCollection(collectionId) {
    if (!collectionId) return;
    goto(`/dashboard/collections/${collectionId}`);
  }

  function handleViewAllCollections() {
    goto('/dashboard/collections');
  }
</script>

<svelte:head>
  <title>{t('dashboard.title')} | GlassClear</title>
</svelte:head>

{#if toast}
  <Toast {toast} onDismiss={() => (toast = null)} />
{/if}

<input
  bind:this={batchFileInput}
  type="file"
  accept=".jpg,.jpeg,.png,.webp"
  multiple
  hidden
  onchange={handleBatchFilesSelected}
/>

<div class="gc-dashboard-page">
  <div class="gc-dashboard-shell">
    <DashboardTopbar
      title={pageLabels.title}
      searchValue={searchQuery}
      searchPlaceholder={pageLabels.searchPlaceholder}
      uploadLabel={pageLabels.uploadImage}
      languageLabel={pageLabels.language}
      languageOptions={LANGUAGE_OPTIONS}
      {currentLanguage}
      userName={getDisplayName(currentUser)}
      userInitial={getUserInitial(currentUser)}
      logoutLabel={pageLabels.logout}
      onSearch={(value) => (searchQuery = value)}
      onUpload={handleUploadNavigation}
      onLanguageChange={handleLanguageChange}
      onLogout={handleLogout}
    />

    {#if workspaceLoaded}
      <main class="gc-dashboard-grid">
        <LatestResultCard
          item={latestResult}
          hasImage={Boolean(latestResult?.originalUrl || latestResult?.processedUrl)}
          helperMessage={latestResultIsSample ? t('dashboard.uploadImageToView') : latestResultHelper}
          disableView={latestResultIsSample}
          disableExport={latestResultIsSample}
          labels={pageLabels.latest}
          onView={() => handleViewResultRoute(latestResult)}
          onExport={() => openExportModal(latestResult)}
          onUpload={handleUploadNavigation}
        />

        <BatchProcessingPanel
          queue={batchQueue}
          summary={batchSummary}
          notice={batchNotice}
          overallProgress={batchOverallProgress}
          disablePick={currentBatchStatus === 'processing' || batchQueue.length >= MAX_BATCH_FILES}
          disableStart={!batchCanStart}
          disableClear={!batchCanClear}
          disableDownload={!batchCanDownload}
          labels={pageLabels.batch}
          onPickFiles={handleBatchPickFiles}
          onStart={handleBatchStart}
          onClear={handleBatchClear}
          onDownloadZip={handleBatchDownload}
        />

        <SmartAlbumsPanel
          albums={dashboardAlbums}
          labels={pageLabels.albums}
          showViewAll={true}
          onViewAll={handleViewAllAlbums}
          onViewAlbum={handleViewAlbum}
        />

        <HistoryPanel
          items={filteredHistory.slice(0, 2)}
          variant="preview"
          labels={pageLabels.history}
          showViewAll={true}
          onViewAll={handleViewAllHistory}
          onView={handleViewResultRoute}
          onExport={openExportModal}
          onDelete={handleDeleteHistory}
        />

        <DeliveryPackPanel
          latestResult={latestCompletedResult}
          latestResultLabel={latestCompletedResultLabel}
          helperMessage={latestDeliveryPackUrl ? t('delivery.latestReady') : t('delivery.historyGenerate')}
          canGenerate={Boolean(latestCompletedResult)}
          canDownload={Boolean(latestDeliveryPackId)}
          generating={generatingDeliveryPack}
          downloading={downloadingDeliveryPack}
          onGenerate={handleGenerateDeliveryPack}
          onDownload={handleDownloadDeliveryPack}
        />

        <CollectionsPanel
          collections={dashboardCollections}
          showViewAll={true}
          creating={creatingCollection}
          addingLatest={addingToCollection}
          latestResultAvailable={Boolean(latestCompletedResult)}
          onCreate={openCreateCollectionModal}
          onAddLatest={openAddToCollectionModal}
          onAddLatestToCollection={handleAddLatestToSpecificCollection}
          onOpenCollection={handleViewCollection}
          onViewAll={handleViewAllCollections}
        />
      </main>
    {/if}
  </div>
</div>

<CollectionPickerModal
  open={collectionModalOpen}
  collections={collections}
  creating={creatingCollection}
  adding={addingToCollection}
  latestResultAvailable={Boolean(latestCompletedResult)}
  bind:newCollectionName
  bind:selectedCollectionId
  mode={collectionModalMode}
  onClose={closeCollectionModal}
  onChoose={(collectionId) => {
    selectedCollectionId = collectionId;
  }}
  onAdd={handleAddLatestToCollection}
  onCreate={handleCreateCollection}
/>

<ExportResultModal
  open={exportModalOpen}
  item={exportModalItem}
  busy={exportModalBusy}
  labels={pageLabels.exportModal}
  onClose={() => {
    exportModalOpen = false;
  }}
  onJpg={() => handleExportVariant('jpg', exportModalItem)}
  onPng={() => handleExportVariant('png', exportModalItem)}
  onHd={() => handleExportVariant('hd', exportModalItem)}
  onComparison={() => handleExportVariant('comparison', exportModalItem)}
/>

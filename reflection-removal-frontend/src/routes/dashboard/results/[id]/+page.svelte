<svelte:options runes={false} />

<script>
  import '../../../../styles/dashboard.css';

  import { goto } from '$app/navigation';
  import { onDestroy, onMount } from 'svelte';
  import ImageCompare from '$lib/components/ImageCompare.svelte';
  import Toast from '$lib/components/dashboard/Toast.svelte';
  import { t } from '$lib/stores/language.js';
  import { downloadExportVariant, getWorkspaceImage, withBase } from '$lib/api/dashboardApi.js';
  import { getStoredToken } from '$lib/api/api.js';

  export let data;

  let resultItem = null;
  let toast = null;
  let toastTimer;
  let quickDownloadBusy = false;
  let selectedFormat = 'png';
  let labels = {};

  $: labels = {
    exportOptions: t('resultDetail.exportOptions'),
    download: t('common.download'),
    downloadPng: t('common.downloadPng'),
    downloadJpg: t('common.downloadJpg'),
    downloadHd: t('common.downloadHd'),
    original: t('common.original'),
    title: t('resultDetail.title'),
    kicker: t('resultDetail.kicker'),
    subtitle: t('resultDetail.subtitle'),
    statusReady: t('resultDetail.statusReady'),
    changeImage: t('resultDetail.changeImage'),
    aiStatus: t('resultDetail.aiStatus'),
    uploadComplete: t('resultDetail.uploadComplete'),
    processed: t('resultDetail.processed'),
    exportReady: t('resultDetail.exportReady'),
    resolution: t('resultDetail.resolution'),
    format: t('resultDetail.format'),
    mode: t('resultDetail.mode'),
    processedOn: t('resultDetail.processedOn'),
    exportTitle: t('resultDetail.exportTitle'),
    exportHelp: t('resultDetail.exportHelp'),
    exportNote: t('resultDetail.exportNote'),
    downloading: t('resultDetail.downloading')
  };

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

  function getResolutionLabel(item = resultItem) {
    if (!item) return t('common.notAvailable');
    if (item.width && item.height) return `${item.width} x ${item.height}`;
    return t('common.notAvailable');
  }

  function getFileFormatLabel(item = resultItem) {
    const filename = item?.filename || '';
    const extension = filename.includes('.') ? filename.split('.').pop() : '';
    return extension ? extension.toUpperCase() : selectedFormat.toUpperCase();
  }

  function getModeLabel(item = resultItem) {
    return item?.mode || t('resultDetail.standardMode');
  }

  function getStatusLabel(item = resultItem) {
    if (!item?.status) return t('common.ready');
    return item.status
      .split('_')
      .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
      .join(' ');
  }

  function mapItem(source = {}) {
    return {
      id: source.id,
      imageId: source.id,
      title: source.title || source.display_name || null,
      filename: source.filename || t('resultDetail.title'),
      originalUrl: normalizeUrl(source.original_url),
      processedUrl: normalizeUrl(source.processed_url),
      thumbnail: normalizeUrl(source.thumbnail_url || source.processed_url || source.original_url),
      processedAt: source.created_at,
      processedAtLabel: formatDate(source.created_at),
      status: (source.status || 'completed').toLowerCase(),
      width: source.width || null,
      height: source.height || null,
      mode: source.mode || source.processing_mode || source.category || null
    };
  }

  async function loadResult() {
    const payload = await getWorkspaceImage(data.id);
    resultItem = payload?.item ? mapItem(payload.item) : null;
  }

  async function handleQuickDownload() {
    if (!resultItem?.imageId || quickDownloadBusy) return;
    quickDownloadBusy = true;
    try {
      await downloadExportVariant(resultItem.imageId, selectedFormat);
      showToast('success', t('dashboard.exportDownloaded'));
    } catch (error) {
      showToast('error', error?.message || t('common.somethingWentWrong'));
    } finally {
      quickDownloadBusy = false;
    }
  }

  async function handleFormatDownload(format) {
    selectedFormat = format;
    await handleQuickDownload();
  }

  onMount(async () => {
    if (!getStoredToken()) {
      goto('/login');
      return;
    }

    await loadResult().catch((error) => {
      showToast('error', error?.message || t('common.somethingWentWrong'));
      goto('/dashboard');
    });
  });

  onDestroy(() => {
    clearTimeout(toastTimer);
  });
</script>

<script context="module">
  export async function load({ params }) {
    return { id: params.id };
  }
</script>

<svelte:head>
  <title>{labels.title}</title>
</svelte:head>

{#if toast}
  <Toast {toast} onDismiss={() => (toast = null)} />
{/if}

<div class="gc-dashboard-page gc-result-page">
  <div class="gc-result-shell">
{#if resultItem}
      <div class="gc-result-topbar">
        <button type="button" class="gc-result-backlink" onclick={() => goto('/dashboard')}>
          <span aria-hidden="true">&#8592;</span>
          <span>{labels.kicker}</span>
        </button>
      </div>

      <section class="gc-result-hero">
        <div class="gc-result-hero__media">
          <div class="gc-result-hero__frame">
            <div class="gc-result-hero__compare">
              <div class="gc-result-hero__eyebrows">
                <span>{labels.original}</span>
                <span>{t('common.output')}</span>
              </div>

              <ImageCompare
                originalImage={resultItem.originalUrl}
                processedImage={resultItem.processedUrl}
                beforeLabel={labels.original}
                afterLabel={t('common.output')}
              />
            </div>
          </div>
        </div>

        <aside class="gc-result-hero__panel">
          <div class="gc-result-hero__header">
            <div class="gc-result-badge">
              <span class="gc-result-badge__dot"></span>
              {labels.statusReady}
            </div>

            <button type="button" class="gc-result-change" onclick={() => goto('/dashboard')}>
              {labels.changeImage}
            </button>
          </div>

          <div class="gc-result-intro">
            <h1>{labels.title}</h1>
            <p>{labels.subtitle}</p>
          </div>

          <div class="gc-result-status">
            <span class="gc-result-status__label">{labels.aiStatus}</span>
            <strong>{t('resultDetail.readyForExport', { status: getStatusLabel() })}</strong>
          </div>

          <div class="gc-result-progress">
            <div class="gc-result-progress__chips">
              <span class="gc-result-progress__chip is-done">{labels.uploadComplete}</span>
              <span class="gc-result-progress__chip is-done">{labels.processed}</span>
              <span class="gc-result-progress__chip is-active">{labels.exportReady}</span>
            </div>
            <div class="gc-result-progress__bar">
              <div class="gc-result-progress__fill"></div>
            </div>
          </div>

          <div class="gc-result-summary">
            <div class="gc-result-summary__item">
              <span>{labels.resolution}</span>
              <strong>{getResolutionLabel()}</strong>
            </div>
            <div class="gc-result-summary__item">
              <span>{labels.format}</span>
              <strong>{getFileFormatLabel()}</strong>
            </div>
            <div class="gc-result-summary__item">
              <span>{labels.mode}</span>
              <strong>{getModeLabel()}</strong>
            </div>
            <div class="gc-result-summary__item">
              <span>{labels.processedOn}</span>
              <strong>{resultItem.processedAtLabel}</strong>
            </div>
          </div>

          <div class="gc-result-export">
            <div class="gc-result-export__top">
              <div>
                <span class="gc-result-export__eyebrow">{labels.exportTitle}</span>
                <p>{labels.exportHelp}</p>
              </div>

              <select bind:value={selectedFormat} class="gc-result-select" aria-label={labels.exportOptions}>
                <option value="png">PNG</option>
                <option value="jpg">JPG</option>
                <option value="hd">HD</option>
              </select>
            </div>

            <button
              type="button"
              class:gc-result-download--busy={quickDownloadBusy}
              class="gc-result-download"
              aria-busy={quickDownloadBusy}
              onclick={handleQuickDownload}
            >
              {quickDownloadBusy ? labels.downloading : labels.download}
            </button>

            <div class="gc-export-actions">
              <button type="button" class="gc-export-button gc-export-button--primary" onclick={() => handleFormatDownload('png')}>
                {labels.downloadPng}
              </button>
              <button type="button" class="gc-export-button" onclick={() => handleFormatDownload('jpg')}>
                {labels.downloadJpg}
              </button>
              <button type="button" class="gc-export-button" onclick={() => handleFormatDownload('hd')}>
                {labels.downloadHd}
              </button>
            </div>

            <p class="gc-result-export__note">{labels.exportNote}</p>
          </div>
        </aside>
      </section>
    {/if}
  </div>
</div>

<style>
  :global(body) {
    background:
      radial-gradient(circle at top, rgba(255, 255, 255, 0.98), rgba(248, 250, 252, 0.96) 46%, rgba(226, 232, 240, 0.92) 100%);
  }

  .gc-result-page {
    min-height: auto;
    padding: 0;
    background: transparent;
  }

  .gc-result-shell {
    max-width: 1320px;
    margin: 0 auto;
    padding: 28px 24px 80px;
  }

  .gc-result-topbar {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 18px;
    flex-wrap: wrap;
  }

  .gc-result-backlink {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 0;
    border: 0;
    background: transparent;
    color: #0f172a;
    font: inherit;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
  }

  .gc-result-backlink:hover {
    color: #4f46e5;
  }

  .gc-result-backlink span:first-child {
    color: #334155;
  }

  .gc-result-hero {
    display: grid;
    grid-template-columns: minmax(0, 1.3fr) minmax(340px, 0.78fr);
    gap: 28px;
    align-items: stretch;
    padding: 1.6rem;
    border-radius: 32px;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(248, 250, 252, 0.96));
    border: 1px solid rgba(226, 232, 240, 0.92);
    box-shadow: 0 24px 64px rgba(79, 70, 229, 0.12);
  }

  .gc-result-hero__media,
  .gc-result-hero__panel {
    min-width: 0;
  }

  .gc-result-hero__frame {
    position: relative;
    height: 100%;
    min-height: 540px;
    padding: 1.35rem;
    border-radius: 26px;
    background: linear-gradient(180deg, #ffffff, #f8fafc);
    border: 1px solid rgba(226, 232, 240, 0.94);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.92);
  }

  .gc-result-hero__compare {
    position: relative;
    height: 100%;
    border-radius: 24px;
    overflow: hidden;
    background: rgba(248, 250, 252, 0.95);
    border: 1px solid rgba(226, 232, 240, 0.94);
  }

  .gc-result-hero__eyebrows {
    position: absolute;
    inset: 16px 16px auto 16px;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    pointer-events: none;
  }

  .gc-result-hero__eyebrows span {
    display: inline-flex;
    align-items: center;
    padding: 0.45rem 0.9rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(148, 163, 184, 0.24);
    color: #334155;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .gc-result-hero__panel {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 1rem;
  }

  .gc-result-hero__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .gc-result-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.9rem;
    border-radius: 999px;
    background: #eef2ff;
    border: 1px solid rgba(99, 102, 241, 0.16);
    color: #4f46e5;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }

  .gc-result-badge__dot {
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 999px;
    background: #6366f1;
  }

  .gc-result-change {
    border: 1px solid rgba(203, 213, 225, 0.9);
    background: #ffffff;
    color: #111827;
    border-radius: 999px;
    padding: 0.7rem 1rem;
    font: inherit;
    font-size: 0.92rem;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
  }

  .gc-result-change:hover {
    transform: translateY(-1px);
    border-color: rgba(99, 102, 241, 0.28);
    box-shadow: 0 10px 24px rgba(79, 70, 229, 0.1);
  }

  .gc-result-intro {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .gc-result-intro h1 {
    margin: 0;
    color: #111827;
    font-size: clamp(1.9rem, 2.7vw, 3rem);
    font-weight: 800;
    letter-spacing: -0.045em;
  }

  .gc-result-intro p {
    margin: 0;
    color: #64748b;
    font-size: 1rem;
    line-height: 1.7;
  }

  .gc-result-status,
  .gc-result-progress,
  .gc-result-export {
    padding: 1rem 1.05rem;
    border-radius: 22px;
    background: #ffffff;
    border: 1px solid rgba(226, 232, 240, 0.92);
  }

  .gc-result-status {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .gc-result-status__label,
  .gc-result-export__eyebrow {
    color: #6366f1;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }

  .gc-result-status strong {
    color: #111827;
    font-size: 1rem;
    font-weight: 700;
  }

  .gc-result-progress {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
  }

  .gc-result-progress__chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
  }

  .gc-result-progress__chip {
    display: inline-flex;
    align-items: center;
    padding: 0.42rem 0.75rem;
    border-radius: 999px;
    background: #f8fafc;
    color: #64748b;
    border: 1px solid rgba(203, 213, 225, 0.92);
    font-size: 0.76rem;
    font-weight: 700;
  }

  .gc-result-progress__chip.is-done {
    background: #f0fdf4;
    color: #166534;
    border-color: rgba(34, 197, 94, 0.24);
  }

  .gc-result-progress__chip.is-active {
    background: #eef2ff;
    color: #4f46e5;
    border-color: rgba(99, 102, 241, 0.2);
  }

  .gc-result-progress__bar {
    width: 100%;
    height: 10px;
    border-radius: 999px;
    background: #e5e7eb;
    overflow: hidden;
  }

  .gc-result-progress__fill {
    width: 100%;
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
  }

  .gc-result-summary {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }

  .gc-result-summary__item {
    display: grid;
    gap: 0.45rem;
    padding: 1rem;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(226, 232, 240, 0.92);
  }

  .gc-result-summary__item span {
    color: #64748b;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .gc-result-summary__item strong {
    color: #111827;
    font-size: 0.98rem;
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  .gc-result-export {
    display: grid;
    gap: 14px;
  }

  .gc-result-export__top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    flex-wrap: wrap;
  }

  .gc-result-export__top p,
  .gc-result-export__note {
    margin: 0;
    color: #64748b;
  }

  .gc-result-export__top p {
    margin-top: 0.35rem;
    font-size: 0.92rem;
    line-height: 1.6;
  }

  .gc-result-select {
    min-width: 124px;
    height: 46px;
    padding: 0 14px;
    border-radius: 16px;
    border: 1px solid rgba(148, 163, 184, 0.22);
    background: rgba(255, 255, 255, 0.96);
    color: #0f172a;
    font: inherit;
    font-weight: 700;
    outline: none;
    box-shadow: 0 8px 18px rgba(79, 70, 229, 0.08);
  }

  .gc-result-download,
  .gc-export-button {
    min-height: 50px;
    padding: 0 18px;
    border-radius: 16px;
    border: 1px solid rgba(148, 163, 184, 0.22);
    background: rgba(255, 255, 255, 0.96);
    color: #334155;
    font: inherit;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease, background 0.18s ease;
  }

  .gc-result-download,
  .gc-export-button--primary {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    border-color: rgba(99, 102, 241, 0.18);
    color: #ffffff;
    box-shadow: 0 16px 32px rgba(79, 70, 229, 0.2);
  }

  .gc-result-download {
    width: 100%;
    justify-content: center;
  }

  .gc-result-download:hover,
  .gc-export-button:hover {
    transform: translateY(-1px);
  }

  .gc-result-download--busy {
    opacity: 0.8;
  }

  .gc-export-actions {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
  }

  .gc-result-export__note {
    font-size: 0.86rem;
    line-height: 1.6;
  }

  .gc-result-hero__compare :global(.ic) {
    min-height: 500px;
    height: 100%;
    background: rgba(248, 250, 252, 0.95);
  }

  .gc-result-hero__compare :global(.ic-layer) {
    background: transparent;
  }

  .gc-result-hero__compare :global(.ic-img) {
    width: 100%;
    height: min(620px, 72vh);
    object-fit: contain;
    background: transparent;
  }

  .gc-result-hero__compare :global(.ic-badge) {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(148, 163, 184, 0.22);
    color: #334155;
    box-shadow: none;
  }

  .gc-result-hero__compare :global(.ic-badge--after) {
    color: #0f172a;
    background: rgba(255, 255, 255, 0.92);
    border-color: rgba(148, 163, 184, 0.22);
  }

  .gc-result-hero__compare :global(.ic-line) {
    background: rgba(255, 255, 255, 0.98);
    box-shadow: 0 0 0 1px rgba(148, 163, 184, 0.18);
  }

  .gc-result-hero__compare :global(.ic-knob) {
    color: #0f172a;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.16);
  }

  @media (max-width: 1024px) {
    .gc-result-hero {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 720px) {
    .gc-result-shell {
      padding: 24px 16px 56px;
    }

    .gc-result-hero {
      padding: 1rem;
    }

    .gc-result-hero__frame {
      min-height: 360px;
      padding: 0.9rem;
    }

    .gc-result-hero__eyebrows {
      inset: 12px 12px auto 12px;
      flex-direction: column;
      align-items: flex-start;
    }

    .gc-result-hero__compare :global(.ic),
    .gc-result-hero__compare :global(.ic-img) {
      min-height: 320px;
      height: 320px;
    }

    .gc-result-hero__header,
    .gc-result-export__top {
      flex-direction: column;
      align-items: stretch;
    }

    .gc-result-select,
    .gc-result-change {
      width: 100%;
    }

    .gc-result-summary,
    .gc-export-actions {
      grid-template-columns: 1fr;
    }
  }
</style>

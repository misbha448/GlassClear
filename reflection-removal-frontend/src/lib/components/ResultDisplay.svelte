<script>
  import { fade } from 'svelte/transition';
  import ImageCompare from './ImageCompare.svelte';
  import { t } from '$lib/state.svelte.js';

  let {
    originalImage = '',
    processedImage = '',
    downloadFilename = '',
    predictionId = null,
    downloadHandler = null,
    aiMode = { selected_mode: 'fidelity', reason: 'No specific reason.' },
    confidenceMap = null,
    ssim = 0.0,
    edgeScore = 0.0,
    intermediateOutputs = [],
    processingSteps = []
  } = $props();

  let selectedFormat = $state('png');
  let selectedQuality = $state('High');

  const displayedProcessedImage = $derived(processedImage);

  function requestDownload(format = 'png') {
    if (typeof downloadHandler === 'function') {
      downloadHandler(format);
      return;
    }
    triggerDownload(format);
  }

  function buildDownloadName(format = 'png') {
    const sourceName = downloadFilename || processedImage.split('/').pop() || `GC_${predictionId || 'Result'}.png`;
    const baseName = sourceName.replace(/\.[^.]+$/, '');
    return `${baseName}.${format}`;
  }

  async function triggerDownload(format = 'png') {
    try {
      const response = await fetch(displayedProcessedImage);
      const blob = await response.blob();
      let finalBlob = blob;
      let extension = 'png';

      if (format === 'jpg') {
        extension = 'jpg';
        const img = await createImageBitmap(blob);
        const canvas = document.createElement('canvas');
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);
        finalBlob = await new Promise((resolve) => canvas.toBlob(resolve, 'image/jpeg', 0.95));
      }

      const url = window.URL.createObjectURL(finalBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = buildDownloadName(extension);
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download failed:', err);
    }
  }

  function handleBack() {
    if (typeof window !== 'undefined') {
      window.history.back();
    }
  }

  function getResolutionLabel() {
    return '4096 x 2160';
  }

  function getFormatLabel() {
    return selectedFormat.toUpperCase();
  }

  function getModeLabel() {
    return aiMode?.selected_mode ? String(aiMode.selected_mode).toUpperCase() : 'FIDELITY';
  }

  function getProcessedDateLabel() {
    return new Date().toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }
</script>

<div class="rd" transition:fade>
  <!-- ── Main card: two columns ── -->
  <div class="rd-card">
    <div class="rd-grid">

      <!-- LEFT: Before/After comparison -->
      <section class="rd-left">
        <div class="rd-col-header">
          <div class="rd-col-header-text">
            <h2 class="rd-col-title">{t('dashboard.beforeAfter')}</h2>
            <p class="rd-col-sub">{t('resultDetail.compareSummary')}</p>
          </div>
          <div class="rd-pill-group">
            <span class="rd-pill rd-pill--muted">{t('common.original')}</span>
            <span class="rd-pill rd-pill--accent">GlassClear</span>
          </div>
        </div>

        <div class="rd-slider-stage">
          <ImageCompare
            originalImage={originalImage}
            processedImage={displayedProcessedImage}
            beforeLabel={t('common.original')}
            afterLabel={t('common.output')}
          />
        </div>
      </section>

      <!-- RIGHT: Summary + Export -->
      <aside class="rd-right">

        <!-- Result Summary -->
        <div class="rd-right-block">
          <div class="rd-col-header">
            <div class="rd-col-header-text">
              <h2 class="rd-col-title">{t('resultDetail.summary')}</h2>
              <p class="rd-col-sub">{t('resultDetail.exportHelp')}</p>
            </div>
            <div class="rd-pill-group">
              <span class="rd-pill rd-pill--green">
                <span class="rd-pill-dot"></span>
                {t('processing.aiProcessing')}
              </span>
            </div>
          </div>

          <div class="rd-detail-list">
            <div class="rd-detail-row">
              <span class="rd-detail-key">{t('resultDetail.resolution')}</span>
              <strong class="rd-detail-val">{getResolutionLabel()}</strong>
            </div>
            <div class="rd-detail-row">
              <span class="rd-detail-key">{t('resultDetail.format')}</span>
              <strong class="rd-detail-val">{getFormatLabel()}</strong>
            </div>
            <div class="rd-detail-row">
              <span class="rd-detail-key">{t('resultDetail.mode')}</span>
              <strong class="rd-detail-val">{getModeLabel()}</strong>
            </div>
            <div class="rd-detail-row">
              <span class="rd-detail-key">{t('resultDetail.processedOn')}</span>
              <strong class="rd-detail-val">{getProcessedDateLabel()}</strong>
            </div>
          </div>
        </div>

        <div class="rd-sep"></div>

        <!-- Export Output -->
        <div class="rd-right-block">
          <h3 class="rd-section-title">{t('resultDetail.exportTitle')}</h3>

          <div class="rd-quality-row">
            <span class="rd-export-label">{t('common.quality')}</span>
            <select id="result-quality" bind:value={selectedQuality} class="rd-select rd-select--wide" aria-label={t('common.quality')}>
              <option>{t('common.standard')}</option>
              <option>{t('common.high')}</option>
              <option>{t('common.ultra')}</option>
            </select>
          </div>

          <div class="rd-export-actions">
            <button type="button" class="rd-btn rd-btn--primary rd-btn--full" onclick={() => requestDownload('png')}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              {t('common.downloadPng')}
            </button>
            <div class="rd-btn-row">
              <button type="button" class="rd-btn rd-btn--secondary" onclick={() => requestDownload('jpg')}>
                {t('common.downloadJpg')}
              </button>
              <button type="button" class="rd-btn rd-btn--secondary" onclick={() => requestDownload('hd')}>
                {t('common.downloadHd')}
              </button>
            </div>
          </div>
        </div>

        <div class="rd-spacer"></div>

        <!-- AI Feedback -->
        <div class="rd-feedback">
          <div class="rd-feedback-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
          </div>
          <p class="rd-feedback-text">{t('result.feedback')}</p>
        </div>

      </aside>
    </div>
  </div>
</div>

<style>
  .rd {
    max-width: 1320px;
    margin: 0 auto;
    padding: 24px 24px 72px;
    font-family: 'Inter', 'DM Sans', system-ui, sans-serif;
    -webkit-font-smoothing: antialiased;
  }

  /* ── Main card ── */
  .rd-card {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(148, 163, 184, 0.20);
    border-radius: 32px;
    box-shadow:
      0 2px 8px rgba(79, 70, 229, 0.04),
      0 20px 60px rgba(79, 70, 229, 0.11);
    padding: 24px;
  }

  /* ── Grid ── */
  .rd-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 380px;
    gap: 20px;
    align-items: stretch;
  }

  /* ── Left column ── */
  .rd-left {
    display: flex;
    flex-direction: column;
    gap: 16px;
    min-width: 0;
  }

  /* ── Right column ── */
  .rd-right {
    display: flex;
    flex-direction: column;
    gap: 0;
    background: rgba(248, 250, 252, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 22px;
    padding: 22px;
    min-width: 0;
  }

  .rd-right-block {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .rd-sep {
    height: 1px;
    background: rgba(148, 163, 184, 0.18);
    margin: 20px 0;
  }

  /* ── Column headers ── */
  .rd-col-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
  }
  .rd-col-header-text { flex: 1; min-width: 0; }

  .rd-col-title {
    margin: 0 0 3px;
    font-size: 15px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;
  }
  .rd-col-sub {
    margin: 0;
    font-size: 12.5px;
    color: #64748b;
    font-weight: 400;
  }

  /* ── Pills ── */
  .rd-pill-group {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
  }
  .rd-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 600;
    white-space: nowrap;
  }
  .rd-pill--muted {
    background: rgba(148, 163, 184, 0.13);
    color: #475569;
    border: 1px solid rgba(148, 163, 184, 0.22);
  }
  .rd-pill--accent {
    background: rgba(99, 102, 241, 0.09);
    color: #4f46e5;
    border: 1px solid rgba(99, 102, 241, 0.18);
  }
  .rd-pill--green {
    background: rgba(34, 197, 94, 0.09);
    color: #16a34a;
    border: 1px solid rgba(34, 197, 94, 0.20);
  }
  .rd-pill-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #16a34a;
    box-shadow: 0 0 5px rgba(34, 197, 94, 0.5);
  }

  /* ── Slider stage ── */
  .rd-slider-stage {
    flex: 1;
    border-radius: 18px;
    overflow: hidden;
    background: #f8fafc;
    border: 1px solid rgba(148, 163, 184, 0.16);
    min-height: 480px;
  }

  .rd-slider-stage :global(*) { box-sizing: border-box; }

  .rd-slider-stage :global(.ic) {
    width: 100% !important;
    height: 100% !important;
    min-height: 480px;
    background: #f8fafc;
  }
  .rd-slider-stage :global(.ic-layer) {
    background: transparent;
  }
  .rd-slider-stage :global(.ic-img) {
    width: 100% !important;
    height: 100% !important;
    min-height: 480px;
    object-fit: cover;
    background: transparent;
    filter: none !important;
  }
  .rd-slider-stage :global(.ic-badge) {
    background: rgba(255, 255, 255, 0.90);
    border: 1px solid rgba(148, 163, 184, 0.22);
    color: #334155;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.05em;
    box-shadow: none;
  }
  .rd-slider-stage :global(.ic-badge--after) {
    color: #0f172a;
    background: rgba(255, 255, 255, 0.90);
    border-color: rgba(148, 163, 184, 0.22);
  }
  .rd-slider-stage :global(.ic-line) {
    background: rgba(255, 255, 255, 0.95);
    box-shadow: 0 0 0 1px rgba(148, 163, 184, 0.20);
  }
  .rd-slider-stage :global(.ic-knob) {
    color: #0f172a;
    background: white;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.18);
  }

  /* ── Detail list ── */
  .rd-detail-list {
    display: flex;
    flex-direction: column;
  }
  .rd-detail-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(148, 163, 184, 0.13);
  }
  .rd-detail-row:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }
  .rd-detail-key {
    font-size: 13px;
    color: #64748b;
    font-weight: 400;
  }
  .rd-detail-val {
    font-size: 13px;
    font-weight: 700;
    color: #0f172a;
    text-align: right;
  }

  /* ── Export section ── */
  .rd-section-title {
    margin: 0;
    font-size: 14px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.01em;
  }
  .rd-quality-row {
    display: flex;
    flex-direction: column;
    gap: 7px;
  }
  .rd-export-label {
    font-size: 11px;
    font-weight: 600;
    color: #94a3b8;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  .rd-export-actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .rd-btn-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }

  /* ── Buttons ── */
  .rd-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    height: 42px;
    padding: 0 18px;
    border-radius: 13px;
    font-family: inherit;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.17s ease, box-shadow 0.17s ease, filter 0.17s ease;
    white-space: nowrap;
    letter-spacing: -0.005em;
  }
  .rd-btn--primary {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    border: none;
    color: #fff;
    box-shadow:
      0 6px 20px rgba(79, 70, 229, 0.30),
      inset 0 1px 0 rgba(255,255,255,0.14);
  }
  .rd-btn--primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(79, 70, 229, 0.40);
    filter: brightness(1.05);
  }
  .rd-btn--primary:active {
    transform: scale(0.976);
    filter: brightness(0.97);
  }
  .rd-btn--secondary {
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid rgba(148, 163, 184, 0.25);
    color: #334155;
  }
  .rd-btn--secondary:hover {
    transform: translateY(-1px);
    border-color: rgba(99, 102, 241, 0.28);
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.08);
  }
  .rd-btn--full { width: 100%; }

  /* ── Selects ── */
  .rd-select {
    height: 42px;
    padding: 0 14px;
    border-radius: 13px;
    border: 1px solid rgba(148, 163, 184, 0.22);
    background: rgba(255, 255, 255, 0.96);
    color: #0f172a;
    font-family: inherit;
    font-size: 13px;
    font-weight: 600;
    outline: none;
    cursor: pointer;
    transition: border-color 0.17s ease, box-shadow 0.17s ease;
    appearance: auto;
  }
  .rd-select:focus {
    border-color: rgba(99, 102, 241, 0.40);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.09);
  }
  .rd-select--wide { width: 100%; }

  .rd-spacer { flex: 1; min-height: 12px; }

  /* ── AI Feedback ── */
  .rd-feedback {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 13px 15px;
    background: rgba(99, 102, 241, 0.05);
    border: 1px solid rgba(99, 102, 241, 0.12);
    border-radius: 13px;
  }
  .rd-feedback-icon {
    flex-shrink: 0;
    width: 26px;
    height: 26px;
    border-radius: 8px;
    background: rgba(99, 102, 241, 0.10);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #6366f1;
    margin-top: 1px;
  }
  .rd-feedback-text {
    margin: 0;
    font-size: 12.5px;
    line-height: 1.65;
    color: #475569;
    font-weight: 400;
  }

  /* ── Responsive ── */
  @media (max-width: 1060px) {
    .rd-grid { grid-template-columns: minmax(0, 1fr) 340px; }
  }
  @media (max-width: 860px) {
    .rd-grid { grid-template-columns: 1fr; }
    .rd-card { padding: 18px; }
    .rd-slider-stage,
    .rd-slider-stage :global(.ic),
    .rd-slider-stage :global(.ic-img) { min-height: 380px; }
  }
  @media (max-width: 600px) {
    .rd { padding: 16px 14px 52px; }
    .rd-card { padding: 14px; border-radius: 22px; }
    .rd-right { border-radius: 16px; padding: 16px; }
    .rd-col-header { flex-direction: column; gap: 8px; }
    .rd-slider-stage,
    .rd-slider-stage :global(.ic),
    .rd-slider-stage :global(.ic-img) { min-height: 300px; }
  }
</style>

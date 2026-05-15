<script>
  import { fade, scale } from 'svelte/transition';
  import AIInsights from './AIInsights.svelte';
  import VersionTimeline from './VersionTimeline.svelte';
  import { t } from '$lib/state.svelte.js';

  let { 
    show = $bindable(false), 
    originalImage = "", 
    processedImage = "", 
    mode = "Quality" 
  } = $props();

  let sliderPos = $state(50);
  let downloadFormat = $state("JPG");
  let currentVersion = $state(mode);

  function close() {
    show = false;
  }

  function download() {
    const link = document.createElement('a');
    link.href = processedImage; // Note: For true conversion on old projects, backend re-processing would be needed
    link.download = `glassclear_${currentVersion.toLowerCase()}.${downloadFormat.toLowerCase()}`;
    link.click();
  }
</script>

{#if show}
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="cinematic-backdrop" transition:fade={{ duration: 300 }} onclick={close}>
    <div 
      class="viewer-container" 
      transition:scale={{ duration: 400, start: 0.9, opacity: 0 }}
      onclick={(e) => e.stopPropagation()}
    >
      <!-- Header Area -->
      <div class="viewer-header">
        <div class="project-meta">
          <span class="badge bg-primary me-2">{t('view_ai_proc')}</span>
          <h5 class="mb-0 text-white">{t('view_title')}</h5>
        </div>
        <div class="viewer-center">
          <VersionTimeline bind:currentVersion />
        </div>
        <div class="viewer-controls">
          <button class="btn-close-custom" onclick={close} aria-label="Close">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
      </div>

      <!-- Comparison Area -->
      <div class="comparison-viewport">
        <div class="image-layer after">
          <img src={processedImage} alt="Processed" />
          <div class="label after">{t('view_processed')} ({t('mode_' + currentVersion.toLowerCase())})</div>
        </div>
        <div 
          class="image-layer before" 
          style="clip-path: inset(0 0 0 {currentVersion === 'Original' ? 0 : sliderPos}%);"
        >
          <img src={originalImage} alt="Original" />
          <div class="label before">{t('studio_original')}</div>
        </div>

        {#if currentVersion !== 'Original'}
          <input 
            type="range" 
            min="0" max="100" 
            bind:value={sliderPos} 
            class="comparison-slider" 
          />
          
          <div class="slider-divider" style="left: {sliderPos}%">
            <div class="divider-line"></div>
            <div class="divider-handle">
              <i class="bi bi-chevron-left"></i>
              <i class="bi bi-chevron-right"></i>
            </div>
          </div>
        {/if}

        <!-- AI Insights Overlay -->
        <div class="insights-overlay">
          <AIInsights />
        </div>
      </div>

      <!-- Footer Area -->
      <div class="viewer-footer">
        <div class="footer-info">
          <p class="small text-white-50 mb-0">{t('view_drag')}</p>
        </div>
        <div class="d-flex align-items-center gap-3">
          <select bind:value={downloadFormat} class="form-select form-select-sm w-auto">
            <option value="JPG">JPG</option>
            <option value="PNG">PNG</option>
          </select>
        <button class="btn-download" onclick={download}>
          <i class="bi bi-download me-2"></i> {t('view_dl')}
        </button>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  .cinematic-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(15px);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }

  .viewer-container {
    width: 100%;
    max-width: 1200px;
    height: 90vh;
    background: #0a0a0c;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 50px 100px rgba(0, 0, 0, 0.8);
    transition: background 0.3s ease, border-color 0.3s ease;
  }

  :global([data-bs-theme='light']) .viewer-container {
    background: #fcfcfd !important;
    border-color: rgba(0, 0, 0, 0.1) !important;
  }

  .viewer-header {
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    transition: border-color 0.3s ease;
  }

  :global([data-bs-theme='light']) .viewer-header {
    border-color: rgba(0, 0, 0, 0.05) !important;
  }

  .viewer-center {
    flex: 1;
    display: flex;
    justify-content: center;
  }

  .viewer-controls {
    display: flex;
    align-items: center;
    gap: 1.5rem;
  }

  .mode-toggle {
    background: rgba(255, 255, 255, 0.05);
    padding: 4px;
    border-radius: 12px;
    display: flex;
  }

  .mode-toggle button {
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.5);
    padding: 6px 16px;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    transition: all 0.2s;
  }

  .mode-toggle button.active {
    background: #6366f1;
    color: white;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  }

  .btn-close-custom {
    background: rgba(255, 255, 255, 0.05);
    border: none;
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.3s ease, transform 0.3s ease, color 0.3s ease;
  }

  .btn-close-custom:hover {
    background: rgba(239, 68, 68, 0.2);
    color: #ef4444;
    transform: rotate(90deg);
  }

  :global([data-bs-theme='light']) .viewer-header h5,
  :global([data-bs-theme='light']) .viewer-header .badge { color: #18181b !important; }

  .comparison-viewport {
    flex: 1;
    position: relative;
    background: #000;
    overflow: hidden;
  }

  .image-layer {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .image-layer img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
  }

  .label {
    position: absolute;
    bottom: 2rem;
    padding: 8px 16px;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
    border-radius: 50px;
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    z-index: 10;
  }

  .label.after { left: 2rem; }
  .label.before { right: 2rem; }

  .comparison-slider {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: col-resize;
    z-index: 30;
  }

  .slider-divider {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 2px;
    background: white;
    z-index: 20;
    pointer-events: none;
    transform: translateX(-50%);
  }

  .divider-line {
    height: 100%;
    width: 100%;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  }

  .divider-handle {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 48px;
    height: 48px;
    background: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #000;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
  }

  .viewer-footer {
    padding: 1.5rem 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: border-color 0.3s ease;
  }

  :global([data-bs-theme='light']) .viewer-footer {
    border-color: rgba(0, 0, 0, 0.05) !important;
  }

  :global([data-bs-theme='light']) .viewer-footer p {
    color: #52525b !important;
  }

  :global([data-bs-theme='light']) .viewer-footer select {
    background: rgba(0,0,0,0.05) !important;
    color: #18181b !important;
    border-color: rgba(0,0,0,0.1) !important;
  }

  .btn-download {
    background: linear-gradient(135deg, #6366f1, #a855f7);
    border: none;
    color: white;
    padding: 10px 24px;
    border-radius: 12px;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease, filter 0.3s ease;
  }

  .btn-download:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
    filter: brightness(1.1);
  }
  .btn-download:active { transform: translateY(0) scale(0.96); }

  .insights-overlay {
    position: absolute;
    top: 2rem;
    right: 2rem;
    z-index: 40;
    pointer-events: none;
  }
</style>
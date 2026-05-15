<script>
  import { onMount } from 'svelte';
  import { t } from '$lib/state.svelte.js';

  let {
    originalSrc = '',
    processedSrc = '',
    title = '',
    subtitle = '',
    onChangeImage = null
  } = $props();

  const statusMessages = [
    () => t('processing.statusUploadComplete'),
    () => t('processing.statusScanning'),
    () => t('processing.statusRemoving'),
    () => t('processing.statusFinalizing')
  ];

  let statusIndex = $state(0);
  let progressValue = $state(22);

  const displayedImage = $derived(processedSrc || originalSrc);
  const panelTitle = $derived(title || t('processing.title'));
  const panelSubtitle = $derived(subtitle || t('processing.subtitle'));

  onMount(() => {
    const statusTimer = setInterval(() => {
      statusIndex = (statusIndex + 1) % statusMessages.length;
    }, 2000);

    const progressTimer = setInterval(() => {
      progressValue = progressValue < 92 ? progressValue + 14 : 92;
    }, 1400);

    return () => {
      clearInterval(statusTimer);
      clearInterval(progressTimer);
    };
  });
</script>

<section class="processing-shell" aria-live="polite">
  <div class="processing-card">
    <div class="processing-preview">
      {#if displayedImage}
        <div class="processing-preview__frame">
          <img src={displayedImage} alt={panelTitle} class="processing-image" />
          <div class="processing-scan" aria-hidden="true"></div>
        </div>
      {:else}
        <div class="processing-empty">{t('processing.preparingPreview')}</div>
      {/if}
    </div>

    <div class="processing-panel">
      <div class="processing-header">
        <div class="processing-header__top">
          <div class="processing-badge">
            <span class="processing-badge__dot"></span>
            {t('processing.badge')}
          </div>
          {#if typeof onChangeImage === 'function'}
            <button type="button" class="processing-change" onclick={onChangeImage}>
              {t('processing.changeImage')}
            </button>
          {/if}
        </div>

        <h3>{panelTitle}</h3>
        <p>{panelSubtitle}</p>
      </div>

      <div class="processing-status">
        <span class="processing-status__label">{t('processing.aiStatus')}</span>
        <strong>{statusMessages[statusIndex]()}</strong>
      </div>

      <div class="processing-progress">
        <div class="processing-progress__top">
          <span class="processing-progress__chip is-done">{t('processing.uploaded')}</span>
          <span class="processing-progress__chip is-active">{t('processing.processing')}</span>
          <span class="processing-progress__chip">{t('processing.finalizing')}</span>
        </div>
        <div class="processing-progress__bar">
          <div class="processing-progress__fill" style={`width:${progressValue}%`}></div>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .processing-shell {
    width: 100%;
    max-width: 1220px;
    margin: 1.5rem auto 0;
  }

  .processing-card {
    display: grid;
    grid-template-columns: minmax(0, 1.2fr) minmax(320px, 0.8fr);
    gap: 28px;
    align-items: stretch;
    padding: 1.6rem;
    background: linear-gradient(180deg, #ffffff, #f8fafc);
    border: 1px solid rgba(226, 232, 240, 0.92);
    border-radius: 28px;
    box-shadow: 0 22px 54px rgba(15, 23, 42, 0.08);
  }

  .processing-preview {
    min-width: 0;
  }

  .processing-preview__frame,
  .processing-empty {
    position: relative;
    min-height: 460px;
    height: 100%;
    display: grid;
    place-items: center;
    border-radius: 24px;
    background: linear-gradient(180deg, #ffffff, #f8fafc);
    border: 1px solid rgba(226, 232, 240, 0.94);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9);
    overflow: hidden;
  }

  .processing-image {
    width: 100%;
    max-height: 460px;
    object-fit: contain;
    display: block;
  }

  .processing-scan {
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(99, 102, 241, 0), rgba(99, 102, 241, 0.12), rgba(99, 102, 241, 0));
    transform: translateY(-100%);
    animation: scan 2.4s ease-in-out infinite;
    pointer-events: none;
  }

  .processing-empty {
    color: #64748b;
    font-size: 0.96rem;
    font-weight: 600;
  }

  .processing-panel {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 1rem;
    min-width: 0;
  }

  .processing-header {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .processing-header__top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .processing-badge {
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

  .processing-badge__dot {
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 999px;
    background: #6366f1;
  }

  .processing-change {
    border: 1px solid rgba(203, 213, 225, 0.9);
    background: #ffffff;
    color: #111827;
    border-radius: 999px;
    padding: 0.7rem 1rem;
    font: inherit;
    font-size: 0.92rem;
    font-weight: 700;
  }

  .processing-header h3 {
    margin: 0;
    color: #111827;
    font-size: clamp(1.7rem, 2.4vw, 2.35rem);
    font-weight: 800;
    letter-spacing: -0.04em;
  }

  .processing-header p {
    margin: 0;
    color: #64748b;
    font-size: 1rem;
    line-height: 1.65;
  }

  .processing-status,
  .processing-progress {
    padding: 1rem 1.05rem;
    border-radius: 20px;
    background: #ffffff;
    border: 1px solid rgba(226, 232, 240, 0.92);
  }

  .processing-status {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .processing-status__label {
    color: #6366f1;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
  }

  .processing-status strong {
    color: #111827;
    font-size: 1rem;
    font-weight: 700;
  }

  .processing-progress {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
  }

  .processing-progress__top {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
  }

  .processing-progress__chip {
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

  .processing-progress__chip.is-done {
    background: #f0fdf4;
    color: #166534;
    border-color: rgba(34, 197, 94, 0.24);
  }

  .processing-progress__chip.is-active {
    background: #eef2ff;
    color: #4f46e5;
    border-color: rgba(99, 102, 241, 0.2);
  }

  .processing-progress__bar {
    width: 100%;
    height: 10px;
    border-radius: 999px;
    background: #e5e7eb;
    overflow: hidden;
  }

  .processing-progress__fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    transition: width 0.8s ease;
  }

  @keyframes scan {
    0% { transform: translateY(-100%); opacity: 0; }
    15% { opacity: 1; }
    85% { opacity: 1; }
    100% { transform: translateY(100%); opacity: 0; }
  }

  @media (max-width: 900px) {
    .processing-card {
      grid-template-columns: 1fr;
    }

    .processing-preview__frame,
    .processing-empty {
      min-height: 320px;
    }
  }

  @media (max-width: 640px) {
    .processing-shell {
      margin-top: 1rem;
    }

    .processing-card {
      padding: 1rem;
    }

    .processing-preview__frame,
    .processing-empty {
      min-height: 260px;
    }
  }
</style>

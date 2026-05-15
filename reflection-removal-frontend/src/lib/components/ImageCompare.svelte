<script>
  import { t } from '$lib/state.svelte.js';
  let {
    originalImage = "",
    processedImage = "",
    beforeLabel = t('common.original'),
    afterLabel = t('common.output')
  } = $props();

  let sliderPos = $state(50);
</script>

<div class="ic">
  <!-- Base layer — processed (After) image -->
  <div class="ic-layer ic-layer--after">
    <img src={processedImage} alt={afterLabel} class="ic-img" />
  </div>

  <!-- Top layer — original (Before) image, clipped from left -->
  <div
    class="ic-layer ic-layer--before"
    style="clip-path: inset(0 {100 - sliderPos}% 0 0);"
  >
    <img src={originalImage} alt={beforeLabel} class="ic-img" />
  </div>

  <!-- Corner labels -->
  <span class="ic-badge ic-badge--before" aria-hidden="true">{beforeLabel}</span>
  <span class="ic-badge ic-badge--after"  aria-hidden="true">{afterLabel}</span>

  <!-- Invisible range input (covers full area for interaction) -->
  <input
    type="range"
    min="0"
    max="100"
    bind:value={sliderPos}
    class="ic-input"
    aria-label="Comparison slider"
  />

  <!-- Visual handle -->
  <div class="ic-handle" style="left: {sliderPos}%" aria-hidden="true">
    <div class="ic-line"></div>
    <div class="ic-knob">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M5.5 4L2 8l3.5 4M10.5 4L14 8l-3.5 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
  </div>
</div>

<style>
  /* ── Wrapper ── */
  .ic {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 10;
    background: linear-gradient(180deg, rgba(255,255,255,0.88), rgba(238,242,255,0.88));
    user-select: none;
    overflow: hidden;
    /* border-radius inherited from parent viewer-card */
  }

  /* ── Image layers ── */
  .ic-layer {
    position: absolute;
    inset: 0;
  }

  .ic-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
    pointer-events: none;
  }

  /* ── Corner badges ── */
  .ic-badge {
    position: absolute;
    top: 14px;
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    pointer-events: none;
    z-index: 15;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }

  .ic-badge--before {
    left: 14px;
    background: rgba(255, 255, 255, 0.86);
    border: 1px solid rgba(226, 232, 240, 0.92);
    color: #475569;
  }

  .ic-badge--after {
    right: 14px;
    background: #eef2ff;
    border: 1px solid rgba(99, 102, 241, 0.18);
    color: #4f46e5;
  }

  /* ── Range input (invisible interaction surface) ── */
  .ic-input {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: col-resize;
    z-index: 30;
    /* reset browser defaults */
    -webkit-appearance: none;
    appearance: none;
    margin: 0;
    padding: 0;
    background: transparent;
  }

  /* ── Divider handle ── */
  .ic-handle {
    position: absolute;
    top: 0;
    bottom: 0;
    z-index: 20;
    pointer-events: none;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  /* Vertical line */
  .ic-line {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 2px;
    background: rgba(255, 255, 255, 0.94);
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.22);
  }

  /* Knob */
  .ic-knob {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: #fff;
    color: #111827;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow:
      0 0 0 4px rgba(255, 255, 255, 0.4),
      0 10px 30px rgba(79, 70, 229, 0.18);
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }

  /* Hover effect via sibling selector on the input */
  .ic-input:hover ~ .ic-handle .ic-knob {
    box-shadow:
      0 0 0 5px rgba(99, 102, 241, 0.18),
      0 4px 24px rgba(99, 102, 241, 0.24);
    transform: translateY(-50%) scale(1.08);
  }
</style>

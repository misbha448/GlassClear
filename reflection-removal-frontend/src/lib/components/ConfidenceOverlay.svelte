<script>
  import { t } from '$lib/state.svelte.js';
  import { fade } from 'svelte/transition';

  let {
    processedImage = "",
    confidenceMap = "",
    showOverlay = $bindable(false)
  } = $props();
</script>

{#if showOverlay && confidenceMap}
  <div class="confidence-overlay-active" transition:fade>
    <div class="overlay-image-wrapper">
      <img src={confidenceMap} alt="Confidence Map" class="map-img" />
      <div class="heatmap-shimmer"></div>
    </div>
    
    <div class="overlay-legend-float">
      <div class="legend-item"><span class="dot high"></span> High</div>
      <div class="legend-item"><span class="dot med"></span> Med</div>
      <div class="legend-item"><span class="dot low"></span> Low</div>
    </div>
  </div>
{/if}

<style>
  .confidence-overlay-active {
    position: absolute;
    inset: 0;
    z-index: 10;
    background: rgba(0,0,0,0.4);
    pointer-events: none;
  }

  .overlay-image-wrapper {
    width: 100%;
    height: 100%;
    mix-blend-mode: screen;
    opacity: 0.6;
  }

  .map-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    filter: hue-rotate(180deg) saturate(2);
  }

  .overlay-legend-float {
    position: absolute;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 1.5rem;
    background: rgba(0,0,0,0.7);
    backdrop-filter: blur(10px);
    padding: 0.5rem 1.5rem;
    border-radius: 99px;
    border: 1px solid rgba(255,255,255,0.1);
  }

  .legend-item { font-size: 0.75rem; color: white; display: flex; align-items: center; gap: 0.4rem; }
  .dot { width: 8px; height: 8px; border-radius: 50%; }
  .high { background: #00ff00; box-shadow: 0 0 8px #00ff00; }
  .med { background: #ffff00; box-shadow: 0 0 8px #ffff00; }
  .low { background: #ff0000; box-shadow: 0 0 8px #ff0000; }
</style>
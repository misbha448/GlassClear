<script>
  import { t } from '$lib/state.svelte.js';
  import { fade } from 'svelte/transition';

  let { intermediateOutputs = [] } = $props();

  let currentStageIndex = $state(0);

  // Keep slider at the end when new outputs arrive
  $effect(() => {
    if (intermediateOutputs.length > 0) {
      currentStageIndex = intermediateOutputs.length - 1;
    }
  });

  let currentImage = $derived(intermediateOutputs[currentStageIndex]);
  let stageLabels = ["Stage 1: Initial", "Stage 2: Intermediate", "Stage 3: Final"];
  let currentStageLabel = $derived(stageLabels[currentStageIndex]);
</script>

<div class="refinement-slider-panel glass-card-nested p-3 mb-4" transition:fade>
  <h6 class="fw-bold mb-3 text-cyan">
    <i class="bi bi-layers-half me-2"></i> {t('progressive_refinement_title')}
  </h6>

  {#if intermediateOutputs.length > 0}
    <div class="image-preview-wrapper rounded-3 overflow-hidden mb-3">
      <img src={currentImage} alt={currentStageLabel} class="img-fluid" />
      <div class="stage-label badge bg-primary">{currentStageLabel}</div>
    </div>

    <input
      type="range"
      min="0"
      max={intermediateOutputs.length - 1}
      bind:value={currentStageIndex}
      class="form-range custom-range-slider"
    />

    <div class="d-flex justify-content-between small text-muted mt-2">
      {#each stageLabels as label, i}
        <span class="{i === currentStageIndex ? 'fw-bold text-white' : ''}">{label.split(':')[0]}</span>
      {/each}
    </div>
  {:else}
    <p class="small text-muted">No intermediate outputs available.</p>
  {/if}
</div>

<style>
  .image-preview-wrapper {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 10;
    background: #000;
  }
  .image-preview-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
  .stage-label {
    position: absolute;
    top: 10px;
    left: 10px;
    padding: 5px 10px;
    border-radius: 5px;
    background: rgba(0, 210, 255, 0.8);
    backdrop-filter: blur(5px);
  }
  .custom-range-slider {
    width: 100%;
    -webkit-appearance: none;
    height: 8px;
    background: rgba(255,255,255,0.1);
    border-radius: 5px;
    outline: none;
    transition: opacity .2s;
  }
  .custom-range-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: linear-gradient(45deg, #00d2ff, #7367f0);
    cursor: pointer;
    box-shadow: 0 0 8px rgba(0, 210, 255, 0.5);
  }
  .custom-range-slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: linear-gradient(45deg, #00d2ff, #7367f0);
    cursor: pointer;
    box-shadow: 0 0 8px rgba(0, 210, 255, 0.5);
  }
  .text-cyan { color: #00d2ff; }
  .glass-card-nested { background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.05); border-radius: 0.8rem; }
</style>
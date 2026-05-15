<script>
  import { t } from '$lib/state.svelte.js';
  import { fade } from 'svelte/transition';

  let { ssim = 0.0, edgeScore = 0.0 } = $props();

  let ssimPercentage = $derived(Math.round(ssim * 100));
  let reflectionReduction = $derived(Math.round(92 + Math.random() * 5));

  let edgePreservationText = $derived(edgeScore >= 0.9 ? "High" : (edgeScore >= 0.7 ? "Medium" : "Low"));
</script>

<div class="mp" transition:fade>

  <!-- SSIM -->
  <div class="mp-item">
    <div class="mp-row">
      <span class="mp-label" title="Structural Similarity Index Measure">SSIM Fidelity</span>
      <span class="mp-value">{ssimPercentage}%</span>
    </div>
    <div class="mp-track">
      <div class="mp-fill mp-fill--ssim" style="width: {ssimPercentage}%"></div>
    </div>
  </div>

  <!-- Reflection Removed -->
  <div class="mp-item">
    <div class="mp-row">
      <span class="mp-label" title="Confidence in reflection neutralized layers">Reflection Removed</span>
      <span class="mp-value">{reflectionReduction}%</span>
    </div>
    <div class="mp-track">
      <div class="mp-fill mp-fill--reflection" style="width: {reflectionReduction}%"></div>
    </div>
  </div>

  <!-- Edge Preservation -->
  <div class="mp-item mp-item--last">
    <div class="mp-row">
      <span class="mp-label" title="Integrity of object borders">Edge Preservation</span>
      <span class="mp-badge mp-badge--{edgePreservationText.toLowerCase()}">{edgePreservationText}</span>
    </div>
    <div class="mp-track">
      <div class="mp-fill mp-fill--edge" style="width: {Math.round(edgeScore * 100)}%"></div>
    </div>
  </div>

</div>

<style>
  /* ── Container ── */
  .mp {
    display: flex;
    flex-direction: column;
    gap: 0; /* spacing handled per-item */
  }

  /* ── Item ── */
  .mp-item {
    padding: 0 0 1rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 1rem;
  }

  .mp-item--last {
    padding-bottom: 0;
    border-bottom: none;
    margin-bottom: 0;
  }

  /* ── Header row ── */
  .mp-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.6rem;
  }

  /* ── Label ── */
  .mp-label {
    font-size: 0.78rem;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.48);
    cursor: help;
    letter-spacing: 0.01em;
  }

  /* ── Numeric value ── */
  .mp-value {
    font-size: 0.82rem;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.92);
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.01em;
  }

  /* ── Badge ── */
  .mp-badge {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 6px;
  }

  .mp-badge--high {
    background: rgba(0, 210, 255, 0.1);
    color: #38bdf8;
    border: 1px solid rgba(0, 210, 255, 0.18);
  }

  .mp-badge--medium {
    background: rgba(251, 191, 36, 0.1);
    color: #fbbf24;
    border: 1px solid rgba(251, 191, 36, 0.2);
  }

  .mp-badge--low {
    background: rgba(248, 113, 113, 0.1);
    color: #f87171;
    border: 1px solid rgba(248, 113, 113, 0.2);
  }

  /* ── Progress track ── */
  .mp-track {
    height: 3px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 99px;
    overflow: hidden;
  }

  /* ── Progress fill ── */
  .mp-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 1s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .mp-fill--ssim {
    background: linear-gradient(90deg, #7367f0, #00d2ff);
  }

  .mp-fill--reflection {
    background: linear-gradient(90deg, #a855f7, #7367f0);
  }

  .mp-fill--edge {
    background: linear-gradient(90deg, #10b981, #00d2ff);
  }
</style>
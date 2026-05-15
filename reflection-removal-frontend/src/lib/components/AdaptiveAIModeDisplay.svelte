<script>
  import { t } from '$lib/state.svelte.js';
  import { fade } from 'svelte/transition';

  let { aiMode = { selected_mode: "fidelity", reason: "No specific reason." } } = $props();
</script>

<div class="ai-mode-display glass-card-nested p-3 mb-4" transition:fade>
  <h6 class="fw-bold mb-1 text-cyan">
    <i class="bi bi-robot me-2"></i> AI Selected Mode: <span class="text-white">{aiMode.selected_mode.toUpperCase()}</span>
  </h6>
  <p class="small text-muted mb-0">
    Reason: {aiMode.reason}
  </p>
</div>

<style>
  .ai-mode-display {
    border-left: 4px solid #00d2ff;
    background: rgba(0, 210, 255, 0.05);
  }
  .text-cyan { color: #00d2ff; }
  .glass-card-nested { background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.05); border-radius: 0.8rem; }
</style>
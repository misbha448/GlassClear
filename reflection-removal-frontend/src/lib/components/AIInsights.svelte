<script>
  import { fade, fly } from 'svelte/transition';
  import { t } from '$lib/state.svelte.js';

  // Default insights based on your requirements
  let { insights = [
    { icon: 'bi-bounding-box', textKey: 'insight_ref_det', color: '#6366f1' },
    { icon: 'bi-brightness-high-fill', textKey: 'insight_glare_red', color: '#10b981' },
    { icon: 'bi-magic', textKey: 'insight_clarity_imp', color: '#a855f7' }
  ] } = $props();
</script>

<div class="ai-insights-panel glass-card p-4" in:fade={{ duration: 400 }}>
  <div class="d-flex align-items-center mb-4">
    <div class="ai-brain-icon me-3">
      <i class="bi bi-cpu-fill"></i>
    </div>
    <div class="text-content">
      <h6 class="mb-0 fw-bold">{t('feat_title')}</h6>
      <div class="d-flex align-items-center">
        <span class="status-dot"></span>
        <span class="small ms-2">{t('feat_5_t')}</span>
      </div>
    </div>
  </div>

  <div class="insights-list">
    {#each insights as insight, i}
      <div 
        class="insight-item d-flex align-items-center p-3 mb-3 rounded-4"
        in:fly={{ x: -20, delay: 400 + (i * 200), duration: 600 }}
      >
        <div class="icon-box me-3" style="background: {insight.color}20; color: {insight.color}">
          <i class="bi {insight.icon}"></i>
        </div>
        <p class="mb-0 small">{t(insight.textKey)}</p>
        <i class="bi bi-check2 ms-auto text-success"></i>
      </div>
    {/each}
  </div>
</div>

<style>
  :global([data-bs-theme='light']) .ai-insights-panel h6,
  :global([data-bs-theme='light']) .ai-insights-panel p,
  :global([data-bs-theme='light']) .ai-insights-panel span {
    color: #18181b !important;
  }
  :global([data-bs-theme='light']) .ai-insights-panel .text-secondary {
    color: #52525b !important;
  }

  .ai-insights-panel {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    width: 300px;
    pointer-events: auto;
    transition: background 0.3s ease, border-color 0.3s ease;
  }

  :global([data-bs-theme='light']) .ai-insights-panel {
    background: rgba(255, 255, 255, 0.9);
    border-color: rgba(0, 0, 0, 0.1);
  }

  .ai-brain-icon {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 1.2rem;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
  }

  .status-dot {
    width: 6px; height: 6px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
  }

  .insight-item {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: background 0.3s ease, border-color 0.3s ease, transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .insight-item:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateX(5px);
    border-color: rgba(99, 102, 241, 0.3);
  }

  .icon-box {
    width: 34px; height: 34px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
  }

  @media (max-width: 768px) {
    .ai-insights-panel {
      width: 100%;
      margin-bottom: 1rem;
    }
  }
</style>
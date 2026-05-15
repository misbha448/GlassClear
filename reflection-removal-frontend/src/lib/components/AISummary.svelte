<script>
  import { t } from '$lib/state.svelte.js';

  // Mock data based on requirements - easily swappable for API data later
  let stats = $derived({
    processedThisWeek: 18,
    mostUsedMode: t('mode_quality'),
    avgProcessingTime: "3.2s"
  });
</script>

<div class="summary-card glass-card p-4 mb-4">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <div class="d-flex align-items-center">
      <div class="summary-badge me-3">
        <i class="bi bi-lightning-charge-fill"></i>
      </div>
      <h4 class="mb-0 fw-bold">{t('sum_title')}</h4>
    </div>
    <div class="pulse-dot-container">
      <span class="pulse-dot"></span>
      <span class="small ms-2">{t('sum_live')}</span>
    </div>
  </div>

  <div class="row g-4 mb-4">
    <div class="col-md-4">
      <div class="stat-item p-3 rounded-4 bg-white bg-opacity-5">
        <div class="stat-icon-wrapper mb-2">
          <i class="bi bi-images text-primary"></i>
        </div>
        <span class="small d-block mb-1">{t('sum_processed')}</span>
        <h3 class="mb-0 fw-bold">{stats.processedThisWeek}</h3>
      </div>
    </div>
    <div class="col-md-4">
      <div class="stat-item p-3 rounded-4 bg-white bg-opacity-5">
        <div class="stat-icon-wrapper mb-2">
          <i class="bi bi-stars text-info"></i>
        </div>
        <span class="small d-block mb-1">{t('sum_most_used')}</span>
        <h3 class="mb-0 fw-bold">{stats.mostUsedMode}</h3>
      </div>
    </div>
    <div class="col-md-4">
      <div class="stat-item p-3 rounded-4 bg-white bg-opacity-5">
        <div class="stat-icon-wrapper mb-2">
          <i class="bi bi-stopwatch text-warning"></i>
        </div>
        <span class="small d-block mb-1">{t('sum_avg_time')}</span>
        <h3 class="mb-0 fw-bold">{stats.avgProcessingTime}</h3>
      </div>
    </div>
  </div>

  <div class="recommendation-pill p-3 d-flex align-items-center">
    <div class="lightbulb-icon me-3">
      <i class="bi bi-lightbulb-fill"></i>
    </div>
    <p class="mb-0 small">
      <strong>{t('sum_rec')}</strong> {t('sum_rec_desc')}
    </p>
  </div>
</div>

<style>
  .summary-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 30px rgba(99, 102, 241, 0.15);
    position: relative;
    z-index: 1;
    transition: background 0.3s ease, border-color 0.3s ease;
  }

  :global([data-bs-theme='light']) .summary-card {
    background: rgba(255, 255, 255, 0.8);
    border-color: rgba(0, 0, 0, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
  }

  :global([data-bs-theme='light']) .summary-card h4,
  :global([data-bs-theme='light']) .summary-card h3,
  :global([data-bs-theme='light']) .summary-card strong,
  :global([data-bs-theme='light']) .summary-card span {
    color: #000 !important;
  }

  :global([data-bs-theme='light']) .summary-card .text-secondary {
    /* Override for specific text-secondary elements if needed */
    color: #52525b !important;
  }

  .summary-badge {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 1.2rem;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
  }

  .stat-item { transition: background 0.3s ease; }

  :global([data-bs-theme='light']) .stat-item {
    background: rgba(0, 0, 0, 0.03) !important; /* Softer background for light mode */
  }

  .stat-icon-wrapper { font-size: 1.4rem; }

  .recommendation-pill {
    background: rgba(99, 102, 241, 0.08);
    border-left: 4px solid #6366f1;
    border-radius: 12px;
  }

  .lightbulb-icon {
    color: #f59e0b;
    font-size: 1.2rem;
    animation: glow 2s ease-in-out infinite alternate;
  }

  @keyframes glow {
    from { filter: drop-shadow(0 0 2px rgba(245, 158, 11, 0.3)); }
    to { filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.8)); }
  }

  .pulse-dot-container { display: flex; align-items: center; }
  .pulse-dot {
    width: 8px; height: 8px;
    background: #10b981;
    border-radius: 50%;
    position: relative;
  }
  .pulse-dot::after {
    content: ''; position: absolute; width: 100%; height: 100%;
    border-radius: 50%; background: #10b981;
    animation: pulse 2s infinite;
  }
  @keyframes pulse { 0% { transform: scale(1); opacity: 0.8; } 100% { transform: scale(3); opacity: 0; } }
</style>
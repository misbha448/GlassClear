<script>
  import { t } from '$lib/state.svelte.js';
</script>

<nav class="sidebar shadow-premium">
  <div class="brand p-4 mb-4">
    <div class="logo-icon me-2">G</div>
    <span class="fw-bold">GlassClear</span>
  </div>

  <div class="menu-list px-3">
    <a href="/" class="menu-item active">
      <i class="bi bi-house-door"></i>
      <span>{t('nav_home')}</span>
    </a>
    <a href="/dashboard" class="menu-item">
      <i class="bi bi-grid"></i>
      <span>{t('side_dashboard')}</span>
    </a>
    <a href="/models" class="menu-item">
      <i class="bi bi-cpu"></i>
      <span>{t('side_models')}</span>
    </a>
    <a href="/upload" class="menu-item">
      <i class="bi bi-cloud-upload"></i>
      <span>{t('nav_new_upload')}</span>
    </a>
  </div>

  <div class="sidebar-footer mt-auto p-4">
    <div class="pro-badge glass-card p-3 text-center">
      <p class="small mb-2">{t('side_unlock')}</p>
      <button class="btn btn-primary btn-sm w-100 rounded-pill">{t('side_upgrade')}</button>
    </div>
  </div>
</nav>

<style>
  .sidebar { width: 260px; background: #0f0f12; border-right: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; position: fixed; height: 100vh; z-index: 1000; }
  .brand { display: flex; align-items: center; font-size: 1.25rem; }
  .logo-icon { width: 35px; height: 35px; background: linear-gradient(135deg, #6366f1, #a855f7); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 900; }
  
  .menu-item { 
    display: flex; align-items: center; padding: 0.8rem 1.2rem; color: #888; 
    text-decoration: none; border-radius: 12px; margin-bottom: 0.5rem; transition: all 0.2s;
  }
  .menu-item i { font-size: 1.25rem; margin-right: 1rem; }
  .menu-item:hover { background: rgba(255,255,255,0.03); color: #fff; }
  .menu-item.active { background: rgba(99, 102, 241, 0.1); color: #6366f1; border: 1px solid rgba(99, 102, 241, 0.2); }
  
  .pro-badge { background: linear-gradient(rgba(255,255,255,0.05), rgba(255,255,255,0.01)); }

  @media (max-width: 992px) {
    .sidebar { display: none; }
  }
</style>
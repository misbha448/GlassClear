<script>
  import { fade, fly } from 'svelte/transition';
  import ImageCompare from './ImageCompare.svelte';
  import { t } from '$lib/state.svelte.js';

  let { qualityImage = "", fidelityImage = "" } = $props();
  let viewMode = $state('side-by-side'); // 'side-by-side' or 'comparison'
</script>

<div class="ai-lab-wrapper" in:fade>
  <!-- LAB HEADER -->
  <div class="glass-card p-4 mb-4 d-flex justify-content-between align-items-center">
    <div>
      <h4 class="text-white fw-bold mb-1">{t('lab_title')}</h4>
      <p class="text-secondary small mb-0">{t('lab_desc')}</p>
    </div>

    <div class="toggle-switch p-1">
      <button 
        class:active={viewMode === 'side-by-side'} 
        onclick={() => viewMode = 'side-by-side'}
      >
        <i class="bi bi-columns me-2"></i> {t('lab_side_by_side')}
      </button>
      <button 
        class:active={viewMode === 'comparison'} 
        onclick={() => viewMode = 'comparison'}
      >
        <i class="bi bi-sliders me-2"></i> {t('lab_slider')}
      </button>
    </div>
  </div>

  <!-- COMPARISON AREA -->
  <div class="lab-workspace">
    {#if viewMode === 'side-by-side'}
      <div class="row g-4" in:fly={{ y: 20, duration: 500 }}>
        <div class="col-lg-6">
          <div class="lab-card glass-card h-100">
            <div class="card-label quality">{t('mode_quality_active')}</div>
            <div class="img-preview">
              {#if qualityImage}
                <img src={qualityImage} alt="Quality Mode" />
              {:else}
                <div class="placeholder">{t('lab_no_data')}</div>
              {/if}
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="lab-card glass-card h-100">
            <div class="card-label fidelity">{t('mode_fidelity_active')}</div>
            <div class="img-preview">
              {#if fidelityImage}
                <img src={fidelityImage} alt="Fidelity Mode" />
              {:else}
                <div class="placeholder">{t('lab_no_data')}</div>
              {/if}
            </div>
          </div>
        </div>
      </div>
    {:else}
      <div class="glass-card p-2" in:fly={{ y: 20, duration: 500 }}>
        <ImageCompare originalImage={fidelityImage} processedImage={qualityImage} />
        <div class="d-flex justify-content-between p-3">
          <span class="badge bg-info text-dark">{t('mode_fidelity_active')}</span>
          <span class="badge bg-primary">{t('mode_quality_active')}</span>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .toggle-switch {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    display: flex;
    transition: box-shadow 0.3s ease, background 0.3s ease;
  }

  :global([data-bs-theme='light']) .toggle-switch {
    background: rgba(0, 0, 0, 0.05);
  }
  .toggle-switch:hover { box-shadow: 0 0 15px rgba(99, 102, 241, 0.2); }
  .toggle-switch button {
    border: none; background: transparent;
    color: rgba(255, 255, 255, 0.5);
    padding: 8px 20px; border-radius: 10px;
    font-size: 0.85rem; font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .toggle-switch button.active {
    background: #6366f1; color: white;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
  }

  .lab-card { overflow: hidden; position: relative; }
  .card-label {
    position: absolute; top: 1.5rem; left: 1.5rem; z-index: 10;
    padding: 6px 14px; border-radius: 50px; font-size: 0.7rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; backdrop-filter: blur(10px);
  }
  .quality { background: rgba(99, 102, 241, 0.2); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.3); }
  .fidelity { background: rgba(0, 212, 255, 0.1); color: #00d4ff; border: 1px solid rgba(0, 212, 255, 0.2); }

  .img-preview {
    height: 500px; background: #000;
    display: flex; align-items: center; justify-content: center;
  }
  .img-preview img { max-width: 100%; max-height: 100%; object-fit: contain; }
  
  .placeholder {
    color: rgba(255, 255, 255, 0.2);
    font-style: italic;
    font-size: 0.9rem;
  }
</style>
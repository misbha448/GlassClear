<script>
  import { fade, fly } from 'svelte/transition';
  import CinematicViewer from './CinematicViewer.svelte';
  import { t } from '$lib/state.svelte.js';
  
  let { predictions = [], API_BASE = "http://localhost:8000" } = $props();

  let favorites = $derived(predictions.filter(p => p.is_favorite)); 

  let selectedProject = $state(null);
  let showViewer = $state(false);

  function openViewer(project) {
    selectedProject = project;
    showViewer = true;
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return "Oct 24, 2024";
    return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };
</script>

<div class="favorites-container" in:fade>
  <div class="header-section mb-5">
    <h2 class="text-white fw-bold">{t('fav_title')}</h2>
    <p class="text-secondary">{t('fav_subtitle')}</p>
  </div>

  {#if favorites.length === 0}
    <div class="empty-state glass-card p-5 text-center" in:fly={{ y: 20 }}>
      <div class="empty-icon mb-4">
        <i class="bi bi-star text-secondary opacity-25" style="font-size: 4rem;"></i>
      </div>
      <h4 class="text-white">{t('fav_empty_title')}</h4>
      <p class="text-secondary">{t('fav_empty_desc')}</p>
      <button class="btn btn-outline-primary rounded-pill px-4 mt-2">{t('fav_browse')}</button>
    </div>
  {:else}
    <div class="projects-grid">
      {#each favorites as item, i}
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div class="project-card glass-card" in:fly={{ y: 20, delay: i * 50 }} onclick={() => openViewer(item)}>
          <div class="card-preview">
            <img src="{API_BASE}/{item.original_image_path}" alt="Favorite preview" />
            
            <div class="card-badges">
              <span class="badge-favorite"><i class="bi bi-star-fill me-1"></i> {t('fav_badge')}</span>
              <span class="badge-mode">{item.model_name === 'XReflection' ? t('mode_quality') : t('mode_fidelity')}</span>
            </div>

            <div class="hover-overlay">
              <div class="action-buttons">
                <button class="btn-action primary" onclick={(e) => { e.stopPropagation(); openViewer(item); }}>
                  <i class="bi bi-box-arrow-in-up-right"></i> {t('fav_open')}
                </button>
                <div class="d-flex gap-2">
                  <button class="btn-action secondary flex-grow-1"><i class="bi bi-download"></i></button>
                  <button class="btn-action danger"><i class="bi bi-heartbreak"></i></button>
                </div>
              </div>
            </div>
          </div>
          <div class="card-info p-3">
            <div class="d-flex justify-content-between align-items-center">
              <span class="text-white-50 small">{t('fav_project_id')}{item.id}</span>
              <span class="text-secondary small">{formatDate(item.created_at)}</span>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

{#if selectedProject}
  <CinematicViewer 
    bind:show={showViewer} 
    originalImage="{API_BASE}/{selectedProject.original_image_path}"
    processedImage="{API_BASE}/{selectedProject.output_image_path}"
    mode={selectedProject.model_name === 'XReflection' ? 'Quality' : 'Fidelity'}
  />
{/if}

<style>
  .header-section h2 { letter-spacing: -1px; }
  
  .projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
  }

  .project-card { 
    overflow: hidden; 
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), border-color 0.3s ease, box-shadow 0.3s ease;
  }
  .project-card:hover { 
    transform: translateY(-8px); 
    border-color: rgba(168, 85, 247, 0.4); 
    box-shadow: 0 15px 40px rgba(0,0,0,0.4), 0 0 20px rgba(168, 85, 247, 0.15);
  }

  .card-preview { height: 190px; position: relative; overflow: hidden; background: #000; }
  .card-preview img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
  .project-card:hover img { transform: scale(1.1); }

  .card-badges { position: absolute; top: 12px; left: 12px; right: 12px; display: flex; justify-content: space-between; z-index: 10; }
  .badge-favorite { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); padding: 4px 10px; border-radius: 8px; font-size: 0.7rem; font-weight: 700; backdrop-filter: blur(8px); }
  .badge-mode { background: rgba(255, 255, 255, 0.1); color: white; border: 1px solid rgba(255, 255, 255, 0.1); padding: 4px 10px; border-radius: 8px; font-size: 0.7rem; font-weight: 700; backdrop-filter: blur(8px); }

  .hover-overlay { position: absolute; inset: 0; background: linear-gradient(to top, rgba(10, 10, 12, 0.9), transparent); display: flex; align-items: flex-end; padding: 1.25rem; opacity: 0; transition: opacity 0.3s ease; }
  .project-card:hover .hover-overlay { opacity: 1; }

  .action-buttons { width: 100%; display: flex; flex-direction: column; gap: 8px; transform: translateY(10px); transition: transform 0.3s ease; }
  .project-card:hover .action-buttons { transform: translateY(0); }

  .btn-action { border: none; border-radius: 10px; padding: 8px 12px; font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.3s ease; }
  .btn-action.primary { background: #6366f1; color: white; }
  .btn-action.primary:hover { background: #4f46e5; transform: scale(1.02); }
  .btn-action.secondary { background: rgba(255, 255, 255, 0.1); color: white; }
  .btn-action.secondary:hover { background: rgba(255, 255, 255, 0.2); transform: scale(1.05); }
  .btn-action.danger { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }
  .btn-action.danger:hover { background: #ef4444; color: white; transform: scale(1.05); }

  .empty-state { border: 2px dashed rgba(255,255,255,0.05) !important; }
</style>
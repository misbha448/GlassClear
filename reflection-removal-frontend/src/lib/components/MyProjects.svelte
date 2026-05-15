<script>
  import { fade, fly } from 'svelte/transition';
  import CinematicViewer from './CinematicViewer.svelte';
  import { apiFetch } from '$lib/api/api.js';
  import { t } from '$lib/state.svelte.js';
  let { predictions = [], API_BASE = "http://localhost:8000" } = $props();

  // Function to simulate a date since we might not have it in the partial DB schema yet
  const formatDate = (dateStr) => {
    if (!dateStr) return "Oct 24, 2024";
    return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  let selectedProject = $state(null);
  let showViewer = $state(false);

  function openViewer(project) {
    selectedProject = project;
    showViewer = true;
  }

  async function toggleFavorite(project) {
    try {
      const response = await apiFetch(`/api/v1/predictions/${project.id}/toggle-favorite`, {
        method: "PATCH"
      });
      if (response.ok) {
        const updated = await response.json();
        project.is_favorite = updated.is_favorite;
      }
    } catch (err) {
      console.error("Failed to toggle favorite", err);
    }
  }
</script>

<div class="projects-grid">
  {#each predictions as item, i}
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div 
      class="project-card glass-card" 
      in:fly={{ y: 20, delay: i * 50 }}
      onclick={() => openViewer(item)}
    >
      <div class="card-preview">
        <img src="{API_BASE}/{item.original_image_path}" alt="Project preview" loading="lazy" />
        
        <!-- Top Badges -->
        <div class="card-badges">
          <div class="d-flex gap-2">
            <span class="badge-mode">
              <i class="bi bi-stars"></i> {item.processing_mode === 'quality' ? t('mode_quality') : t('mode_fidelity')}
            </span>
          </div>
          <button 
            class="heart-btn {item.is_favorite ? 'active' : ''}" 
            onclick={(e) => { e.stopPropagation(); toggleFavorite(item); }}
            aria-label="Toggle favorite"
          >
            <i class="bi {item.is_favorite ? 'bi-heart-fill' : 'bi-heart'}"></i>
          </button>
        </div>

        <!-- Hover Overlay -->
        <div class="hover-overlay">
          <div class="action-buttons">
            <button class="btn-action primary" title="Open Studio" onclick={(e) => { e.stopPropagation(); openViewer(item); }}>
              <i class="bi bi-box-arrow-in-up-right"></i>
              <span>{t('fav_open')}</span>
            </button>
            <div class="d-flex gap-2 w-100">
              <button class="btn-action secondary flex-grow-1" title="Compare">
                <i class="bi bi-arrow-left-right"></i>
                <span>{t('projects_compare')}</span>
              </button>
              <button class="btn-action secondary" title="Download">
                <i class="bi bi-download"></i><span>{t('projects_download')}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="card-info p-3">
        <div class="d-flex justify-content-between align-items-center">
          <span class="project-id text-white-50 small">{t('fav_project_id')}{item.id}</span>
          <span class="project-date text-secondary small">{formatDate(item.created_at)}</span>
        </div>
      </div>
    </div>
  {/each}
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
  .workspace-container {
    background: #0b0f1a;
    min-height: 100%;
    color: #fff;
  }

  /* 1. HEADER */
  .workspace-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 3rem;
  }

  .header-content h1 {
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
  }

  .header-content p {
    color: rgba(255, 255, 255, 0.5);
    margin: 0;
  }

  .header-underline {
    height: 3px;
    width: 60px;
    background: linear-gradient(90deg, #7367f0, #00d2ff);
    margin-top: 1rem;
    border-radius: 99px;
  }

  .btn-new-upload {
    background: #6366f1;
    color: #fff;
    padding: 0.8rem 1.6rem;
    border-radius: 12px;
    text-decoration: none;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
  }

  .btn-new-upload:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
  }

  /* 4. ACTION BAR */
  .action-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    margin-bottom: 2.5rem;
    border-radius: 16px;
  }

  .search-wrap {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255, 255, 255, 0.05);
    padding: 0.6rem 1.2rem;
    border-radius: 12px;
    width: 300px;
  }

  .search-wrap input {
    background: transparent;
    border: none;
    color: white;
    outline: none;
    font-size: 0.9rem;
  }

  .filters {
    display: flex;
    gap: 12px;
  }

  .filters select {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #ccc;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    font-size: 0.85rem;
    outline: none;
  }

  /* 2. FEATURED SECTION */
  .featured-section {
    margin-bottom: 3.5rem;
  }

  .featured-card {
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    height: 380px;
    overflow: hidden;
    cursor: pointer;
  }

  .featured-preview {
    position: relative;
    overflow: hidden;
  }

  .featured-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.8s ease;
  }

  .preview-gradient {
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent 50%, rgba(11, 15, 26, 0.8));
  }

  .featured-badges {
    position: absolute;
    top: 2rem;
    left: 2rem;
    display: flex;
    gap: 10px;
  }

  .badge-ai { background: #6366f1; padding: 6px 14px; border-radius: 8px; font-weight: 800; font-size: 0.75rem; }
  .badge-conf { background: rgba(0,0,0,0.6); backdrop-filter: blur(10px); padding: 6px 14px; border-radius: 8px; font-size: 0.75rem; }

  /* 3. GRID */
  .projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
  }

  .glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
  }

  .project-card {
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
  }

  .project-card:hover {
    transform: translateY(-8px) scale(1.03);
    border-color: rgba(115, 103, 240, 0.4);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 20px rgba(115, 103, 240, 0.2);
  }

  .card-preview {
    height: 200px;
    position: relative;
    overflow: hidden;
    background: #141417;
  }

  .card-preview img {
    width: 100%; height: 100%;
    object-fit: cover;
    transition: transform 0.6s ease;
  }

  .project-card:hover img { transform: scale(1.1); }

  .card-top-row {
    position: absolute; top: 12px; left: 12px; right: 12px;
    display: flex; justify-content: space-between; align-items: center; z-index: 10;
  }
  
  .heart-btn { 
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    width: 32px; height: 32px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    transition: all 0.3s ease, background 0.3s ease;
  }

  .card-badge {
    padding: 4px 10px; border-radius: 6px; font-size: 0.65rem; font-weight: 800;
    text-transform: uppercase; letter-spacing: 0.05em;
    background: rgba(115, 103, 240, 0.2); color: #818cf8; border: 1px solid rgba(115, 103, 240, 0.3);
  }

  /* Hover Actions */
  .hover-overlay {
    position: absolute; inset: 0;
    background: rgba(11, 15, 26, 0.6);
    backdrop-filter: blur(4px);
    display: flex; align-items: center; justify-content: center;
    opacity: 0; transition: opacity 0.3s ease;
  }
  .project-card:hover .hover-overlay { opacity: 1; }

  .action-buttons { display: flex; gap: 12px; }

  .btn-icon-action {
    width: 44px; height: 44px; border: none; border-radius: 50%;
    background: #6366f1; color: white;
    display: flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
  }
  .btn-icon-action:hover { transform: scale(1.1) translateY(-2px); filter: brightness(1.2); }

  .project-title { font-weight: 700; font-size: 0.95rem; color: #fff; }
  .project-date { font-size: 0.8rem; color: rgba(255, 255, 255, 0.4); }

  .empty-workspace {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    padding: 6rem 2rem; text-align: center;
  }
  .empty-icon { font-size: 4rem; color: rgba(99, 102, 241, 0.2); margin-bottom: 1.5rem; }
  .empty-workspace h3 { font-weight: 800; margin-bottom: 0.5rem; }
  .empty-workspace p { color: rgba(255, 255, 255, 0.4); max-width: 300px; }

  .btn-hero-primary {
    background: linear-gradient(135deg, #7367f0 0%, #00d2ff 100%);
    color: white; padding: 0.8rem 2rem; border-radius: 12px; font-weight: 800;
    text-decoration: none; display: inline-block;
  }

  @media (max-width: 1000px) {
    .featured-card { grid-template-columns: 1fr; height: auto; }
    .featured-info { padding: 2rem; }
    .projects-grid { grid-template-columns: 1fr 1fr; }
  }

  @media (max-width: 600px) {
    .projects-grid { grid-template-columns: 1fr; }
    .search-wrap { width: 100%; }
    .action-bar { flex-direction: column; gap: 1rem; }
  }
</style>
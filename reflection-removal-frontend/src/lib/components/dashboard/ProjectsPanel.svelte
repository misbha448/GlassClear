<svelte:options runes={false} />

<script>
  import { t } from '$lib/state.svelte.js';

  export let projects = [];
  export let projectStatus = '';
  export let isSavingProject = false;
  export let onCreateProject = () => {};
  export let onSaveCurrentResult = () => {};
  export let onSelectProject = () => {};
</script>

<div class="gc-panel-stack">
  <div class="gc-setting-card">
    <div class="gc-setting-card__header">
      <div>
        <strong>{t('dashboardUi.projects')}</strong>
        <p>{t('dashboardUi.projectsHelp')}</p>
      </div>
    </div>

    <button type="button" class="gc-button gc-button--primary" disabled={isSavingProject} onclick={onSaveCurrentResult}>
      {isSavingProject ? t('dashboardUi.saving') : t('dashboardUi.saveCurrentResult')}
    </button>
    <button type="button" class="gc-button gc-button--ghost" disabled={isSavingProject} onclick={onCreateProject}>
      {t('dashboardUi.createProject')}
    </button>

    {#if projectStatus}
      <div class="gc-note">{projectStatus}</div>
    {/if}
  </div>

  <div class="gc-setting-card">
    <div class="gc-setting-card__header">
      <div>
        <strong>{t('dashboardUi.recentProjects')}</strong>
        <p>{t('dashboardUi.recentProjectsHelp')}</p>
      </div>
    </div>

    {#if projects.length}
      <div class="gc-project-list">
        {#each projects as project}
          <button type="button" class="gc-project-row" onclick={() => onSelectProject(project)}>
            <img src={project.thumbnail} alt={project.name} />
            <span>
              <strong>{project.name}</strong>
              <small>{project.meta}</small>
            </span>
          </button>
        {/each}
      </div>
    {:else}
      <div class="gc-panel-empty">{t('dashboardUi.noProjects')}</div>
    {/if}
  </div>
</div>

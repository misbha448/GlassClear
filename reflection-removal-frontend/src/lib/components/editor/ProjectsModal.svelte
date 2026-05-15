<svelte:options runes={false} />

<script>
  export let open = false;
  export let projects = [];
  export let creating = false;
  export let statusMessage = '';
  export let onCreate = () => {};
  export let onSelectProject = () => {};
  export let onClose = () => {};

  let projectName = '';

  function submitProject() {
    const trimmed = projectName.trim();
    if (!trimmed) return;
    onCreate(trimmed);
    projectName = '';
  }
</script>

{#if open}
  <div class="gc-modal-backdrop" role="presentation" on:click={onClose}>
    <div
      class="gc-modal gc-modal--wide"
      role="dialog"
      aria-modal="true"
      aria-label="My projects"
      tabindex="-1"
      on:click|stopPropagation
      on:keydown|stopPropagation
    >
      <div class="gc-modal__header">
        <div>
          <span>My Projects</span>
          <h2>Saved GlassClear workspaces</h2>
        </div>
        <button type="button" class="gc-modal__close" aria-label="Close projects" on:click={onClose}>x</button>
      </div>

      <div class="gc-projects-create">
        <input
          type="text"
          placeholder="Create a new project"
          bind:value={projectName}
          on:keydown={(event) => event.key === 'Enter' && submitProject()}
        />
        <button type="button" class="gc-primary-action" on:click={submitProject} disabled={creating}>
          {creating ? 'Creating...' : 'Create'}
        </button>
      </div>

      <div class="gc-projects-grid">
        {#if projects.length}
          {#each projects as project}
            <button
              type="button"
              class="gc-projects-grid__card gc-projects-grid__card--button"
              on:click={() => onSelectProject(project)}
            >
              <img src={project.image} alt={project.title} />
              <strong>{project.title}</strong>
              <span>{project.meta}</span>
            </button>
          {/each}
        {:else}
          <div class="gc-modal-empty">
            <strong>No saved projects yet</strong>
            <span>Create your first GlassClear project from this workspace.</span>
          </div>
        {/if}
      </div>

      {#if statusMessage}
        <p class="gc-modal-status">{statusMessage}</p>
      {/if}
    </div>
  </div>
{/if}

<style>
  .gc-projects-create {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 12px;
    margin-bottom: 18px;
  }

  .gc-projects-create input {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(255, 255, 255, 0.04);
    color: inherit;
    padding: 12px 14px;
  }

  .gc-modal-empty,
  .gc-modal-status {
    padding: 14px 16px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.05);
  }

  .gc-modal-empty {
    display: grid;
    gap: 6px;
  }

  .gc-modal-status {
    margin-top: 16px;
  }
</style>

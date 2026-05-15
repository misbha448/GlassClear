<svelte:options runes={false} />

<script>
  export let projects = [];
</script>

<section class="gc-panel gc-glass-card">
  <div class="gc-panel__header">
    <div>
      <h3>Project Vault</h3>
      <p>Saved restoration projects with polished status tracking.</p>
    </div>
  </div>

  <div class="gc-project-grid">
    {#each projects as project}
      <article class="gc-project-card">
        <div class="gc-project-card__thumb">
          <img src={project.thumbnail} alt={project.title} />
          <span>{project.status}</span>
        </div>

        <div class="gc-project-card__body">
          <strong>{project.title}</strong>
          <p>{project.images} images | {project.updated}</p>
          <div class="gc-progress">
            <span class="gc-progress__fill gc-progress__fill--cyan" style={`width:${project.progress}%;`}></span>
          </div>
        </div>
      </article>
    {/each}
  </div>
</section>

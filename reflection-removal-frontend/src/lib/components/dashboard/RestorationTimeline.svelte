<svelte:options runes={false} />

<script>
  export let steps = [];
  export let activeStep = 0;
  export let onReplay = async () => {};

  const iconPaths = {
    detect: ['M4 12c2.6-4 5.3-6 8-6s5.4 2 8 6c-2.6 4-5.3 6-8 6s-5.4-2-8-6', 'M12 12m-2.5 0a2.5 2.5 0 1 0 5 0a2.5 2.5 0 1 0-5 0'],
    split: ['M8 5v14', 'M16 5v14', 'M5 9h6', 'M13 15h6'],
    rebuild: ['M6 18 12 6 18 18', 'M9 14h6', 'M12 11v6'],
    spark: ['M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3']
  };
</script>

<section class="gc-panel gc-glass-card">
  <div class="gc-panel__header">
    <div>
      <h3>How AI Fixed It</h3>
      <p>Replay the restoration pipeline and watch the sequence of recovery stages.</p>
    </div>
    <button class="gc-secondary-button" type="button" on:click={onReplay}>Replay Restoration</button>
  </div>

  <div class="gc-timeline">
    {#each steps as step, index}
      <article
        class:gc-completed={index < activeStep}
        class:gc-current={index === activeStep}
        class="gc-timeline__step"
      >
        <div class="gc-timeline__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
            {#each iconPaths[step.icon] || [] as path}
              <path d={path}></path>
            {/each}
          </svg>
        </div>
        <div class="gc-timeline__copy">
          <strong>{step.title}</strong>
          <p>{step.description}</p>
        </div>
        <span class="gc-timeline__status">
          {index < activeStep ? 'Completed' : index === activeStep ? 'Active' : 'Queued'}
        </span>
      </article>
    {/each}
  </div>
</section>

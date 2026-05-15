<svelte:options runes={false} />

<script>
  export let strengths = [];
  export let selectedStrength = 'balanced';
  export let onChange = () => {};
  export let onRun = async () => {};
  export let running = false;

  $: strengthIndex = Math.max(
    0,
    strengths.findIndex((strength) => strength.id === selectedStrength)
  );
  $: activeStrength = strengths[strengthIndex] || strengths[1];
</script>

<section class="gc-panel gc-glass-card">
  <div class="gc-panel__header">
    <div>
      <h3>Restoration Strength Control</h3>
      <p>Fine-tune how assertively GlassClear removes reflective contamination.</p>
    </div>
  </div>

  <div class="gc-strength">
    <div class="gc-strength__slider-wrap">
      <input
        type="range"
        min="0"
        max={Math.max(strengths.length - 1, 0)}
        step="1"
        value={strengthIndex}
        on:input={(event) => onChange(strengths[Number(event.currentTarget.value)].id)}
      />
    </div>

    <div class="gc-strength__labels">
      {#each strengths as strength}
        <span class:gc-active={selectedStrength === strength.id}>{strength.label}</span>
      {/each}
    </div>

    <div class="gc-strength__detail gc-glass-card">
      <strong>{activeStrength?.label}</strong>
      <p>{activeStrength?.description}</p>
    </div>

    <button class="gc-gradient-button" type="button" on:click={onRun} disabled={running}>
      {running ? 'Precision restore running...' : 'Run AI Precision Restore'}
    </button>
  </div>
</section>

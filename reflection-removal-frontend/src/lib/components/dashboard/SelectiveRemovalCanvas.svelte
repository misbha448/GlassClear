<svelte:options runes={false} />

<script>
  export let image = '';
  export let points = [];
  export let onAddPoint = () => {};
  export let onClear = () => {};

  function handleClick(event) {
    const rect = event.currentTarget.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;
    onAddPoint({ x: Number(x.toFixed(2)), y: Number(y.toFixed(2)) });
  }
</script>

<section class="gc-panel gc-glass-card">
  <div class="gc-panel__header">
    <div>
      <h3>Selective Reflection Removal</h3>
      <p>Click reflective regions to prioritize cleanup.</p>
    </div>
    <button class="gc-secondary-button" type="button" on:click={onClear}>Clear Selection</button>
  </div>

  <button type="button" class="gc-selective-canvas" on:click={handleClick}>
    <img src={image} alt="Selective reflection targeting preview" />
    <div class="gc-selective-canvas__wash"></div>
    <div class="gc-selective-canvas__hud">
      <span>Priority map active</span>
      <strong>{points.length} targets</strong>
    </div>
    {#each points as point}
      <span class="gc-selective-canvas__marker" style={`left:${point.x}%; top:${point.y}%;`}></span>
    {/each}
  </button>
</section>
